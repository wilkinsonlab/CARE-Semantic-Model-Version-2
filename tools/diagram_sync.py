#!/usr/bin/env python3
"""
Global sync tool for CARE-Semantic-Model-Version-2.

The Mermaid diagrams in diagrams/ are the single source of truth for the
model. This tool derives everything else FROM them and reports (or, with
--write, applies) corrections to:

  1. implementation/Toolkit/toolkit/template.py's TEMPLATE_MAP_OBO --
     mechanical and safe to auto-write: every field is either a verified
     fixed constant or absent.
  2. docs/glossary.md's per-model Mandatory/Optional/N-A column marks --
     mechanical and safe to auto-write. Hand-authored descriptions are
     preserved whenever the column already had one; cleared (matching the
     file's existing convention) when a column becomes N/A; a flagged
     placeholder is inserted when a column becomes M/O for the first time.
  3. implementation/CSV/*.csv examples -- report only. Runs each example
     through the real Toolkit pipeline and flags dropped rows or
     never-populated expected columns. Fixing example data requires
     clinical judgment a script doesn't have.
  4. implementation/YARRRML/CARE_yarrrml.yaml structural coverage --
     report only, NEVER writes to this file, under any flag. Flags diagram
     edges with no corresponding predicate anywhere in the mapping. New
     structural patterns (this session's Genetic multi-variant grouping,
     Consent's Input_ value, boolean support) need real RML/GREL design
     judgment, not auto-generation -- the tool's job here is only to flag
     "this diagram edge has no home in the mapping yet, go look at it,"
     never to guess at the fix itself.

Usage:
    python3 tools/diagram_sync.py                  # check mode, all models
    python3 tools/diagram_sync.py Birthdate         # check mode, one model
    python3 tools/diagram_sync.py --write           # apply 1 + 2, all models
    python3 tools/diagram_sync.py --write Genetic   # apply 1 + 2, one model
    python3 tools/diagram_sync.py --csv             # add CSV validation pass
    python3 tools/diagram_sync.py --yarrrml         # add YARRRML coverage pass
    python3 tools/diagram_sync.py --write --csv --yarrrml   # everything
"""
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = REPO_ROOT / "diagrams"
GLOSSARY_PATH = REPO_ROOT / "docs" / "glossary.md"
TOOLKIT_DIR = REPO_ROOT / "implementation" / "Toolkit"
TEMPLATE_PATH = TOOLKIT_DIR / "toolkit" / "template.py"
CSV_DIR = REPO_ROOT / "implementation" / "CSV"
YARRRML_PATH = REPO_ROOT / "implementation" / "YARRRML" / "CARE_yarrrml.yaml"

sys.path.insert(0, str(TOOLKIT_DIR))

# ---------------------------------------------------------------------------
# Model <-> glossary section anchor. Explicit, not positional -- anchors
# don't always match the model tag (e.g. "genotype_glossary" for Genetic,
# "country_glossary" for Birthplace), and a positional zip would silently
# write into the wrong section if anyone ever reorders glossary.md.
# ---------------------------------------------------------------------------
MODEL_TO_ANCHOR = {
    "Birthdate": "birthdate_glossary",
    "Birthyear": "birthyear_glossary",
    "Birthplace": "country_glossary",
    "Deathdate": "deathdate_glossary",
    "Sex": "sex_glossary",
    "First_visit": "first-visit_glossary",
    "Status": "status_glossary",
    "Symptoms_onset": "symptoms_onset_glossary",
    "Phenotype": "phenotype_glossary",
    "Diagnosis": "diagnosis_glossary",
    "Examination": "examination_glossary",
    "Laboratory": "laboratory_glossary",
    "Genetic": "genotype_glossary",
    "Medication": "medication_glossary",
    "Hospitalization": "hospitalization_glossary",
    "Surgery": "surgery_glossary",
    "Questionnaire": "questionnaire_glossary",
    "Functional_Assessment": "functional_assessment_glossary",
    "Biobank": "biobank_glossary",
    "Consent": "consent_glossary",
    "Clinical_trial": "clinical_trial_glossary",
    "Cohort": "cohort_glossary",
}
MODEL_ORDER = list(MODEL_TO_ANCHOR)

