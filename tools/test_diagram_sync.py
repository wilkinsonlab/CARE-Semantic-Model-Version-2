"""Regression tests for tools/diagram_sync.py.

Run with: python3 -m pytest tools/test_diagram_sync.py
"""
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("diagram_sync", REPO_ROOT / "tools" / "diagram_sync.py")
diagram_sync = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(diagram_sync)


def test_write_glossary_requires_marks_for_every_model(tmp_path, monkeypatch):
    """`--write <model>` scopes derivation to one model, but write_glossary()
    rewrites the WHOLE glossary.md file (one shared file, every model's
    section) in a single pass, so it needs marks for every model in
    MODEL_ORDER, not just the requested one.

    Bug (2026-09-23): main() called `write_glossary(all_marks)` directly,
    where `all_marks` only contained the model(s) `--write` was scoped to.
    Any OTHER model hit `all_new_marks[model]` with no fallback and raised
    KeyError, crashing `--write <one-model>` entirely (discovered running
    `--write Genetic`, which is otherwise unrelated to the models it
    crashed on, e.g. Birthdate). Fixed by overlaying the requested model(s)'
    freshly-derived marks onto load_glossary_ground_truth()'s full set
    before calling write_glossary() -- the same pattern write_template_py()
    already used correctly.
    """
    tmp_glossary = tmp_path / "glossary.md"
    tmp_glossary.write_text(diagram_sync.GLOSSARY_PATH.read_text())
    monkeypatch.setattr(diagram_sync, "GLOSSARY_PATH", tmp_glossary)

    full_marks = diagram_sync.load_glossary_ground_truth()
    assert len(full_marks) == len(diagram_sync.MODEL_ORDER)

    # Simulates `--write Genetic`: only Genetic's marks were freshly
    # re-derived from the diagram this run; every other model is untouched.
    # Uses target="M" specifically (not "O"): merged_columns() has its own
    # separate safety rule that refuses to let an auto-derived "O" downgrade
    # an existing hand-verified "M" already in glossary.md, so "O" would
    # make this test's outcome depend on the live repo's current mark
    # instead of on the overlay fix being tested here.
    partial_marks = {"Genetic": dict(full_marks["Genetic"], target="M")}

    # Pin the bug: calling write_glossary with ONLY the requested model's
    # marks must fail exactly as it did before the fix -- if this stops
    # raising, the KeyError guard this test exists to document is gone and
    # the test itself needs re-evaluating, not silently deleting.
    with pytest.raises(KeyError):
        diagram_sync.write_glossary(dict(partial_marks))

    # The actual fix: overlay onto the full ground truth first (main()'s
    # call-site pattern), which must succeed and must not touch models
    # outside the requested set.
    overlaid = dict(full_marks)
    overlaid.update(partial_marks)
    diagram_sync.write_glossary(overlaid)  # must not raise

    written_marks = diagram_sync.load_glossary_ground_truth()
    assert written_marks["Genetic"]["target"] == "M"
    other_model = next(m for m in diagram_sync.MODEL_ORDER if m != "Genetic")
    assert written_marks[other_model] == full_marks[other_model]


def _derived_marks(model):
    """Glossary marks derived from a model's diagram exactly as main() does
    (including its mediated-value value_datatype preservation)."""
    nodes, edges = diagram_sync.parse_diagram(diagram_sync.DIAGRAMS_DIR / f"CARE-SM-obo-{model}.md")
    fixed, dynamic = diagram_sync.derive_classified(nodes, edges)
    old_entry = diagram_sync.load_toolkit_ground_truth().get(model, {})
    if "value_datatype" not in fixed and "value_datatype" in old_entry:
        fixed["value_datatype"] = old_entry["value_datatype"]
    return diagram_sync.derive_glossary_marks(nodes, edges, fixed, model=model, dynamic=dynamic)


@pytest.mark.parametrize("model", ["Birthdate", "Sex", "Symptoms_onset", "Phenotype", "Biobank"])
def test_value_datatype_is_optional_wherever_value_applies(model):
    """GitHub issue #3: the template's value_datatype is only a per-model
    default that a CSV value_datatype overrides, so it must not be marked
    N/A just because template.py fills it. Previously every model came out
    N, contradicting the exemplar CSVs (and Symptoms_onset genuinely needs
    the override: date of onset OR age of onset)."""
    marks = _derived_marks(model)
    assert marks["value"] in ("M", "O")
    assert marks["value_datatype"] == "O"


def test_value_datatype_stays_na_without_value():
    """Genetic has no Output_ value at all (its literal is identifier_value)."""
    marks = _derived_marks("Genetic")
    assert marks["value"] == "N"
    assert marks["value_datatype"] == "N"


@pytest.mark.parametrize("model", ["Birthplace", "Biobank", "Clinical_trial", "Cohort"])
def test_mediated_value_through_output_identifier_is_optional(model):
    """GitHub issue #3 follow-up: for these models `value` reaches the RDF
    via Output_ --has identifier--> X --has value--> literal (main.py routes
    it to value_id_string), so it's a real CSV column, not N/A."""
    assert _derived_marks(model)["value"] == "O"


@pytest.mark.parametrize("model", ["Hospitalization", "Surgery"])
def test_placeholder_output_value_is_optional(model):
    """These models' Output_ value is a deliberately optional free-form
    placeholder; the generic has-value rule must not force it to M."""
    assert _derived_marks(model)["value"] == "O"


def test_glossary_csv_mismatches_flags_missing_mandatory_and_filled_na():
    """The --csv check must catch exactly the issue #3 discrepancies: a
    Mandatory column left empty (Sex.value) and an N/A column filled."""
    import pandas as pd

    raw = pd.DataFrame({"model": ["Sex", "Sex"], "pid": ["1", "2"],
                        "attribute_type": ["http://x", "http://y"],
                        "unit": [None, "http://z"]})
    marks = {"model": "M", "pid": "M", "value": "M", "attribute_type": "M", "unit": "N"}
    problems = diagram_sync.glossary_csv_mismatches(raw, marks)
    assert any("'value' is Mandatory" in p for p in problems)
    assert any("'unit' is N/A" in p for p in problems)
    assert len(problems) == 2

    raw["value"] = ["Female", "Male"]
    raw["unit"] = None
    assert diagram_sync.glossary_csv_mismatches(raw, marks) == []
