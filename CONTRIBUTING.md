# Contributing to the DTL taxonomy

The taxonomy is the shared vocabulary — growing it helps everyone who verifies AI output.

**New claim type (existing domain):** PR directly. Add to `claim_types` with `type`, a realistic `example`, and a `statuses` map where every value is one of `pass | fail | refuse | malformed`. CI enforces this.

**New domain:** open an issue first with (1) the domain, (2) what a *deterministic* check looks like (same input → same verdict, no model in the loop), (3) what the gate must REFUSE on. The refuse set is as important as the pass set.

**Verdict schema changes:** issue first — the schema is a compatibility surface for every integrator.

**What won't merge:** claim types that require a model's judgement to decide (that's the opposite of a gate), statuses that guess instead of refusing, and anything whose example can't be checked by a person with a pencil.
