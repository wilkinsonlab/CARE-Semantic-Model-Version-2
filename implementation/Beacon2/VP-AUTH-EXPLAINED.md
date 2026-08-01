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
mistake for a resource implementer to make. There's also a third hop
worth understanding if the resource itself is a Severance-backed facade
(like this one): the facade's own authentication to Severance External is
a completely separate, independent credential from anything discussed
above, and it currently carries none of the VP-vs-public trust
distinction forward — see "This facade's own hop: Severance's `AUTH_TOKEN`"
near the end of this document.

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
human either. At best it confirms "this call came through something
holding the VP's shared secret" — and even that weaker claim needs the
qualification the next section spells out, because holding the secret is
far easier to come by than "being the VP." A resource choosing to trust
`auth-key`-bearing calls is a pragmatic call — "at least this presents the
credential we were told to expect" — not a meaningful access-control
decision about the end user, and, as it turns out, not even a reliable
one about the calling software. Both mechanisms currently describe *where
a request claims to come from*, not *who should be allowed to see a
count*. Closing that gap for real would need something neither mechanism
provides today: an actual, ERDERA-governed authorization signal (e.g. a
specific entitlement tied to real ethics/data-access approval),
independent of which identity or software happened to carry the request.

## How trivially spoofable is this, in practice?

Everything above analyzes what each header is *supposed* to mean. This
section is about what stops someone from just... not going through the VP
at all, and sending whatever they want directly. Short answer: as
designed, nothing does. This isn't a flaw specific to this facade — it's
a property of the VP's whole trust model, and applies identically to
every resource behind it.

**Both headers are static, unsigned, bearer-style values — anyone who
sees one, once, can replay it forever, from anywhere.** Neither `auth-key`
nor the forwarded `Authorization` token is bound to a specific request, a
specific time window, a specific origin, or a specific TLS session. They
are exactly the string that gets sent, every time, until someone manually
rotates them. That means:

- **Anyone can watch their own browser's Network tab during a normal,
  legitimate login and read both headers directly** — the exact scenario
  raised here. There's no special access or interception required: a
  logged-in VP user, using nothing but their own browser's built-in
  devtools, sees the literal `auth-key` and `Authorization` values on
  every outgoing request their own session makes. HTTPS doesn't help
  here — TLS protects data in transit *between* endpoints, from a network
  eavesdropper sitting somewhere on the path. It does nothing to stop an
  endpoint from reading its own already-decrypted traffic, which is
  exactly what a browser's Network tab shows. "It's HTTPS" is not an
  answer to "the legitimate client can see its own headers."
- **Once captured, `auth-key` doesn't just replay the same request — it
  authorizes *any* request.** There's no request signing (HMAC over the
  body, a signed nonce, anything binding the credential to specific
  content), so a captured key can be attached to a hand-crafted request
  with arbitrary filters, not merely a re-sent copy of one that was
  observed. Concretely: anyone who has ever seen this facade's `auth-key`
  once can query it directly, forever, for counts on any filter
  combination they like, indistinguishable at the protocol level from a
  genuine VP call.
- **`auth-key` is one shared secret for the *entire* VP, not per-user or
  per-session.** Any single person who extracts it — a curious end user,
  a developer with server/log access, a leaked CI secret, a compromised
  laptop — compromises trust for every VP user simultaneously.
  There's no way to revoke access for just the person who misused it
  without rotating the key and re-distributing it to every registered
  resource.
- **The forwarded `Authorization` token is, if anything, worse to rely
  on for exactly the reason raised here.** It's the end user's *own*
  credential — they don't need to "steal" it, they already legitimately
  possess it. Nothing stops them from extracting it from their own
  browser and calling a resource directly, bypassing the VP's UI (and
  whatever filter-gating logic lives only in that UI/backend) entirely.
  This is a real reason not to lean on "validate the LS-AAI token" as a
  meaningful access control even before the audience/entitlement concerns
  raised earlier in this document.
- **Nothing in the source (VP or this facade) implements rate limiting,
  anomaly detection, or key rotation.** A captured credential can be used
  as often and as fast as the caller likes; nothing currently in this
  chain would notice or slow it down.

