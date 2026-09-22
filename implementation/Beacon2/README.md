# Beacon2: a GA4GH Beacon v2-shaped facade for CARE-SM-2

A query-path-only, Beacon v2-shaped API in front of CARE-SM-2 patient
data, built for ERDERA's rare-disease Virtual Platform (VP), using
[Severance](https://github.com/FAIR-Data-Systems/Severance) as the secure
query relay to the internal triplestore. No `/catalog`.

**The facade itself moved.** As of 2026-09-22, the Sinatra app
(`facade/`), the SPARQL query binding contract (`severance-queries/`),
and the original design rationale (`handoff-beacon-caresm.md`) all live
in [`FAIR-Data-Systems/Severance-Facades`](https://github.com/FAIR-Data-Systems/Severance-Facades)'s
`beacon-facade/` directory now, alongside its domain-agnostic sibling
`shallot-facade`. Neither facade had a real code dependency on the repo
it previously lived in, so this repo's copies were removed rather than
kept in sync with two owners. Full pre-move commit history for
`beacon-facade` is preserved in that repo's own git log.

## What's still here

- **[`VP-AUTH-EXPLAINED.md`](VP-AUTH-EXPLAINED.md)** — a source-cited
  explainer of how auth actually works between the VP and any resource it
  queries: the static per-resource `auth-key` vs. the forwarded end-user
  LifeScience AAI token, what each does and doesn't prove, and the honest
  limits of both. General enough to apply to any VP-facing resource, not
  specific to this facade's own code, so it stayed here. Written up in
  enough detail to fold into ERDERA's onboarding documentation.

For the facade's own setup, request/response contract, known gaps, and
the query modeling assumptions, see
[`beacon-facade/README.md`](https://github.com/FAIR-Data-Systems/Severance-Facades/blob/main/beacon-facade/README.md)
and
[`beacon-facade/severance-queries/README.md`](https://github.com/FAIR-Data-Systems/Severance-Facades/blob/main/beacon-facade/severance-queries/README.md)
in the new repo.