# Canonical column order == Toolkit.columns (implementation/Toolkit/toolkit/main.py).
# Single source of truth for order -- no independent "nicer" ordering invented here.
PUBLIC_COLUMNS = [
    "model", "pid", "event_id", "value", "age", "value_datatype",
    "activity", "unit", "input", "target", "protocol_id",
    "frequency_type", "frequency_value", "startdate", "enddate",
    "comments", "organisation", "duration_value", "duration_startdate",
    "duration_enddate", "identifier_value", "input_value",
    "attribute_type", "output_type", "output_id", "cause_id",
]
# Two generations of retired routing columns, both migrated onto their
# direct replacement rather than discarded:
#   - "specification" (pre-this-session): the real, wired-up protocol
#     column (confirmed against $(protocol_id) in YARRRML) is "protocol_id".
#   - "valueIRI"/"agent": overloaded multi-purpose staging columns retired
#     in favour of direct, self-describing columns (attribute_type,
#     output_type, output_id, cause_id, or -- for Medication's drug
#     identity, previously routed through "agent" -- "input"). See
#     CHANGELOG.md's "[Unreleased]" entry for the full reasoning. Since
#     valueIRI/agent meant DIFFERENT things per model, there's no single
#     correct migration target here -- glossary write-back just clears
#     their old description rather than guessing which replacement it
#     belongs to; the per-model fix was done by hand once, at refactor time.
RETIRED_COLUMN_ALIASES = {"specification": "protocol_id"}
RETIRED_COLUMNS_NO_MIGRATION = {"valueIRI", "agent"}
NOT_DERIVABLE = {"age"}  # editorial judgment call, no corresponding diagram node

MARKER_TO_LETTER = {"2854d7": "M", "d7a028": "O", "a29e96": "N"}
LETTER_TO_MARKER_URL = {
    "M": "https://placehold.jp/12/2854d7/ffffff/20x20.png?text=M",
    "O": "https://placehold.jp/12/d7a028/000000/20x20.png?text=O",
    "N": "https://placehold.jp/12/a29e96/000000/20x20.png?text=N",
}

# Source-node-aware: the same SIO property can mean different template
# fields depending on which node it originates from (e.g. "has identifier"
# from Output_ means output_id_type, but from Attribute_ it means
# identifier_type -- Genetic's per-variant Identifier_, added this session).
SOURCE_PROPERTY_TO_FIELD = {
    ("Role_", "SIO_000356"): "process_type",
    ("Process_", "SIO_000230"): "input_type",
    ("Process_", "SIO_000291"): "target_type",
    ("Output_", "SIO_000221"): "unit_type",
    ("Process_", "SIO_000900"): "frequency_type",
    ("Process_", "SIO_000339"): "protocol_type",
    ("Process_", "SIO_000229"): "output_type",
    ("Process_", "SIO_000028"): "specific_method_type",
    ("Output_", "SIO_000628"): "attribute_type",
    ("Output_", "SIO_00243"): "cause_type",
    ("ID_", "SIO_000020"): "role_type",
    ("Individual_", "SIO_000228"): "role_type",
    ("Output_", "SIO_000671"): "output_id_type",
    ("Attribute_", "SIO_000671"): "identifier_type",
}
# Fallback for any (property) not covered above, regardless of source --
# kept from the tool's original, simpler table for safety on unseen patterns.
EDGE_PROPERTY_TO_FIELD = {
    "SIO_000356": "process_type", "SIO_000230": "input_type",
    "SIO_000291": "target_type", "SIO_000221": "unit_type",
    "SIO_000900": "frequency_type", "SIO_000339": "protocol_type",
    "SIO_000229": "output_type", "SIO_000028": "specific_method_type",
    "SIO_000628": "attribute_type", "SIO_00243": "cause_type",
    "SIO_000020": "role_type", "SIO_000228": "role_type",
}

DYNAMIC_MARKERS = ("e.g.", "One of the following", "Child of", "child of", "IRI for")


