# Changelog

All notable changes to this project are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

This is the first tagged release of CARE-Semantic-Model-Version-2 — everything below is new relative to the original [CARE-SM](https://github.com/CARE-SM/CARE-Semantic-Model) it was derived from.

## [Unreleased]

### Genetic model — `target` (gene) added

- **The `Genetic` model can now name the gene a variant/zygosity report is about** —
  previously it had no slot for this at all, only `identifier_value` (a variant's own
  lexical notation, e.g. HGVS) and `attribute_type` (zygosity). Added the same
  `Process_ --has target--> Target_` pattern already used by Diagnosis/Laboratory/etc.:
  `Target_` is typed by the gene's concept IRI (e.g. `http://identifiers.org/hgnc/10591`
  for SCN4A) and carries the gene symbol as an `rdfs:label`. Diagram
  (`diagrams/CARE-SM-obo-Genetic.md`), Toolkit template
  (`implementation/Toolkit/toolkit/template.py`), and `docs/glossary.md` all
  regenerated/updated via `tools/diagram_sync.py --write Genetic`.
- **`target` is Mandatory, not Optional**, for this model specifically
  (`POSITIVE_MANDATORY_OVERRIDE[("target", "Genetic")]` in `tools/diagram_sync.py`): a
  variant or zygosity report is only meaningful in relation to a specific gene, so every
  Genetic record must name one. Data that does not unambiguously identify a single gene
  should not be represented as a Genetic record at all.
- `implementation/Toolkit/toolkit/main.py`: added `"Genetic"` to the `target_type`
  allowlist in `expected_target_models` — without this, the Toolkit's `dispatch()` would
  silently drop any populated `target` value on a Genetic row (logs an info message,
  emits nothing). This is the actual load-bearing gate; `tools/diagram_sync.py` keeps its
  own mirror of this list (`DYNAMIC_FIELD_ROUTING`) in sync by hand, updated alongside it.
- `implementation/CSV/Genetic.csv`: added a populated `target` on every row (previously
  two rows demonstrated the multi-variant-per-report pattern with bare chromosome-level
  `NC_` accessions and no resolvable gene — replaced with a real compound-heterozygous
  `DYSF` example, two variants, same gene, both `GENO_0000402`). Verified end-to-end
  through the real Toolkit (`_process_file`): zero rows dropped, `target_type` correctly
  populated on all three.
- No YARRRML change needed — confirmed via `tools/diagram_sync.py --yarrrml`: the
  existing generic `target_id`/`target_type` mapping (`sio:SIO_000291`, already exercised
  by other models) covers the new edge for free.
- **Found and fixed a real bug in `tools/diagram_sync.py`**: `--write <one-model>`
  crashed with `KeyError` on every model *other* than the one requested, because
  `write_glossary()` rewrites the whole shared `docs/glossary.md` file in one pass and
  needs marks for every model in `MODEL_ORDER`, but was being called with only the
  requested model's freshly-derived marks. Fixed by overlaying the requested model(s)
  onto `load_glossary_ground_truth()`'s full set first — the same safe-overlay pattern
  `write_template_py()` already used correctly. Regression test added
  (`tools/test_diagram_sync.py`).

### Changed

