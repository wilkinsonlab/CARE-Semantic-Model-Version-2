#!/usr/bin/env python3
"""
Prototype sync-checker for CARE-SM Version 2.

Parses each model's Mermaid diagram (the source of truth, per project
decision) and mechanically derives:
  1. The per-model ontology lookup that CARE-SM-Toolkit's
     `toolkit/template.py` needs (TEMPLATE_MAP_OBO entries).
  2. The Mandatory/Optional/N-A column marks that `docs/glossary.md`
     documents for that model.

It then diffs those derived values against the real, currently-installed
`care-sm-toolkit` package and the real `docs/glossary.md`, to surface
drift between the diagram and the two hand-maintained artifacts.

This does NOT generate CARE.csv (a Toolkit-generated output, not something
to hand-author) and does NOT touch YARRRML (generic across all models,
only needs edits for genuinely new structural patterns not yet supported).

Usage:
    python3 tools/diagram_sync.py                  # full report, all models
    python3 tools/diagram_sync.py Birthdate         # single model
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = REPO_ROOT / "diagrams"
GLOSSARY_PATH = REPO_ROOT / "docs" / "glossary.md"

# ---------------------------------------------------------------------------
# Diagram <-> glossary section order. Glossary heading text doesn't always
# match the model tag string exactly (e.g. "First Confirmed Visit" heading
# vs "First_visit" tag), so sections are matched by their fixed document
# order, verified by hand against docs/glossary.md.
# ---------------------------------------------------------------------------
MODEL_ORDER = [
    "Birthdate", "Birthyear", "Birthplace", "Deathdate", "Sex",
    "First_visit", "Status", "Symptoms_onset", "Phenotype", "Diagnosis",
    "Examination", "Laboratory", "Genetic", "Medication", "Hospitalization",
    "Surgery", "Questionnaire", "Functional_Assessment", "Biobank", "Consent",
    "Clinical_trial", "Cohort",
]
# NOTE: "Functional_Assessment" was renamed from "Disability" on the diagram
# side only (docs/glossary.md and the installed toolkit's TEMPLATE_MAP_OBO
# still use the old "Disability" key/section) -- kept at the same position in
# this list so the positional glossary-section zip still lines up correctly.
# Expect full drift on this model in both toolkit and glossary comparisons
# until that rename propagates downstream.

# Property connecting a used-instance node to its parent hub is stable
# across diagrams even when the node's own label is model-specific
# (e.g. Medication's "input" role is drawn as "URI for drug identifier").
EDGE_PROPERTY_TO_FIELD = {
    "SIO_000356": "process_type",          # is realized in     (Role_ -> Process_)
    "SIO_000230": "input_type",            # has input
    "SIO_000291": "target_type",           # has target
    "SIO_000221": "unit_type",             # has unit
    "SIO_000900": "frequency_type",        # has frequency
    "SIO_000339": "protocol_type",         # is specified by
    "SIO_000229": "output_type",           # has output
    "SIO_000028": "specific_method_type",  # has part
    "SIO_000628": "attribute_type",        # refers to
    "SIO_00243":  "cause_type",            # is causally related with
    "SIO_000020": "role_type",             # denotes            (ID_ -> Role_)
    "SIO_000228": "role_type",             # has role           (Individual_ -> Role_)
    "SIO_000671": "output_id_type",        # has identifier
}

PUBLIC_COLUMNS = [
    "model", "pid", "event_id", "value", "age", "value_datatype", "valueIRI",
    "activity", "unit", "input", "target", "specification", "frequency_type",
    "frequency_value", "agent", "startdate", "enddate", "comments", "organisation",
]

MARKER_TO_LETTER = {"2854d7": "M", "d7a028": "O", "a29e96": "N"}


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


def derive_toolkit_entry(nodes, edges):
    sio_code_re = re.compile(r"SIO_\d{6}")

    node_to_field = {}
    for src, label, dst in edges:
        if dst not in nodes or nodes[dst]["cls"] != "usedInstance":
            continue
        m = sio_code_re.search(label)
        if not m:
            continue
        field = EDGE_PROPERTY_TO_FIELD.get(m.group(0))
        if field:
            node_to_field[dst] = field

    entry = {}
    for src, label, dst in edges:
        if label != "rdf:type" or src not in node_to_field:
            continue
        if dst not in nodes or dst.startswith("SIO_"):
            continue  # generic/universal classes, already hardcoded in shared YARRRML
        entry[node_to_field[src]] = f"http://purl.obolibrary.org/obo/{dst}"

    # value_datatype: heuristic from the Output_'s "has value" literal node label
    for src, label, dst in edges:
        if src == "Output_" and label.startswith("sio:SIO_000300"):
            target_label = nodes.get(dst, {}).get("label", "").lower()
            if "duration" in target_label:
                entry["value_datatype"] = "xsd:duration"
            elif "iso 8601" in target_label or "date" in target_label:
                entry["value_datatype"] = "xsd:date"
            elif (
                "float" in target_label or "measur" in target_label
                or "numeric" in target_label or "score" in target_label
                or "scale" in target_label
                or re.search(r"\b\d+\.\d+\b", target_label)  # e.g. "e.g. 10.5"
            ):
                entry["value_datatype"] = "xsd:float"
            elif "integer" in target_label or "count" in target_label:
                entry["value_datatype"] = "xsd:integer"
            else:
                entry["value_datatype"] = "xsd:string"
    return entry


NOT_DERIVABLE = {"age"}  # editorial judgment calls with no corresponding diagram node


def derive_glossary_marks(nodes, edges, entry):
    marks = {c: "N" for c in PUBLIC_COLUMNS}
    marks["model"] = "M"
    marks["pid"] = "M"

    has_value_edge = False
    for src, label, dst in edges:
        if src == "Output_" and label.startswith("sio:SIO_000300"):
            has_value_edge = True
        elif "is specified by" in label:
            marks["specification"] = "O"
        elif "rdfs:comment" in label:
            marks["comments"] = "O"
        elif "has input" in label:
            marks["input"] = "O"
        elif "has target" in label:
            marks["target"] = "O"
        elif "has unit" in label:
            marks["unit"] = "O"
        elif "has frequency" in label:
            marks["frequency_type"] = "O"
            marks["frequency_value"] = "O"

    if has_value_edge:
        marks["value"] = "M"
        marks["value_datatype"] = "O"

    if "Output_" in nodes:
        marks["startdate"] = "O"
        marks["enddate"] = "O"
    marks["event_id"] = "O"

    # any column the toolkit template hardcodes a default for is auto-filled
    # by the toolkit -> not something the CSV author needs to supply
    for field in entry:
        if field in marks:
            marks[field] = "N"

    for field in NOT_DERIVABLE:
        marks[field] = None  # explicitly "not derivable from the diagram" rather than a guess

    return marks


# ---------------------------------------------------------------------------
# Ground truth: installed toolkit + glossary.md
# ---------------------------------------------------------------------------
def load_toolkit_ground_truth():
    from toolkit.template import TEMPLATE_MAP_OBO
    ground_truth = {}
    for model, entry in TEMPLATE_MAP_OBO.items():
        ground_truth[model] = {k: v for k, v in entry.items() if v is not None and k != "pid"}
    return ground_truth


def load_glossary_ground_truth():
    text = GLOSSARY_PATH.read_text()
    sections = re.split(r"\n<hr>\n", text)
    field_re = re.compile(r"!\[\]\(https://placehold\.jp/12/([0-9a-f]{6})/[^)]*\)\s*\*\*([a-zA-Z_]+)\*\*")

    parsed_sections = []
    for section in sections:
        if "_glossary)=" not in section:
            continue
        marks = {}
        for color, field in field_re.findall(section):
            letter = MARKER_TO_LETTER.get(color)
            if letter:
                marks[field] = letter
        parsed_sections.append(marks)

    return dict(zip(MODEL_ORDER, parsed_sections))


# ---------------------------------------------------------------------------
# Report
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
    only = sys.argv[1] if len(sys.argv) > 1 else None
    models = [only] if only else MODEL_ORDER

    toolkit_truth = load_toolkit_ground_truth()
    glossary_truth = load_glossary_ground_truth()

    total_toolkit_diffs = 0
    total_glossary_diffs = 0

    for model in models:
        diagram_path = DIAGRAMS_DIR / f"CARE-SM-obo-{model}.md"
        if not diagram_path.exists():
            print(f"!! {model}: no diagram found at {diagram_path}")
            continue

        nodes, edges = parse_diagram(diagram_path)
        derived_entry = derive_toolkit_entry(nodes, edges)
        derived_marks = derive_glossary_marks(nodes, edges, derived_entry)

        toolkit_diffs = diff_dicts(derived_entry, toolkit_truth.get(model, {}))
        glossary_diffs = diff_dicts(
            derived_marks, glossary_truth.get(model, {}),
            all_keys=PUBLIC_COLUMNS, skip_keys=NOT_DERIVABLE,
        )

        total_toolkit_diffs += len(toolkit_diffs)
        total_glossary_diffs += len(glossary_diffs)

        status = "OK" if not toolkit_diffs and not glossary_diffs else "DRIFT"
        print(f"\n=== {model}: {status} ===")

        if toolkit_diffs:
            print("  toolkit/template.py mismatches (diagram vs installed toolkit):")
            for k, d, t in toolkit_diffs:
                print(f"    {k}: diagram says {d!r:60} toolkit has {t!r}")
        if glossary_diffs:
            print("  glossary.md mismatches (diagram vs documented column):")
            for k, d, t in glossary_diffs:
                print(f"    {k}: diagram says {d!r:5} glossary has {t!r}")
        if not toolkit_diffs and not glossary_diffs:
            print("  (fully consistent)")

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_toolkit_diffs} toolkit field mismatches, "
          f"{total_glossary_diffs} glossary column mismatches across {len(models)} models")


if __name__ == "__main__":
    main()