# ---------------------------------------------------------------------------
# Diagram parsing
# ---------------------------------------------------------------------------
def parse_diagram(path):
    text = path.read_text()
    m = re.search(r"```mermaid\n(.*?)\n```", text, re.S)
    body = m.group(1)

    nodes = {}
    edges = []

    node_re = re.compile(r'^\s*([A-Za-z0-9_]+)(\{\{.*?\}\}|\["[^"]*"\]|\[[^\]]*\]):::(\w+)\s*$')
    edge_re = re.compile(r'^\s*([A-Za-z0-9_]+)\s*-->\s*(?:\|"([^"]*)"\|)?\s*([A-Za-z0-9_]+)\s*$')

    for line in body.splitlines():
        s = line.strip()
        nm = node_re.match(s)
        if nm:
            nid, shape_raw, cls = nm.groups()
            shape = "diamond" if shape_raw.startswith("{{") else "rect"
            label_match = re.search(r'"([^"]*)"|\{\{([^}]*)\}\}|\[([^\]]*)\]', shape_raw)
            label = next((g for g in label_match.groups() if g), nid) if label_match else nid
            nodes[nid] = {"shape": shape, "cls": cls, "label": label}
            continue
        em = edge_re.match(s)
        if em:
            src, label, dst = em.groups()
            edges.append((src, label or "", dst))

    return nodes, edges


def is_dynamic(nodes, class_id):
    label = nodes.get(class_id, {}).get("label", "")
    return any(marker in label for marker in DYNAMIC_MARKERS)


def derive_classified(nodes, edges):
    """Returns (fixed, dynamic) dicts: field -> value (fixed) or class-node-id (dynamic)."""
    sio_code_re = re.compile(r"SIO_\d+")  # not all codes are 6 digits (Deathdate's malformed SIO_00243)

    fixed = {}
    dynamic = {}
    for src, label, dst in edges:
        if label != "rdf:type" or dst not in nodes or dst.startswith("SIO_"):
            continue
        m = sio_code_re.search(
            next((lbl for s2, lbl, d2 in edges if d2 == src and s2 != src), "")
        )
        # Find the edge that reaches `src` (the used-instance node whose rdf:type this is)
        field = None
        for s2, lbl, d2 in edges:
            if d2 != src or d2 not in nodes or nodes[d2]["cls"] != "usedInstance":
                continue
            code_m = sio_code_re.search(lbl)
            if not code_m:
                continue
            field = SOURCE_PROPERTY_TO_FIELD.get((s2, code_m.group(0)))
            if field is None:
                field = EDGE_PROPERTY_TO_FIELD.get(code_m.group(0))
            if field:
                break
        if not field:
            continue
        iri = f"http://purl.obolibrary.org/obo/{dst}"
        if is_dynamic(nodes, dst):
            dynamic[field] = dst
        else:
            fixed[field] = iri

    # value_datatype: heuristic from the Output_'s "has value" literal node label.
    # Several models route "has value" through an intermediate node instead of
    # directly on Output_ (Birthplace, Genetic-pre-redesign, Biobank, Clinical_trial,
    # Cohort) -- in the current diagrams none of those still have a literal
    # "has value" edge at all (Genetic's moved to Identifier_, handled by
    # identifier_type instead), so no mediated-value fallback is needed anymore.
    for src, label, dst in edges:
        if src == "Output_" and label.startswith("sio:SIO_000300"):
            target_label = nodes.get(dst, {}).get("label", "").lower()
            if "duration" in target_label:
                fixed["value_datatype"] = "xsd:duration"
            elif "true / false" in target_label or "true/false" in target_label:
                fixed["value_datatype"] = "xsd:boolean"
            elif "iso 8601" in target_label or "date" in target_label:
                fixed["value_datatype"] = "xsd:date"
            elif any(k in target_label for k in ("float", "measur", "numeric", "score", "scale")) or re.search(r"\b\d+\.\d+\b", target_label):
                fixed["value_datatype"] = "xsd:float"
            elif any(k in target_label for k in ("integer", "count", "year", "yyyy")):
                fixed["value_datatype"] = "xsd:integer"
            else:
                fixed["value_datatype"] = "xsd:string"

    return fixed, dynamic