- Replaced all references to FAIR-in-a-box/FiaB (`docs/implementation.md`,
  `implementation/RDF/README.md`) with [Sextans Suite](https://github.com/wilkinsonlab/Sextans-Suite)
  — FAIR-in-a-box has been superseded and no longer exists.

- `implementation/Beacon2/facade`, `implementation/Beacon2/severance-queries`, and
  `implementation/Beacon2/handoff-beacon-caresm.md` moved to their own dedicated repo,
  [`FAIR-Data-Systems/Severance-Facades`](https://github.com/FAIR-Data-Systems/Severance-Facades)
  (`beacon-facade/`), alongside its sibling `shallot-facade` (moved there from the `Severance` repo in
  the same change). The facade had no real code dependency on anything else in this repo. Full pre-move
  commit history is preserved in the new repo's own git log. `implementation/Beacon2/README.md` and
  `VP-AUTH-EXPLAINED.md` stay here, updated to point at the new repo; `VP-AUTH-EXPLAINED.md` is general
  VP-auth documentation, not specific to this facade's own code.

### Beacon facade (`implementation/Beacon2/facade`)

*(Historical -- this facade has since moved; see "Changed" above.)*

- Fixed `CVE-2026-42257`: the base `ruby:3.2-alpine` image's own stale, vulnerable `net-imap` default
  gem (`0.3.9`) -- an unused-by-this-app default gem, caught by the first real run of Severance's
  `Security/security-patch.sh` (which builds this facade from a fresh clone of this repo). Same fix as
  its sibling `shallot-facade`: pinned `net-imap ~> 0.5` in the `Gemfile` (resolves to `0.6.7`) and
  explicitly uninstalled the base image's stale copy in the Dockerfile (pinning alone installs the
  patched version alongside the old one, not in place of it). Verified live: rebuilt image has only
  `net-imap 0.6.7` present, and still boots and serves correctly.

### Beacon facade (`implementation/Beacon2/facade`)

- Added `docker-compose.yml`, hardened the same way as Severance's own `external/`/`internal/` compose
  files: `restart: always`, `security_opt: no-new-privileges`, `cap_drop: [ALL]` (no `cap_add` needed --
  this Dockerfile never runs as root), `mem_limit`/`cpus` ceilings. Builds from source (`build: .`)
  since this facade has no registry image yet. Done alongside the identical addition to its sibling,
  `Severance/facades/shallot-facade/docker-compose.yml` (a separate repo).
- **Found and fixed a real bug, by actually building and running the image for the first time**: the
  Dockerfile's runtime stage never copied `Gemfile`/`Gemfile.lock`, only the already-vendored gems --
  `bundle exec` needs the Gemfile itself present to resolve/activate them. Every container exited
  immediately with "Could not locate Gemfile". The README's own "Known gaps" note that this build was
  unverified turned out to be accurate.
- Added a generic `error StandardError` handler to `app.rb` as defense in depth: `show_exceptions
  :after_handler` renders Sinatra's detailed exception page (full backtrace, file paths, gem versions)
  for any uncaught exception, in every environment. Not currently reachable here (`/individuals` already
  rescues everything `SeveranceClient#query` can raise), but this facade's sibling
  (`shallot-facade`) hit exactly this class of bug live on a route with no such rescue, before its own
  fix and this same backstop were added there too.
- Verified live end to end with the rebuilt image: `GET /info` (200) and `POST /individuals` against an
  unreachable Severance (clean `502 severance_unreachable`, no leaked trace), running as the correct
  non-root `beacon` user.

## [1.0.0-beta2] - 2026-08-07

The model-side redesign in 1.0.0-beta was intentionally ahead of the CARE-SM Toolkit, YARRRML mapping, and example CSVs. This entry propagates that redesign into the real, executable implementation, consolidated into this repository at `implementation/` (superseding the separate `CARE-SM-Implementation` and `CARE-SM-Toolkit` repos, which are no longer the actively-edited copies).

### RDF / SPARQL examples

- **Found and fixed a real bug in the YARRRML mapping itself**, caught only by actually running the real pipeline end-to-end (Toolkit → `yarrrml-parser` → `rmlmapper-java`) rather than inspecting the mapping by eye: the `grel:controls_if` gates added earlier this session for the truth-contingent `Attribute_` edge (Phenotype/Diagnosis, `value=false`) and the `Identifier_` edge (absent `identifier_value`) used `grel:any_true: value: ""` to mean "emit nothing." In practice `rmlmapper-java` treats an empty string as a real (if degenerate) IRI local name, so a `value=false` row produced a triple pointing at the bare base URI (`<http://example.com>`) instead of no triple at all — worse than the already-accepted orphan-bnode residual, since it's a broken reference rather than just an unreferenced one. Fixed by removing the `any_true` parameter entirely (an unset branch correctly resolves to null, which `rmlmapper-java` does skip) in both `CARE_yarrrml.yaml` and `CARE_Fiab_yarrrml.yaml`. Verified against regenerated RDF: the false-value row now correctly contributes zero `refers to` triples.
- All 17 `implementation/RDF/*.nq` example files were fully stale (generated before this session's redesign — e.g. Phenotype's example still used the old URI-as-identity pattern, no boolean `value`, unconditional `Attribute_`/`Causality_`/`Unit_` regardless of model). Regenerated all of them, plus 2 new ones (`Consent`, `Functional_Assessment`, which now have real CSV examples), by actually running the real pipeline against small samples of each model's `implementation/CSV/*.csv` (trimmed to ~3 rows each, matching the original files' illustrative scale rather than dumping the full ~100-row bulk examples).
  - Toolchain used (none of it previously available in this environment, all installed fresh): `yatter` (a Python YARRRML→RML converter) was tried first but silently produced zero `rr:predicateObjectMap`s — it doesn't recognize this mapping's `predicateobject:` key (the standard YARRRML key is `po`). Switched to the real `@rmlio/yarrrml-parser` (JS, via a portable Node.js binary, no system install) plus `rmlmapper-java` 8.1.0 (via a portable JDK 21 tarball, since the pinned version needs a newer class-file version than the system's JDK 11) — this is the same toolchain the user's actual Sextans Fix / `yarrrml-rdfizer` deployment uses, so the regenerated examples are produced by the real reference implementation, not an approximation.
- **Found and fixed 3 real, pre-existing bugs in the exemplar SPARQL queries** (`implementation/SPARQL/`), independent of anything changed this session but now more consequential given it: `complete_query.sparql`, `diagnostic.sparql`, and `only-sio.sparql` all required inherently optional, model-specific predicates (`refers to Attribute_`, `has unit`, `has identifier`, `is causally related with` on `Output_`; `has target`/`has input`/`has frequency`/`is specified by`/`has part` on `Process_`) as a single mandatory basic graph pattern. Since almost no single model has all of these simultaneously, these queries likely already returned empty or wrong results against real v1 data — and now would additionally, silently exclude every `value=false` Phenotype/Diagnosis row (no `Attribute_` present), directly undermining this session's negative-observation work. Rewrote all three with proper `OPTIONAL {}` wrapping per predicate. Also fixed an unrelated typo in `only-sio.sparql` (`?casue` — a disconnected, never-bound variable shadowing the real `?cause`). `records.sparql` and `timeline.sparql` didn't touch this structure at all and were already correct, confirmed by testing.
  - Verified all 5 queries against the regenerated RDF using `pyoxigraph` (rdflib's pure-Python SPARQL engine proved too slow — multiple minutes/timeouts — on this many nested `OPTIONAL`s even on a few hundred quads; unrelated to query correctness, just not a viable test harness at this scale).

### w3id namespace

- Moved the CARE-SM w3id identifier from `https://w3id.org/CARE-SM` to `https://w3id.org/CARE-SM-2`, since v2 is a distinct, incompatible model redesign and needs its own persistent identifier rather than silently reusing v1's. Updated everywhere the old namespace appeared: `schema/care-sm-2.skos` (all 22 concept URIs, `skos:inScheme` references, and `rdfs:seeAlso` links, now pointing at the new `care-sm-semantic-model-v2.readthedocs.io` docs site), the `caresm:` prefix in both `implementation/YARRRML/CARE_yarrrml.yaml` and `CARE_Fiab_yarrrml.yaml`, all 19 regenerated `implementation/RDF/*.nq` examples, and the legend text embedded in the legacy drawio diagram source `images/obo/CARE-SM-obo`.
- While updating `care-sm-2.skos`, also renamed its `Disability` concept to `Functional_Assessment` to match the model rename made earlier in the v2 redesign, and corrected the Genetic concept's `rdfs:seeAlso` anchor from `#genetic` to `#genotype` to match its actual heading anchor.
- **Reverted the `CARE-SM-2` namespace above** in favor of `https://w3id.org/CARE-SM/v2`, at the w3id.org maintainers' request: they asked that all CARE-SM community entries consolidate into a single `.htaccess` under the one `w3id.org/CARE-SM` prefix, with v1 (widely in use, can't change) resolving as before and v2 (not yet in use anywhere, safe to redirect) living at the `/v2` subpath instead of a separate `-2` prefix. Updated every reference: `schema/care-sm-2.skos` (still so named — see note below), all 19 `implementation/RDF/*.nq` examples, the `caresm:` prefix in both YARRRML mappings, and the drawio legend in `images/obo/CARE-SM-obo`. File and directory names (`care-sm-2.skos`, `CARE-SM-*.nq`) were deliberately left as-is — only the namespace URIs needed to be correct, not the local filenames.

- `setup.py`'s `url`/`project_urls` updated from the old `CARE-SM/CARE-SM-Toolkit` repo to this one (author credit to Pablo Alarcón Moreno kept as-is — legitimate provenance, not a stale reference).
- `Dockerfile` and `docker-compose.yaml` moved from `toolkit/API/` to the Toolkit package root, so they build from (and are discoverable at) the package's own top level rather than buried inside its API submodule. `toolkit/API/requirements.txt` no longer lists `care-sm-toolkit` as a PyPI dependency (the image now installs from local source via `pip install .`, which would otherwise conflict).
- Added `VERSION` (currently `2.0.0`) at the Toolkit root, matching the plain-`VERSION`-file convention already used across this org's other projects (`FAIR-Champion`, `FDP-Tools`, etc.) — a manually-maintained record, not something the Dockerfile reads programmatically, consistent with how those other projects use it.
- **Found and fixed a real, previously-unnoticed bug**: `toolkit/API/main.py` computed its data folder as `Path(__file__).resolve().parent.parent / "data"` — a relative-to-`__file__` calculation that only happens to equal `/data` if the file sits exactly two directories below the container root. Three different places in the pre-existing setup each guessed a different container path for the same thing (the app's own computation, the original `docker-compose.yaml`'s `/data` mount, and this docs page's own example `/code/data`) and none of them agreed. Confirmed against the real, currently-deployed [Sextans Fix](https://github.com/wilkinsonlab/Sextans-Suite) production `docker-compose-template.yml` (which almost all real users go through, not this Dockerfile directly) that the authoritative, actually-relied-upon convention is `/data` — replaced the fragile computation with a hardcoded `/data` default, overridable via `CARE_DATA_DIR`. This also makes `markw/care-sm-toolkit:2.0.0` a drop-in replacement for the currently-deployed `fairdatasystems/care:2026-07-10` in that same compose file, with no volume-mount changes needed.
- Documented the full Sextans Fix integration in `docs/toolkit.md` (new "Sextans Fix" section): how its four services chain together, and specifically how `caresm` (`/data`) and `yarrrml-rdfizer` (`/mnt/data`) — two separate containers — share one host folder at each container's own fixed mount point rather than needing matching internal paths.

### Added

- `implementation/Toolkit/` — the CARE-SM Toolkit Python package, brought into this repo so the model redesign can be implemented directly rather than tracked as external drift.
- Truth-contingent `Attribute_` for Phenotype/Diagnosis: `Toolkit.value_edition()` now derives `attribute_type` from `target` only when `value == "true"`; left unset when `false`, so the paired YARRRML gate (below) skips creating `Attribute_` entirely for a negative result, matching "if it doesn't exist, then it isn't an attribute."
- `xsd:boolean` support end-to-end: a `value_boolean` column in `Toolkit.value_edition()` and a matching `has value` predicate-object in the YARRRML `Output_` mapping — previously unsupported anywhere in the pipeline.
- Multi-variant support for Genetic: rows sharing `pid` + `model` + `event_id` now collapse onto one shared `Process_`/`Output_` (`uniqid`), while each row keeps its own distinct `Attribute_`/`Identifier_` pair (new `attribute_uniqid`), so one sequence variant report can describe several variants. `event_id` was previously collected but never used for anything.
- `Attribute_ --has identifier--> Identifier_` mapping in YARRRML (genuinely new — no model needed it before Genetic), plus the `identifier_value`/`identifier_type` columns feeding it.
- `Input_ --has value-->` mapping in YARRRML plus a new `input_value` column, needed by Consent's Consent-Form branch (added to the diagram earlier this session, never wired into the mapping until now).
- New/updated CSV examples reflecting all of the above: `Genetic.csv` (multi-variant), `Consent.csv` (new), `Functional_Assessment.csv` (renamed + rewritten), `Phenotype.csv`/`Diagnosis.csv` (rewritten for the new boolean `value` + `target` design, including a `false` case).
- `.github/workflows/toolkit-tests.yml` at the repo root, and a test-status badge on `implementation/Toolkit/README.md`.

### Fixed

- Propagated the "Disability" → "Functional Assessment" rename (diagram-only until now) into `template.py`, `main.py`'s model keyword sets, and the CSV example/filename.
- Removed several stale/mismatched `template.py` constants inherited from before this session's redesign, found while implementing the above and confirmed against the current diagrams (not guessed at):
  - Phenotype/Diagnosis/Functional_Assessment: incorrect fixed `attribute_type` values (`NCIT_C217011`, `NCIT_C7057` — apparent copy-paste artifacts from unrelated models); removed since none of the three has a fixed-type `Attribute_` anymore.
  - Phenotype/Diagnosis/Genetic: `output_id_type` / `output_id` dispatch, describing an `Output_ --has identifier-->` structure none of the three has in its current diagram.
  - Genetic: the `output_id_type` value it *did* correctly need (`NCIT_C164607`, Sequence Identifier) was misfiled under the wrong field name (it types `Attribute_`'s `Identifier_`, not `Output_`'s) — moved to a correctly-named `identifier_type`.
  - Consent: `input_type` was missing from `template.py` entirely (the Consent-Form `Input_` branch was added to the diagram this session but never propagated).
  - Functional_Assessment: added to `target_type` dispatch (has a `Target_` node in the current diagram; didn't before this session) and removed from `input_id` dispatch (has no `Input_` node at all).
- Confirmed (not assumed) that Medication's and Consent's dynamic `output_type` were already correctly handled by an existing `valueIRI → output_type` dispatch rule — no code needed, verified with an end-to-end smoke test.
- `test_time_edition_missing_dates` (Toolkit pytest suite) asserted `is None` on a pandas value that had passed through `Series.where()` — which normalizes missing values to `NaN` even on an `object`-dtype column, regardless of whether the original held a literal `None`. The underlying `time_edition()` behavior was already correct (confirmed with `pd.isna()`); only the assertion was too strict. Fixed to `assert pd.isna(...)`. Full suite (14/14) now passes.

### Known limitations

- The orphan-bnode residual for a `false` Phenotype/Diagnosis row (a disconnected `sio:SIO_614`-typed triple with no incoming edge, since RML triples maps fire per row regardless of whether anything references the subject) is accepted as-is — cleanable later with a SPARQL `DELETE` if it ever matters.

### Changed (public CSV schema)

- `specification` was a validated public column (`Toolkit.columns_to_check`) that was never actually consumed anywhere in the YARRRML mapping — only `protocol_id` was wired up. Removed `specification` entirely rather than keep two columns for one concept; `protocol_id` is now the single, documented, real column. `IRI reference to any associated protocol`-style descriptions were migrated onto `protocol_id`, not discarded.

- Retired the overloaded `valueIRI`/`agent` public columns. Both were routed to *different* internal fields depending on the model (`valueIRI` meant `attribute_type` for Sex/Status/Examination, `output_type` for Consent/Medication, `output_id` for Birthplace/Clinical_trial/Cohort/Biobank, `cause_id` for Deathdate; `agent` meant `attribute_type` for Genetic, the drug's own identity for Medication) — a CSV author saw a generic-sounding column with no hint what it meant for their specific model, and no script could reliably tell "the point of the record" (Mandatory) from "an optional extra" (Optional) from diagram structure alone. Replaced with direct, self-describing public columns following the pattern `target`/`frequency_type` already used successfully: `attribute_type`, `output_type`, `output_id`, `cause_id`. Medication's drug identity (previously `agent`) now goes through the existing `input` column, joining Questionnaire in the `input_id` dispatch.
  - Confirmed before refactoring that neither `valueIRI` nor `agent` was ever referenced directly in YARRRML (`grep '$(valueIRI)\|$(agent)'` — no matches) — both were pure `main.py`-side staging columns, immediately renamed into their real internal field by `value_edition()`'s dispatch tables before anything downstream ever saw them. This meant the refactor was contained entirely to `main.py` and the CSV layer; **no YARRRML or `template.py` changes were needed**, since YARRRML already read `$(attribute_type)`/`$(output_type)`/etc. by their real internal names.
  - `main.py`'s `expected_valueIRI_models`/`expected_agent_models` dispatch tables removed entirely — no longer needed, since these fields now flow straight through `add_columns_from_template()`'s existing raw-column merge, the same mechanism `target_type`/`input_type` already relied on for their *fixed* half.
  - All 9 affected CSV examples (`Biobank`, `Consent`, `Birthplace`, `Genetic`, `Status`, `Deathdate`, `Examination`, `Medication`, `Sex`) updated to the new column names; re-verified end-to-end through the real Toolkit pipeline (0 rows dropped).
  - `docs/glossary.md`'s master column table and every affected per-model section updated. The M-vs-O distinction for each new column (e.g. Sex's `attribute_type` is Mandatory, Genetic's is Optional) is hand-verified positive knowledge carried over from the pre-refactor `valueIRI`/`agent` marks, encoded in `tools/diagram_sync.py`'s new `POSITIVE_MANDATORY_OVERRIDE` table — not re-derived from scratch, since (as established earlier in this same entry) that distinction isn't reliably derivable from diagram structure alone.
  - `implementation/YARRRML/CARE_Fiab_yarrrml.yaml` — found to be fully unpatched for every structural change made to `CARE_yarrrml.yaml` this session (the `attribute_type` null-gate, `value_boolean` support, `input_value` support, Genetic's `Identifier_`/`attribute_uniqid` mapping) plus using the pre-rename `$(duration)` instead of `$(duration_value)`. Re-synced to match `CARE_yarrrml.yaml` exactly except for its one deliberate divergence — the `this: '|||baseURI|||'` placeholder, substituted by the external RDFizing workflow so generated URIs can optionally resolve — which was confirmed as the only such placeholder present and preserved as-is.

### Tooling

- `tools/diagram_sync.py` rewritten from a read-only drift *checker* into the full sync workflow requested: `--write` now directly regenerates `implementation/Toolkit/toolkit/template.py`'s `TEMPLATE_MAP_OBO` and every per-model section of `docs/glossary.md` (Mandatory/Optional/N-A marks) from the diagrams, the single source of truth. `--csv` validates every `implementation/CSV/*.csv` example against the real Toolkit pipeline (reports dropped rows). `--yarrrml` reports diagram edges with no corresponding predicate anywhere in the YARRRML mapping.
  - Ground truth is now our own `implementation/Toolkit/` copy, not the external pip-installed package.
  - Classification-aware: distinguishes true fixed constants from dynamic per-record ranges (an early, cruder version of this logic mistook dynamic diagram labels like "IRI for X, e.g.:" for fixed IRIs — caught and fixed before trusting any output).
  - Source-node-aware field derivation: the same SIO property can mean different things depending on which node it originates from (`has identifier` from `Output_` means `output_id_type`; from `Attribute_` it means the new `identifier_type`) — a plain property-code lookup would have conflated these.
  - Mirrors `main.py`'s dispatch tables (`DYNAMIC_FIELD_ROUTING`) to know which public column feeds a dynamic field for a given model — information genuinely absent from the diagram itself.
  - Deliberately conservative safety net, added after the naive version was caught proposing real regressions during review: never auto-downgrades an existing `M` mark to `O` (the M-vs-O distinction for routed dynamic fields isn't reliably derivable from structure alone — caught this concretely on Sex's `valueIRI` and Medication's `agent`, both correctly `M`); preserves the existing description whenever a column already had one, clearing it only when the diagram shows the column is now structurally `N/A`; new/newly-relevant columns get a clearly flagged placeholder description rather than a guess.
  - Every automatically-generated placeholder description was subsequently reviewed and replaced by hand with real content in this pass — none were left in the committed `docs/glossary.md`.
  - Column order within each glossary section is preserved as originally hand-authored (new columns appended at the end) rather than forced into a canonical order, to avoid pure reordering noise.

## [1.0.0-beta] - 2026-07-26

### Added

- Mermaid transcriptions of all 22 original CARE-SM data-element diagrams (`diagrams/CARE-SM-obo-*.md`), styled for readability (narrow layout, muted `rdf:type` annotations, larger fonts) — see each file's own history for the styling iterations.
- A full Sphinx + MyST + `sphinxcontrib-mermaid` documentation site (`docs/`), mirroring and extending the original CARE-SM ReadTheDocs structure, with diagrams pulled in from `diagrams/` via a single source of truth (no duplicated content). Published at [care-sm-semantic-model-v2.readthedocs.io](https://care-sm-semantic-model-v2.readthedocs.io/en/latest/).
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
