# How authentication actually works between the ERDERA Virtual Platform and the resources it queries

This explains what "auth" means on a Beacon (or other) call arriving from
the ERDERA Virtual Platform (VP), for anyone implementing or registering a
resource behind it. It was written while building a Beacon v2 facade for
CARE-SM-2 (see `handoff-beacon-caresm.md` and `facade/`), by reading the
VP's own source — `RDVP-Portal-frontend` and `RDVP-Portal-backend` on the
ERDERA GitHub org — rather than assuming spec behavior. Every claim below
points at the specific class/file it comes from, so it can be re-verified
if the VP codebase changes.

**The short version:** every outbound call from the VP to a resource
carries *two* separate, unrelated auth headers. Only one of them is meant
for the resource to check. Confusing the two is an easy and consequential
mistake for a resource implementer to make.

## The two headers

Built in `BeaconIndividualsQueryHandler.getResponse()` (RDVP-Portal-backend):

```java
WebClient client = WebClient.create();
response = client.post()
        .uri(resource.getResourceAddress())
        .bodyValue(requestBody)
        .accept(MediaType.APPLICATION_JSON)
        .header("auth-key", authKey)
        .header("Authorization", UserHandler.getBearerToken())
        ...
```

### `auth-key` — a static, per-resource secret. **This is the one resources should check.**

This identifies *the VP itself* as a trusted caller — not the individual
end user, and not tied to any login state at all.

- The VP operator holds one environment variable, `RESOURCES_AUTH_KEYS`
  (`ResourceService.java`), containing a single JSON object mapping
  resource ID → secret, e.g. `{"my-resource-id": "some-long-secret"}`.
- When your resource is registered with the VP, the onboarding/VP team
  adds one entry for you to that map and separately tells you the value.
- That same value is sent as `auth-key` on **every** call to your
  resource — whether the human using the VP is logged in or completely
  anonymous. It does not change per-user or per-session.
- This is what a resource implementer should validate: reject the call
  (401/403) if `auth-key` doesn't match the value you were given.

### `Authorization: Bearer <token>` — the calling user's own AAI token, just forwarded. **Not meant for resources to validate.**

```java
public static String getBearerToken() {
    String token = null;
    if (isAuthenticated() && !isAnonymous()) {
        var authentication = SecurityContextHolder.getContext().getAuthentication();
        token = "Bearer " + ((JwtAuthenticationToken) authentication).getToken().getTokenValue();
    }
    return token;
}
```

(`UserHandler.java`)

If the person using the VP logged in via LifeScience AAI, this is
*literally that person's own AAI access token* (a JWT), forwarded
byte-for-byte to every resource the VP queries on their behalf. If they
are not logged in, `getBearerToken()` returns `null` and the header is
effectively empty.

Crucially: **no resource is expected to validate this token.** Only the
VP backend itself validates it — via `SecurityConfig.java`, which
configures a `JwtDecoder` against LifeScience AAI's JWK set
(`JWK_SET_URI`) — and it does so purely to decide, server-side, whether
*it* is willing to include certain filters in the request it's about to
build (see below). For a resource to independently validate an arbitrary
end user's AAI token, that resource would have to separately register as
an OIDC relying party with LifeScience AAI itself. Nothing in the current
design expects or requires that. Treat this header as informational/audit
only, not a credential to check.

## What login state actually gates: filters, not access to the resource itself

Being logged into the VP doesn't grant a different auth token to
resources (see above — `auth-key` never changes). What it actually
controls is **which search filters the VP is willing to send at all**:

- `SearchFilters.vue` (RDVP-Portal-frontend) has real, working UI controls
  for `sexes` (checkboxes) and three age-range sliders — `ageThisYear`,
  `symptomOnset`, `ageAtDiagnoses`.
- `DiscoverySearchResults.vue`'s `discardFiltersNeedingAuthorization()`
  strips all four of those out of the request client-side if the user
  isn't logged in.
- `SearchController.java` enforces the same rule server-side — an
  anonymous request that somehow includes any of those four params gets
  HTTP 401.
- `diseases` (and non-Beacon params like `resourceTypes`/`countries`) are
  **not** gated and reach resources regardless of login state.

