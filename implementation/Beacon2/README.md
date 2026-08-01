# Beacon2: a GA4GH Beacon v2-shaped facade for CARE-SM-2

**Version: see [`VERSION`](VERSION)** (currently `0.1.0` — first
documented, versioned snapshot; not yet run against real data or a live
Severance/CARE-SM-2 deployment. See "Status" below.)

## What this is

A query-path-only, Beacon v2-shaped API in front of CARE-SM-2 patient
data, built for ERDERA's rare-disease Virtual Platform (VP), using
[Severance](https://github.com/FAIR-Data-Systems/Severance) as the secure
query relay to the internal triplestore. No `/catalog`.

Built primarily to correctly answer ERDERA's actual VP client, not a
literal reading of the GA4GH Beacon v2 spec — the VP deviates from the
spec in several real ways, and it's the only real caller this facade has.
See `facade/README.md` for specifics.

## Where everything is

- **[`handoff-beacon-caresm.md`](handoff-beacon-caresm.md)** — the
  original architecture plan this was built from (Severance's
  submit→poll→respond cycle, the two named-query design, why boolean vs.
  count granularity is a real question). Historical/design-rationale
  document; read this first for *why* things are shaped the way they are.
- **[`VP-AUTH-EXPLAINED.md`](VP-AUTH-EXPLAINED.md)** — a source-cited
  explainer of how auth actually works between the VP and any resource it
  queries: the static per-resource `auth-key` vs. the forwarded end-user
  LifeScience AAI token, what each does and doesn't prove, and the honest
  limits of both. Written up in enough detail to fold into ERDERA's
  onboarding documentation.
- **[`facade/`](facade/)** — the Sinatra app itself: routes, filter
  mapping, the Severance submit/poll client, response shaping, Dockerfile.
  See `facade/README.md` for setup, the request/response contract, and
  known gaps.
- **[`severance-queries/`](severance-queries/)** — the two named SPARQL
  queries (`individuals_exists`, `individuals_count`) that must be
  installed into a Severance Internal deployment's `./queries` folder for
  this facade to work at all. See `severance-queries/README.md` for the
  filter contract and the modeling assumptions baked into them.

## Status

- Filter mapping, response shaping, and the auth/access-tier model
  (public callers get a boolean `exists`; a caller presenting the correct
  `auth-key` gets a full count) have been built against, and smoke-tested
  against, ERDERA's actual `RDVP-Portal-frontend`/`-backend` source and a
  stub Severance server — not a real Severance + CARE-SM-2 deployment.
- **Not yet tested "in reality"** — no real data provider has deployed
  this over live CARE-SM-2 data yet. The specific modeling assumptions in
  `severance-queries/README.md` (person/role graph scoping, the
  true/false diagnosis match, the `age_diagnosis` property mapping) are
  the most likely things to need correction once that happens.
- Docker image builds on plain `ruby:3.2-alpine` (not a "hardened" vendor
  image — see `facade/README.md`'s Version section for why, and how the
  version is threaded through the image).