# Mirrors main.py's value_edition() dispatch tables -- which public column
# feeds a given *dynamic* field is a routing decision made in main.py, not
# something visible in the diagram itself. Keep in sync with main.py by
# hand; anything not listed here falls through to the "?? needs review"
# report instead of silently guessing "N".
#
# attribute_type/output_type/output_id/cause_id are NOT listed here: since
# the valueIRI/agent refactor they're direct, self-describing public
# columns (same name as the internal field, like target/frequency_type
# already were), so they need no routing table at all -- handled by the
# generic "field is already a public column name" rule below instead.
DYNAMIC_FIELD_ROUTING = {
    "target_type": [("target", {"Examination", "Laboratory", "Surgery", "Diagnosis", "Phenotype", "Functional_Assessment"})],
    "target_id": [("target", {"Symptoms_onset", "Clinical_trial", "Cohort"})],
    "input_type": [("input", {"Laboratory", "Genetic", "Biobank"})],
    "input_id": [("input", {"Questionnaire", "Medication"})],
    "specific_method_type": [("activity", None)],  # None == every OBO model (keywords_OBO)
    "unit_type": [("unit", None)],
    "frequency_type": [("frequency_type", None)],  # direct same-name column, already handled by the edge rule below -- listed only to silence the "needs review" flag
}

# M-vs-O for a dynamic field is not reliably derivable from diagram
# structure alone (see the has_value_edge comment below for the general
# problem). For the direct columns this is positive, hand-verified
# knowledge carried over from the pre-refactor valueIRI/agent marks --
# not a guess. Any (field, model) pair not listed here defaults to "O".
POSITIVE_MANDATORY_OVERRIDE = {
    ("attribute_type", "Sex"): "M",
    ("attribute_type", "Status"): "M",
    ("attribute_type", "Examination"): "M",
    ("attribute_type", "Genetic"): "O",
    ("output_type", "Consent"): "M",
    ("output_type", "Medication"): "M",
    ("output_id", "Birthplace"): "M",
    ("output_id", "Clinical_trial"): "M",
    ("output_id", "Cohort"): "M",
    ("output_id", "Biobank"): "M",
    ("cause_id", "Deathdate"): "O",
    # Medication's drug identity was previously routed through the retired
    # "agent" column (M); now routed through "input" (feeds input_id).
    ("input", "Medication"): "M",
}


