# DTL Taxonomy

[![CI](https://github.com/kyal102/dtl-taxonomy/actions/workflows/ci.yml/badge.svg)](https://github.com/kyal102/dtl-taxonomy/actions/workflows/ci.yml) ![license](https://img.shields.io/badge/license-MIT-green)

**The open claim taxonomy and verdict schema for deterministic AI-output verification.**

When an AI system makes a checkable claim — a physics equation, a chemical reaction, a drug pairing, an RTL block, a statistical assertion — this repo defines the shared language for verifying it:

- **`taxonomy/domains.json`** — the claim taxonomy: domains → claim types → which gate checks them → what each status means. Four universal verdict classes: **pass · fail · refuse · malformed**. A gate that can't rule *refuses* — it never guesses.
- **`schemas/verdict.schema.json`** — the JSON shape every gate verdict follows, including the SHA-256 `certificate_hash` that makes results replayable.
- **`client/dtl_client.py`** — a zero-dependency Python client for the hosted API.

## The contract

```
AI proposes  →  gate verifies (deterministic, same input = same verdict)  →  certificate
```

`model_override` is always `false`: no model may overrule a gate.

## Try it in 60 seconds — no account

Every domain has a free, MIT-licensed lite gate you can run locally (linked per-domain in `taxonomy/domains.json`):

```bash
pip install requests-nothing-needed  # kidding — stdlib only
git clone https://github.com/kyal102/unitgate && cd unitgate
python -m unitgate "E = 0.5*m*v**2 + m*g*h"   # → DIMENSIONALLY_VALID
python -m unitgate "E = m*g*h + m*v"           # → DIMENSIONALLY_INVALID (exit 1)
```

## Call the hosted engines

The full engines (larger rule sets, certificates, evidence-pack replay, SLA) are hosted at [jvi3.com](https://jvi3.com):

```python
from dtl_client import DTLClient
c = DTLClient(api_key="jv3_live_...")   # free tier: 100 calls/mo, no card
v = c.check("unitgate", "check", {"query": "E = m * a", "mode": "equation"})
assert v["passed"] is False
print(v["proof_evidence"]["reason"])    # E is M*L^2*T^-2, but m*a is M*L*T^-2
print(v["certificate_hash"])            # sha-256 seal — auditors can replay this
```

Live price list: `GET https://jvi3.com/api/apigate/catalog` (most gates: 1 token = A$0.01 per call).

## Extend the taxonomy (PRs welcome)

Companies integrating DTL are invited to grow the shared vocabulary:

1. **New claim type in an existing domain** — add an entry under `claim_types` with an `example` and a `statuses` map to the four verdict classes.
2. **New domain** — open an issue first describing the domain, what a deterministic check looks like, and what the gate must *refuse* on. Then PR.
3. **Schema changes** — issue first; the verdict schema is a compatibility surface.

CI validates every PR: JSON well-formedness, every status maps to a valid verdict class, every lite repo URL resolves.

## What this repo is not

It is **not** the verification engines. Lite gates are open (MIT, linked above); the full engines, rule corpora, and replay infrastructure are proprietary to EcoKure — see [LICENSING.md](LICENSING.md). The taxonomy is the open interface between them and you: build against it freely, including commercially.

---

*Method patent-filed (AU provisional applications 2026905289, 2026905506). Maintained by EcoKure Pty Ltd (ACN 699 693 779) — kyal11105@gmail.com.*