None of this is solved by "add a bit more validation" in this facade
alone — it's a systemic property of using static, unsigned, bearer-style
secrets over a client the request-sender fully controls. Real mitigations
would look more like: short-lived, per-request signed tokens (issued by
the VP with an expiry, not one static value); HMAC request signing over
the body so a captured credential can't be pasted onto an arbitrary
query; mutual TLS or IP allowlisting for the VP's known egress (Severance
itself already does exactly this for its own Internal↔External traffic —
`ALLOWED_INTERNAL_IPS` in `external/env_template` — the same pattern
could apply between the VP and its resources, though the VP's IPs would
need to be known and stable for that to work); rate limiting; and a real
key-rotation procedure. None of that exists today. This facade's current
`auth-key` check is better than nothing (it stops a casual, uninformed
caller from getting a count by accident) but should not be described, to
anyone, as meaningfully restricting *who* can obtain patient counts from
a determined, technically unsophisticated observer — a browser's Network
tab is all it takes.

## Practical takeaway for resource implementers

1. Validate `auth-key` against the secret you were given at registration
   — but understand what that check actually buys you: it filters out
   casual/uninformed callers, not a determined one. Anyone who has ever
   captured the value (trivially, via their own browser's Network tab)
   can replay it indefinitely, from anywhere, with any request body they
   like. Don't describe or rely on this as real access control over *who*
   gets a count — see the spoofability section above.
2. Don't attempt to validate `Authorization` — it's the end user's own AAI
   token passed through as a courtesy, present only when they're logged
   in, not verifiable by you without becoming an AAI relying party
   yourself, and just as easily extracted and replayed by that same user
   directly, bypassing the VP entirely.
3. Don't assume "logged in" vs "anonymous" is visible to you as a
   resource — it isn't, directly. It's visible only indirectly, through
   which filters happen to be present in the request you receive.
4. If a real access-control decision is ever needed (e.g. gating patient
   counts to genuinely ethics-approved researchers), don't build it on
   either header as currently implemented. It needs something with actual
   cryptographic teeth — signed, short-lived, request-bound credentials —
   not a static value that's identical on every call forever.

## This facade's own hop: Severance's `AUTH_TOKEN`

Everything above is about the hop from the VP (or any other caller) to
this facade. There's a separate, independent hop after that: this
facade's own authentication to Severance External, using
`BEACON_SEVERANCE_AUTH_TOKEN` (sent as `Authorization: Bearer ...` on
every call to `/severance/queries`, matching Severance External's own
`AUTH_TOKEN` env var — see `Severance/external/env_template`). Worth
understanding on its own terms, separately from the VP-facing headers
above.

**Same underlying weakness, real structural mitigant.** Severance's
`AUTH_TOKEN` is exactly the same shape of thing as `auth-key` — a static,
unsigned bearer value, good until someone rotates it, replayable by
anyone who ever sees it (a leaked config, a compromised deployment
host, a captured value in transit if it's ever mishandled). But unlike a
bare API key in front of an arbitrary query endpoint, Severance bounds
what a stolen token actually grants: **only pre-approved, named queries**,
never arbitrary SPARQL. Even with a fully compromised `AUTH_TOKEN`, an
attacker can submit only a `query_id` that already exists in Internal's
`./queries` folder, with attacker-chosen values for that query's own
declared variables — they can't discover the query text (it never leaves
Internal), invent a new query, or execute anything outside that
pre-approved set. That named-query boundary is doing real security work
here; the token by itself isn't what's protecting the triplestore.

This is also why Severance is comfortable letting the token's *meaning*
be whatever the deploying client wants — e.g. some deployments (RedCap
logins setting a per-installation token that Severance External is
configured to match) get real, if informal, per-deployment significance
out of this value. **Beacon deployments don't get any of that.** This
facade uses exactly one static `BEACON_SEVERANCE_AUTH_TOKEN` for every
single call to Severance External, regardless of whether the original
`/individuals` request came from the VP with a valid `auth-key`, or from
a fully anonymous public caller with none at all. From Severance
External's point of view, there is exactly one caller: "the Beacon
facade" — full stop. The VP-vs-public trust distinction made earlier in
the request lifecycle (see the granularity split above) is fully
resolved and discarded *before* Severance is ever contacted; Severance's
own `AUTH_TOKEN` layer carries zero information about, and provides zero
additional protection specific to, the original caller's trust level.
**Beacon calls are, in this specific sense, ignoring Severance's own
per-client authentication semantics entirely** — they collapse it to a
single, undifferentiated "yes, this is Beacon" signal, in a way that
other Severance client integrations may not.

None of this is a defect unique to this implementation — it's inherent
to using one shared client credential for an entire class of traffic
(every Beacon caller, trusted or not) rather than a credential per
underlying requester. If finer-grained propagation of caller trust all
the way through to Severance is ever wanted, it would need Severance
itself to understand more than one caller identity per registered
client, which it doesn't today.