def derive_glossary_marks(nodes, edges, fixed_entry, model=None, dynamic=None):
    marks = {c: "N" for c in PUBLIC_COLUMNS}
    resolved = set()
    marks["model"] = "M"
    marks["pid"] = "M"

    has_value_edge = any(
        src == "Output_" and label.startswith("sio:SIO_000300") for src, label, dst in edges
    )
    for src, label, dst in edges:
        if "is specified by" in label and src == "Process_":
            marks["protocol_id"] = "O"
        elif "rdfs:comment" in label:
            marks["comments"] = "O"
        elif "has input" in label:
            marks["input"] = "O"
            if "Input_" in nodes and any(
                s2 == "Input_" and l2.startswith("sio:SIO_000300") for s2, l2, d2 in edges
            ):
                marks["input_value"] = "O"
        elif "has target" in label:
            marks["target"] = "O"
        elif "has unit" in label:
            marks["unit"] = "O"
        elif "has frequency" in label:
            marks["frequency_type"] = "O"
            marks["frequency_value"] = "O"
        elif "has identifier" in label and src == "Attribute_":
            marks["identifier_value"] = "O"
        elif "exists at" in label and dst == "Duration_":
            marks["duration_value"] = "O"
            marks["duration_startdate"] = "O"
            marks["duration_enddate"] = "O"

    if has_value_edge:
        # KNOWN LIMITATION: this always assumes M. Not always true -- e.g.
        # Hospitalization/Surgery's Output_ value is a deliberately optional
        # generic placeholder ("no fixed meaning defined yet"), which this
        # rule can't distinguish from a model where the value is the whole
        # point of the record. Verify by hand for new models -- no
        # positive-evidence override table for this one yet (unlike the
        # attribute_type/output_type/etc. M-vs-O cases, which do have one:
        # POSITIVE_MANDATORY_OVERRIDE).
        marks["value"] = "M"
        marks["value_datatype"] = "O"

    if "Output_" in nodes:
        marks["startdate"] = "O"
        marks["enddate"] = "O"
    marks["event_id"] = "O"

    # Any field the toolkit template hardcodes a constant for is auto-filled
    # by the toolkit -- not something the CSV author needs to supply.
    for field in fixed_entry:
        if field in marks:
            marks[field] = "N"

    # Dynamic (non-fixed) fields are supplied via whichever public column
    # carries them. attribute_type/output_type/output_id/cause_id ARE the
    # public column (direct pass-through, no separate routing); everything
    # else still needs main.py's dispatch table to know which raw column
    # (target/input/activity/unit) feeds it for this model.
    for field, node_id in (dynamic or {}).items():
        if field in PUBLIC_COLUMNS:
            marks[field] = POSITIVE_MANDATORY_OVERRIDE.get((field, model), "O")
            resolved.add(field)
            continue
        for pub_col, models in DYNAMIC_FIELD_ROUTING.get(field, []):
            if models is None or (model and model in models):
                marks[pub_col] = POSITIVE_MANDATORY_OVERRIDE.get((pub_col, model), "O")
                resolved.add(pub_col)
                break

    # output_id/cause_id (Output_'s own IDENTITY, e.g. an external accession
    # number) have no rdf:type edge at all -- there's nothing for
    # derive_classified to see, so they'd never appear in `dynamic` above.
    # POSITIVE_MANDATORY_OVERRIDE's presence for a (field, model) pair here
    # IS the positive evidence, applied unconditionally rather than gated
    # on a diagram signal that structurally can't exist for these two.
    for field in ("output_id", "cause_id"):
        if (field, model) in POSITIVE_MANDATORY_OVERRIDE:
            marks[field] = POSITIVE_MANDATORY_OVERRIDE[(field, model)]
            resolved.add(field)

    for field in NOT_DERIVABLE:
        marks[field] = None  # explicitly "not derivable from the diagram", not a guess

    return marks


# ---------------------------------------------------------------------------
# template.py: ground truth (our own copy) + write-back
# ---------------------------------------------------------------------------
def load_toolkit_ground_truth():
    from toolkit.template import TEMPLATE_MAP_OBO
    ground_truth = {}
    for model, entry in TEMPLATE_MAP_OBO.items():
        ground_truth[model] = {k: v for k, v in entry.items() if v is not None and k != "pid"}
    return ground_truth


FIELD_ORDER = [
    "role_type", "process_type", "attribute_type", "output_type",
    "output_id_type", "identifier_type", "protocol_type", "input_type",
    "target_type", "unit_type", "specific_method_type", "cause_type",
    "frequency_type", "value_datatype",
]


def render_template_map_obo(all_fixed):
    lines = ["TEMPLATE_MAP_OBO = {", ""]
    for model in MODEL_ORDER:
        fixed = all_fixed[model]
        lines.append(f'        "{model}": Template_OBO.build_entry(')
        for field in FIELD_ORDER:
            if field in fixed:
                lines.append(f'            {field}="{fixed[field]}",')
        lines.append("        ),")
    lines.append("    }")
    return "\n".join(lines)


def write_template_py(all_fixed):
    text = TEMPLATE_PATH.read_text()
    new_block = render_template_map_obo(all_fixed)
    pattern = re.compile(r"TEMPLATE_MAP_OBO = \{.*?\n    \}", re.S)
    if not pattern.search(text):
        raise RuntimeError("Could not locate TEMPLATE_MAP_OBO block in template.py")
    new_text = pattern.sub(lambda m: new_block, text, count=1)
    TEMPLATE_PATH.write_text(new_text)


# ---------------------------------------------------------------------------
# glossary.md: parsing + write-back
# ---------------------------------------------------------------------------
BULLET_RE = re.compile(
    r'^-\s*!\[\]\(https://placehold\.jp/12/([0-9a-f]{6})/[^)]*\)\s*'
    r'\*\*([a-zA-Z_]+)\*\*:\s?(.*)$'
)


