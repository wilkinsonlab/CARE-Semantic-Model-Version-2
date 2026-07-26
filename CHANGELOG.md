# Changelog

All notable changes to this project are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

This is the first tagged release of CARE-Semantic-Model-Version-2 — everything below is new relative to the original [CARE-SM](https://github.com/CARE-SM/CARE-Semantic-Model) it was derived from.

## [1.0.0-beta] - 2026-07-26

### Added
- Mermaid transcriptions of all 22 original CARE-SM data-element diagrams (`diagrams/CARE-SM-obo-*.md`), styled for readability (narrow layout, muted `rdf:type` annotations, larger fonts) — see each file's own history for the styling iterations.
- A full Sphinx + MyST + `sphinxcontrib-mermaid` documentation site (`docs/`), mirroring and extending the original CARE-SM ReadTheDocs structure, with diagrams pulled in from `diagrams/` via a single source of truth (no duplicated content). Published at https://care-sm-semantic-model-v2.readthedocs.io/en/latest/.
- `tools/diagram_sync.py` — parses a diagram's Mermaid source and mechanically derives the per-model ontology lookup the CARE-SM Toolkit needs plus the glossary's Mandatory/Optional column marks, then diffs both against the real installed Toolkit and `docs/glossary.md` to surface drift between the (now-ahead) diagrams and the (not-yet-updated) downstream artifacts.
- Negative-observation support for Phenotype and Diagnosis: `Process_ --has target--> Target_` (what was tested) + boolean `Output_ --has value-->` result + `Attribute_` asserted only when the result is `true`. The original model had no way to represent a confirmed-absent finding.
- Optional evidentiary-provenance placeholder (`Process_ --has input--> Input_`) on Diagnosis, deliberately left unpopulated by design — see `docs/migration.md` for the reasoning.
- Optional consent-form reference on Consent (`has input`, filename + version string rather than a URL).
- `docs/migration.md` / README "Migrating from v1" section — a full model-by-model diff against the original CARE-SM for anyone migrating existing data or tooling.
- ERDERA funding acknowledgement (continuation of the original EJP RD acknowledgement).

### Changed
- **Renamed** the "Disability" model to **"Functional Assessment"** and moved it from "Patient-reported outcomes" to "Clinical and molecular measurements". Split its previously-conflated `IRISpecificAssessment` node into a separate `Target_` (the instrument/metric identity, e.g. WHODAS) and `URIProtocol` (the exact administration protocol) — the same instrument can be delivered under different protocols, which the original model couldn't distinguish. Added an optional, Toolkit-resolved human-readable label on `Output_`.
- Coded-value identifier nodes (a phenotype/disease/country code reached via `Output_ --has identifier-->`) are now explicit bnodes (`Identifier_`) with the code stored as a literal `has value`, rather than nodes whose identity was effectively derived from the code itself — which risked unrelated patient records merging together at that node. Affected: Phenotype, Diagnosis, Birthplace, Genetic.
- Duration/time-interval data is now modeled via `Output_ --exists at--> Duration_` instead of `Output_ --refers to--> Attribute_` (which incorrectly typed a time interval as an attribute of the patient, and gave it a `has value` that SIO durations don't have). Affected: Phenotype, Disability/Functional Assessment; added fresh to Diagnosis.
- Genetic: `has identifier` moved from `Output_` to `Attribute_`, so a single sequence variant report can now describe multiple variants (one `Attribute_`/`Identifier_` pair each) instead of being limited to one.
- Node naming standardized across models: the same structural role (reached via `has target`/`has input`/`is specified by`/`is causally related with`) now uses the same generic node name everywhere (`Target_`, `Input_`, `URIProtocol`, `Causality_`) instead of bespoke per-model names (`IRIGeneticDisease`, `URITreatmentPlan`, `IRIConditionCode`, etc.). Affected: Clinical_trial, Cohort, Medication, Deathdate, Questionnaire, Symptoms_onset. Cosmetic only — does not change the RDF produced.
- README/RTD sidebar and layout fixes (width, scrollbar, logo sizing).

### Fixed
- Hospitalization and Surgery had no `Output_`/`Duration_` branch at all, despite the glossary documenting `startdate`/`enddate` as available columns for both — there was previously nowhere in the RDF for that data to go. Both now have the standard `Output_ --exists at--> Duration_` branch plus an optional generic output value.

### Known limitations
- None of the above has been propagated to the CARE-SM Toolkit, YARRRML mapping, glossary CSV-column documentation, or example CSVs yet — the diagrams are intentionally ahead of those artifacts during this harmonization phase. `tools/diagram_sync.py` tracks exactly where they currently disagree.
- `Attribute_` now has three different cardinalities depending on the model (unconditional / conditional / multi-valued) — see `docs/migration.md` for which models use which.