So: an anonymous VP search can only ever carry a disease filter. A
logged-in user's search can carry disease + sex + all three age ranges.
Your resource has no way to distinguish "logged-in VP user" from
"anonymous VP user" — it only sees whichever filters made it through. If
finer-grained access control at the resource level is ever wanted (e.g.
"only some resources get to see age/sex filters," or "count granularity
only for trusted partners"), that would need a mechanism separate from
`auth-key`, since `auth-key` identifies the VP as a whole, not the
end user or their permission level.

## A real design flaw this creates: non-VP callers can only ever get a boolean

Because `auth-key` is a single shared secret known only to the VP, and
Beacon is meant to be publicly queryable, a resource that treats
`auth-key` as a hard access gate (require it or reject the call) would
make itself unreachable by anyone except the VP — undesirable, since real
Beacon clients other than this VP should be able to reach a registered
resource too. The alternative — not gating access at all, just answering
everyone — means the resource can safely only hand out a `boolean`
`exists` answer to anyone who isn't holding the shared `auth-key`, and
reserve an actual patient `count` for whoever does (see this facade's own
`app.rb`/`lib/beacon_response.rb` for a concrete implementation of that
split).

That is a real, significant limitation, not just a caveat: **the actual
purpose of a Beacon** — helping someone identify a resource with enough
matching patients to be worth pursuing, e.g. for a clinical trial site
survey — generally needs a *count*, not just an existence flag. A "yes,
somebody somewhere matches" answer is close to useless for that purpose.
As things stand, only the one client holding the shared `auth-key` (today,
just the VP) can ever get that count from a resource that follows this
access model — anyone else querying a resource directly, or through some
other federated Beacon network, is stuck with boolean-only.

### Could a resource validate the forwarded LS AAI token directly instead, and grant count access to any authorized LS AAI user (not just the VP)?

Technically, partially — but with real caveats, not just "yes":

- LifeScience AAI is a standard OIDC provider with a public JWKS endpoint
  (e.g. `https://login.aai.lifescience-ri.eu/oidc/jwk` for the generic
  service; ERDERA/EJP-RD may run its own VO-scoped proxy of it — the
  specific `JWK_SET_URI` the VP itself uses, in `SecurityConfig.java`,
  would need confirming rather than assumed identical). A resource could
  independently verify the forwarded `Authorization: Bearer` token's
  signature against that same JWKS, exactly as the VP's own
  `NimbusJwtDecoder` does — this part is real and would detect tampering.
- LS AAI does support entitlement-style claims (`eduperson_entitlement`,
  `voperson_external_affiliation`) that can encode VO/group membership --
  in principle, "is this person in the ERDERA/EJP-RD group recognized as
  ethics-approved for rare disease count queries" is exactly the kind of
  thing such a claim is designed to express, *if* ERDERA defines and
  populates that specific group.
- But two things make this less solid than it sounds:
  1. **Signature validity only proves "this is a genuine LS AAI-authenticated
     user," not "this specific user is ethics-approved for anything."**
     Without checking a specific entitlement value for an
     ERDERA-controlled VO/group, any LS AAI user at all — of any
     participating service, anywhere — would pass. That's barely more
     restrictive than no check.
  2. **Audience mismatch / token-passthrough risk.** The token
     `UserHandler.getBearerToken()` forwards is the VP frontend's own
     access token, most likely issued with an audience scoped to the VP's
     backend as the intended resource server — not to us. Verifying its
     signature doesn't confirm it was ever meant to authenticate the
     bearer to a *different* downstream API. Relying on it that way is a
     known OAuth anti-pattern (a resource ends up trusting a token minted
     for someone else's use, not "resource indicators"/audience-restricted
     for it). It would need explicit sign-off that this forwarding
     pattern is intentional and safe, not assumed.
  3. It's also unconfirmed whether entitlement claims like
     `eduperson_entitlement` actually survive into the specific *access
     token* JWT being forwarded here (`at+jwt` type) — some providers only
     expose richer claims via the ID token or userinfo endpoint, keeping
     the access token minimal. This would need inspecting a real captured
     token to confirm, not assuming.

**Bottom line:** this is a real, buildable improvement — closer to
"actually useful count-tier access for genuinely ethics-approved
researchers, VP or not" — but it needs a specific ERDERA-recognized
entitlement value to check for, confirmation of the exact JWKS/audience
details, and ideally a real sample token to validate against, before it's
safe to rely on for anything beyond "slightly better than nothing." **We
have deliberately not implemented this yet** — it's documented here as an
open design question, not a plan in progress, pending those specifics.

### The uncomfortable part: neither mechanism is actually "security"

It's worth being blunt about this, because it's easy to read "validate the
LS AAI token" as a fix and miss that it isn't one. LifeScience AAI is a
*federation* — it lets someone log in via their home institution's IdP, a
handful of other research-AAI federations (eduGAIN and similar), or in
some deployments even social/other external identities. A validly-signed
LS AAI token proves only "some account, from some participating identity
source, somewhere, authenticated" — it says nothing about whether that
person is who a resource actually wants to trust with patient counts
(e.g. an ethics-body-approved researcher). Without a specific,
ERDERA-controlled entitlement claim to check, "validate the LS AAI token"
and "accept any token at all" are close to the same thing in practice.

And the shared `auth-key` this facade currently checks has the identical
underlying weakness, just one level removed: it doesn't authenticate the
human either. It only confirms "this call came through something holding
the VP's shared secret" — i.e. it's evidence the request passed through
the VP's intended UI/flow, not evidence about who's sitting behind it or
whether they're ethically authorized for anything. A resource choosing to
trust `auth-key`-bearing calls is a pragmatic call — "at least we know
this went through the front door we were told to expect" — not a
meaningful access-control decision about the end user. Both mechanisms
currently describe *where a request came from*, not *who should be
allowed to see a count*. Closing that gap for real would need something
neither mechanism provides today: an actual, ERDERA-governed authorization
signal (e.g. a specific entitlement tied to real ethics/data-access
approval), independent of which identity or software happened to carry
the request.

## Practical takeaway for resource implementers

1. Validate `auth-key` against the secret you were given at registration.
   That's your real authentication check.
2. Don't attempt to validate `Authorization` — it's the end user's own AAI
   token passed through as a courtesy, present only when they're logged
   in, and not verifiable by you without becoming an AAI relying party
   yourself.
3. Don't assume "logged in" vs "anonymous" is visible to you as a
   resource — it isn't, directly. It's visible only indirectly, through
   which filters happen to be present in the request you receive.