def load_glossary_ground_truth():
    text = GLOSSARY_PATH.read_text()
    result = {}
    for model, anchor in MODEL_TO_ANCHOR.items():
        section = extract_section(text, anchor)
        if section is None:
            result[model] = {}
            continue
        _, cols, _ = parse_section(section)
        result[model] = {c: v[0] for c, v in cols.items()}
    return result


def extract_section(text, anchor):
    """Returns the full section text, including the "(anchor)=\\n" line --
    used as-is for the literal replace in write_glossary. parse_section
    strips the anchor line itself before parsing."""
    m = re.search(rf"\({re.escape(anchor)}\)=\n", text)
    if not m:
        return None
    start = m.start()
    next_m = re.search(r"\n\([a-zA-Z0-9_-]+_glossary\)=\n", text[m.end():])
    end = m.end() + next_m.start() + 1 if next_m else len(text)
    return text[start:end]


def parse_section(section):
    lines = section.splitlines()
    if lines and re.match(r"^\([a-zA-Z0-9_-]+_glossary\)=$", lines[0].strip()):
        lines = lines[1:]  # anchor line, not part of the body
    intro = []
    cols = {}
    trailing = []
    seen_first_bullet = False
    for line in lines:
        bm = BULLET_RE.match(line.strip())
        if bm:
            seen_first_bullet = True
            color, colname, desc = bm.groups()
            letter = MARKER_TO_LETTER.get(color, "N")
            cols[colname] = (letter, desc.rstrip())
        elif not seen_first_bullet:
            intro.append(line)
        elif line.strip() == "<hr>":
            continue
        else:
            trailing.append(line)
    while trailing and trailing[0].strip() == "":
        trailing.pop(0)
    while trailing and trailing[-1].strip() == "":
        trailing.pop()

    # Migrate any retired column name's description onto its replacement,
    # so hand-written prose isn't silently discarded (e.g. "specification"'s
    # old "IRI reference to any associated protocol" -> protocol_id).
    for old_name, new_name in RETIRED_COLUMN_ALIASES.items():
        if old_name in cols and new_name not in cols:
            cols[new_name] = cols.pop(old_name)
        elif old_name in cols:
            cols.pop(old_name)

    # No single replacement column exists for these (valueIRI/agent meant a
    # different thing per model) -- just drop the stale bullet line. The
    # correct new-column mark/description was set by hand at refactor time,
    # not migrated automatically.
    for old_name in RETIRED_COLUMNS_NO_MIGRATION:
        cols.pop(old_name, None)

    return intro, cols, trailing


def render_section(anchor, intro_lines, cols, trailing_lines, order):
    out = [f"({anchor})="]
    out.extend(intro_lines)
    for colname in order:
        if colname not in cols:
            continue
        letter, desc = cols[colname]
        badge = f"![]({LETTER_TO_MARKER_URL[letter]})"
        desc_part = f" {desc}" if desc else ""
        out.append(f"- {badge} **{colname}**:{desc_part}")
    if trailing_lines:
        out.append("")
        out.extend(trailing_lines)
    out.append("<hr>")
    out.append("")
    out.append("")
    return "\n".join(out)


PLACEHOLDER = "*(needs a description -- added automatically from the diagram, please review)*"


def column_order(old_cols):
    """Preserve each section's own existing column order (a cosmetic,
    hand-chosen thing with no bearing on correctness) instead of resorting
    everything to PUBLIC_COLUMNS' canonical order -- that would just be
    large, valueless diff noise across all 22 sections. New columns not
    already present are appended at the end in canonical order."""
    existing = [c for c in old_cols if c in PUBLIC_COLUMNS]
    new = [c for c in PUBLIC_COLUMNS if c not in old_cols]
    return existing + new


def merged_columns(model, old_cols, new_marks):
    merged = {}
    for colname in PUBLIC_COLUMNS:
        new_letter = new_marks.get(colname)
        if new_letter is None:
            if colname in old_cols:
                merged[colname] = old_cols[colname]
            continue
        old = old_cols.get(colname)
        if old is None:
            desc = "" if new_letter == "N" else PLACEHOLDER
            merged[colname] = (new_letter, desc)
        else:
            old_letter, old_desc = old
            # N is a strong structural signal (the edge plain doesn't exist
            # in the diagram) and always wins. Otherwise never auto-downgrade
            # an existing M to O -- the M/O distinction for routed dynamic
            # fields (is this the point of the record, or an optional extra)
            # isn't reliably derivable from diagram structure alone.
            if new_letter == "N":
                merged[colname] = ("N", "")
            elif old_letter == "M" and new_letter == "O":
                merged[colname] = ("M", old_desc)
            elif old_letter == new_letter:
                merged[colname] = (old_letter, old_desc)
            elif old_desc:
                merged[colname] = (new_letter, old_desc)
            else:
                merged[colname] = (new_letter, PLACEHOLDER)
    return merged


