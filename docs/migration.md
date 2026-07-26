# Migrating from CARE-SM v1

This page tracks every semantic difference between the original CARE-SM (v1, Pablo Alarcón-Moreno's model) and this harmonized version (v2), so that anyone migrating existing data or tooling knows what changed and why. It is **not** a full changelog of documentation/presentation work (diagram styling, font sizes, etc.) — only changes that affect the RDF a model produces or the CSV columns it expects.

This is a living document — v2 is still under active harmonization, so expect it to grow.

## Cross-cutting changes (apply to more than one model)

### `Attribute_` now has three different cardinalities, not one

In v1, `Output_ --refers to--> Attribute_` was always exactly one unconditional assertion per record. In v2 that same pattern is used three different ways depending on the model, and it's important to know which one a given model uses:

| Behavior | Models | What it means |
| --- | --- | --- |
| **Unconditional** (same as v1) | Birthdate, Birthyear, Deathdate, Birthplace, Sex, First_visit, Status, Symptoms_onset, Consent, Examination | `Attribute_` is always emitted, once, describing a fixed property of the record. |
| **Conditional** (new in v2) | Phenotype, Diagnosis | `Attribute_` is emitted **only** when the record's boolean result is `true`. A `false` result is still fully recorded (see below) but does not produce an `Attribute_` triple. |
| **Multi-valued / repeating** (new in v2) | Genetic | `Output_ --refers to--> Attribute_` can now repeat: one `Attribute_` instance per sequence variant, each carrying its own zygosity type and its own identifying notation. v1 only allowed one identifier per report. |

### Negative observations are now representable (new capability)

v1 had no way to record "tested for X, confirmed absent" — only positive findings could be asserted. Phenotype and Diagnosis now support this via:

- `Process_ --has target--> Target_` — records *what* was tested/assessed (a phenotype or diagnosis code), independent of the result.
- `Output_ --has value--> true/false` — the boolean result.
- `Output_ --refers to--> Attribute_` — only asserted when the value is `true` (see the conditional row above).

A `false` result is now a fully valid, queryable fact — it was previously simply not recordable.

### Coded-value identifier nodes are now bnodes, not implied-URI nodes

v1 sometimes modeled a coded value (a phenotype code, disease code, country code, etc.) via `Output_ --has identifier--> <code node>`, where that node's own identity was, in practice, derived from the code value itself. Since many unrelated patient records can share the same code (e.g. the same phenotype, the same country), this risked those records' subgraphs merging together at the identifier node — a real problem at scale.

v2 makes this node an explicit bnode (`Identifier_`), with the code stored as a **literal** `has value`, plus an optional `rdfs:label` carrying the human-readable name (e.g. the country or diagnosis name that was previously — inconsistently — attached via `has value` directly).

Affected models: **Phenotype, Diagnosis, Birthplace, Genetic**.

### Duration is no longer modeled as a patient `Attribute_`

v1 sometimes represented a time interval via `Output_ --refers to--> Attribute_`, with that `Attribute_` typed as *both* `sio:Attribute` and a Duration class. This is a category error — a duration isn't an attribute of the patient — and SIO durations don't have their own `has value` in the first place (only start/end times).

v2 uses `Output_ --exists at--> Duration_`, with `Duration_` typed only as `obo:NCIT_C217011` (Duration Quantity Value) + `sio:SIO_000417` (time interval), carrying `has start time`/`has end time` and no value.

Affected models: **Phenotype, Disability/Functional Assessment**; added fresh to **Diagnosis**, which previously had no duration concept at all.

### Node naming is now consistent across models

v1 used bespoke, domain-specific node names for structurally identical roles — e.g. `IRIGeneticDisease`, `URITreatmentPlan`, `URIDrugIdentifier`, `IRIConditionCode`, `IRIQuestionCode`. v2 uses the same generic node name for the same structural role everywhere (`Target_` for anything reached via `has target`, `Input_` for `has input`, `URIProtocol` for `is specified by`, `Causality_` for `is causally related with`), with the domain-specific detail living only in the class label. This does not change the RDF produced (node names are internal diagram labels, not published URIs) — it only makes the diagrams easier to compare model-to-model.

## Per-model changes

| Model | What changed |
| --- | --- |
| **Phenotype** | Negative-observation support added (`Target_` + boolean `Output_` value + conditional `Attribute_`). Duration fixed (`exists at`, no value). Identifier fixed (bnode `Identifier_` + optional label). |
| **Diagnosis** | Same three fixes as Phenotype, applied fresh. Added optional `Process_ --has input--> Input_` as an evidentiary-provenance placeholder — deliberately left as an empty, untyped-beyond-`information content entity` bnode; see the note in the diagram file for why it isn't populated. |
| **Disability → Functional Assessment** (renamed) | Moved from "Patient-reported outcomes" to "Clinical and molecular measurements". `Target_` (the metric/instrument being used, e.g. WHODAS) split out from `URIProtocol` (the exact administration protocol) — v1 conflated these into one node. Added an optional, Toolkit-resolved human-readable label on `Output_`. Duration fixed (`exists at`, no value). |
| **Genetic** | `has identifier` moved from `Output_` to `Attribute_` — a sequence variant report can now describe multiple variants (one `Attribute_`/`Identifier_` pair each) instead of being limited to a single identifier per report. |
| **Birthplace** | Identifier fixed (bnode); country name moved to an optional label. |
| **Consent** | Added optional `Process_ --has input--> Input_`, typed `obo:NCIT_C16468` (Consent Form), carrying a filename + version string (deliberately **not** a URL — most real-world consent forms won't have one). |
| **Hospitalization, Surgery** | Added a missing `Output_`/`Duration_` branch. v1 had no way to record any dates or result at all for these two models, despite the glossary documenting `startdate`/`enddate` as available (Optional) columns — filling those columns in previously had nowhere to go in the RDF. |
| **Clinical_trial, Cohort, Medication, Deathdate, Questionnaire, Symptoms_onset** | Node(s) renamed for cross-model consistency only (see above) — no change to the RDF produced. |

## Not yet migrated

Everything above is diagram-level (Mermaid source) work — these changes have **not** yet been propagated to the CARE-SM Toolkit, YARRRML mapping, glossary CSV-column documentation, or example CSVs. Until that propagation happens, generating RDF from real data with the current Toolkit will not reflect these fixes. `tools/diagram_sync.py` in this repository tracks exactly where the diagrams and the installed Toolkit currently disagree, model by model.