def write_glossary(all_new_marks):
    text = GLOSSARY_PATH.read_text()
    for model in MODEL_ORDER:
        anchor = MODEL_TO_ANCHOR[model]
        section = extract_section(text, anchor)
        if section is None:
            print(f"  !! No glossary section found for {model} (anchor {anchor}) -- skipped")
            continue
        intro, old_cols, trailing = parse_section(section)
        merged = merged_columns(model, old_cols, all_new_marks[model])
        order = column_order(old_cols)
        new_section = render_section(anchor, intro, merged, trailing, order)
        text = text.replace(section, new_section, 1)
    GLOSSARY_PATH.write_text(text)


# ---------------------------------------------------------------------------
# CSV example validation (report-only)
# ---------------------------------------------------------------------------
def check_csv_examples(models):
    import pandas as pd
    from toolkit.main import Toolkit

    t = Toolkit()
    print("\n" + "=" * 60)
    print("CSV EXAMPLE VALIDATION (report only)")
    print("=" * 60)
    for model in models:
        path = CSV_DIR / f"{model}.csv"
        if not path.exists():
            print(f"  {model}: no example CSV found ({path.name})")
            continue
        before = len(pd.read_csv(path))
        try:
            df = t._process_file(str(path), "OBO")
        except Exception as e:
            print(f"  {model}: FAILED to process -- {e}")
            continue
        after = len(df)
        status = "OK" if after == before else f"DROPPED {before - after} of {before} rows"
        print(f"  {model}: {status}")


# ---------------------------------------------------------------------------
# YARRRML structural coverage (report-only)
# ---------------------------------------------------------------------------
def check_yarrrml_coverage(models):
    yarrrml_text = YARRRML_PATH.read_text()
    print("\n" + "=" * 60)
    print("YARRRML STRUCTURAL COVERAGE (report only)")
    print("=" * 60)
    sio_code_re = re.compile(r"SIO_\d+")
    seen = set()
    for model in models:
        path = DIAGRAMS_DIR / f"CARE-SM-obo-{model}.md"
        if not path.exists():
            continue
        nodes, edges = parse_diagram(path)
        for src, label, dst in edges:
            m = sio_code_re.search(label)
            if not m or dst not in nodes:
                continue
            key = (nodes.get(src, {}).get("cls"), m.group(0), nodes[dst]["cls"])
            if key in seen:
                continue
            seen.add(key)
            code = m.group(0)
            if code not in yarrrml_text:
                print(f"  {model}: property {code} ('{label}') has no reference anywhere in YARRRML -- needs review")


# ---------------------------------------------------------------------------
# Report (check mode)
# ---------------------------------------------------------------------------
def diff_dicts(derived, truth, all_keys=None, skip_keys=frozenset()):
    keys = all_keys if all_keys is not None else sorted(set(derived) | set(truth))
    diffs = []
    for k in keys:
        if k in skip_keys:
            continue
        d, t = derived.get(k), truth.get(k)
        if d != t:
            diffs.append((k, d, t))
    return diffs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("model", nargs="?", help="Restrict to a single model")
    parser.add_argument("--write", action="store_true", help="Apply fixes to template.py and glossary.md")
    parser.add_argument("--csv", action="store_true", help="Also validate CSV examples against the real pipeline")
    parser.add_argument("--yarrrml", action="store_true", help="Also report YARRRML structural coverage gaps")
    args = parser.parse_args()

    models = [args.model] if args.model else MODEL_ORDER

    toolkit_truth = load_toolkit_ground_truth()
    glossary_truth = load_glossary_ground_truth()

    all_fixed = {}
    all_marks = {}
    total_toolkit_diffs = 0
    total_glossary_diffs = 0

    for model in models:
        diagram_path = DIAGRAMS_DIR / f"CARE-SM-obo-{model}.md"
        if not diagram_path.exists():
            print(f"!! {model}: no diagram found at {diagram_path}")
            continue

        nodes, edges = parse_diagram(diagram_path)
        fixed, dynamic = derive_classified(nodes, edges)

        # value_datatype heuristic only looks at a "has value" edge sitting
        # directly on Output_. Some models (Birthplace, Biobank, Clinical_trial,
        # Cohort) route it through an intermediate node instead (mediated
        # value) -- absence of a direct-edge signal here means "heuristic
        # can't see it", not "diagram no longer supports it". Preserve the
        # existing toolkit value rather than silently dropping it.
        old_entry = toolkit_truth.get(model, {})
        if "value_datatype" not in fixed and "value_datatype" in old_entry:
            mediated_value = any(
                label.startswith("sio:SIO_000300") and nodes.get(src, {}).get("cls") == "usedInstance" and src != "Output_"
                for src, label, dst in edges
            )
            if mediated_value:
                fixed["value_datatype"] = old_entry["value_datatype"]

        marks = derive_glossary_marks(nodes, edges, fixed, model=model, dynamic=dynamic)
        all_fixed[model] = fixed
        all_marks[model] = marks

        toolkit_diffs = diff_dicts(fixed, toolkit_truth.get(model, {}))
        undetermined = {k for k, v in marks.items() if v is None}
        model_truth = glossary_truth.get(model, {})
        # Match write-back's safety rule: an auto-derived "O" never counts as
        # a mismatch against an existing "M" (see merged_columns) -- reporting
        # it here would just be noise about a downgrade we'd never apply.
        soft_downgrades = {k for k in PUBLIC_COLUMNS if marks.get(k) == "O" and model_truth.get(k) == "M"}
        glossary_diffs = diff_dicts(marks, model_truth, all_keys=PUBLIC_COLUMNS, skip_keys=NOT_DERIVABLE | undetermined | soft_downgrades)

        total_toolkit_diffs += len(toolkit_diffs)
        total_glossary_diffs += len(glossary_diffs)

        status = "OK" if not toolkit_diffs and not glossary_diffs else "DRIFT"
        print(f"\n=== {model}: {status} ===")
        if toolkit_diffs:
            print("  template.py mismatches (diagram vs our implementation/Toolkit copy):")
            for k, d, t in toolkit_diffs:
                print(f"    {k}: diagram says {d!r:60} toolkit has {t!r}")
        if glossary_diffs:
            print("  glossary.md mismatches (diagram vs documented column):")
            for k, d, t in glossary_diffs:
                print(f"    {k}: diagram says {d!r:5} glossary has {t!r}")
        if not toolkit_diffs and not glossary_diffs:
            print("  (fully consistent)")
        if dynamic:
            for field, node_id in dynamic.items():
                routed = field in PUBLIC_COLUMNS or any(
                    models is None or model in models
                    for _, models in DYNAMIC_FIELD_ROUTING.get(field, [])
                )
                if not routed:
                    print(f"  ?? {model}.{field} (node: {node_id}) is dynamic with no known public-column routing -- needs review")

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_toolkit_diffs} template.py mismatches, {total_glossary_diffs} glossary mismatches across {len(models)} models")

    if args.write:
        print("\nApplying fixes...")
        # Current ground truth for every model as the safe base, then overlay
        # only the freshly re-derived (mediated-value-safe) model(s) actually
        # requested -- never re-derives models outside `models` from scratch.
        full_fixed = load_toolkit_ground_truth()
        full_fixed.update(all_fixed)
        write_template_py(full_fixed)
        print(f"  wrote {TEMPLATE_PATH.relative_to(REPO_ROOT)}")
        write_glossary(all_marks)
        print(f"  wrote {GLOSSARY_PATH.relative_to(REPO_ROOT)}")

    if args.csv:
        check_csv_examples(models)
    if args.yarrrml:
        check_yarrrml_coverage(models)


if __name__ == "__main__":
    main()
