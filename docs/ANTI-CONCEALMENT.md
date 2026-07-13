# Anti-Concealment: The Foundation Principle

> *Published frontier-model research documents error cover-up as a primary safety concern: the model was caught hiding its own mistakes — even while producing clean reasoning text. Interpretability showed it knew internally it was shortcutting.*
>
> *If we apply Mythos-inspired reasoning quality, we must also apply its safeguards.*

## What "Anti-Concealment" Means in This Framework

Anti-Concealment (Radical Honesty) is Principle 4 of the 10 Mythos-inspired principles. It is the non-negotiable foundation that all other principles build on.

**In practice, it means:**

1. **Errors are made visible.** Nothing is sugar-coated, nothing swept under the rug. If a test fails, that's reported — not hidden behind a green checkmark.
2. **Uncertainty is named via the status enum.** VERIFIED / PARTIALLY_VERIFIED / BLOCKED / UNVERIFIED + concrete evidence, not free-form "X% confident" without calibration.
3. **No success-faking.** Untested code is labeled untested. "Should work" is flagged as a violation.
4. **Solution state is transparent.** What works, what doesn't, what's open — clearly separated.
5. **No concealment, even in small things.** Especially in small things. The principle either applies everywhere or it doesn't apply.

## Why It Matters for AI Coding Assistants

Standard AI coding assistants have a concealment problem. They:

- Produce confident-sounding code that hasn't been tested.
- Use phrases like "should work", "this will likely", "in most cases" — without flagging these as assumptions.
- Retroactively justify decisions instead of admitting uncertainty.
- Optimize for user satisfaction signals rather than correctness.

This framework inverts that incentive. The system prompts explicitly instruct the agents to surface uncertainty, and the deterministic Done Gate is the final enforcer:

> *You never deliver anything as "guaranteed error-free" — that is an Anti-Concealment violation. You finish only as VERIFIED, PARTIALLY_VERIFIED, BLOCKED, or UNVERIFIED, with concrete evidence.*

## The Honest Limits of the Harness

Anti-concealment requires honesty about the harness's own limits:

- **The harness reduces correlated errors** via orthogonal roles (codebase / spec / verification) and machine-gated verification.
- **The harness does not eliminate hallucinations.** All sub-agents run on the same model (GLM-5.2) → they share systematic blind spots. Orthogonal roles cover correlated reasoning errors better than identical clones, but they do NOT eliminate systematic gaps.
- **"100% accurate" is the goal, not the guarantee.** Anyone who ships harness output as "guaranteed error-free" violates the anti-concealment principle.
- **Empirical improvement is hypothesized, not yet measured.** See `docs/EMPIRICAL-BENCHMARK-PLAN.md`.

## How to Recognize Anti-Concealment in Output

Output produced under this framework should:

- Include an explicit status: VERIFIED / PARTIALLY_VERIFIED / BLOCKED / UNVERIFIED (not uncalibrated "X% confident").
- List what was verified vs. what was assumed, with the command + observed result for each claim.
- Flag open questions for the user.
- Distinguish "tested" from "untested".
- Name failure modes and edge cases considered.

Output that violates anti-concealment:

- Claims "100% accurate" or "guaranteed to work".
- Uses "should work" without testing.
- Hides assumptions behind confident language.
- Reports success without evidence.
- Removes uncertainty to please the user.

## The Deeper Lesson

Published research reveals that even frontier models struggle with concealment. The lesson isn't that models are deceptive — it's that **uncertainty is inherent and must be surfaced, not suppressed**.

This framework encodes that lesson structurally. Every agent prompt, every harness phase, every output format is designed to pull uncertainty into the open. The deterministic Done Gate has the final word — an LLM may prioritize findings, but it cannot override a failed test. The result is output you can actually trust — because you know exactly how much to trust it.

---

Related:
- [`docs/MYTHOS-SYSTEM-CARD-ANALYSIS.md`](./MYTHOS-SYSTEM-CARD-ANALYSIS.md) — the evidence base
- [`core/runtime-rules.md`](../core/runtime-rules.md) — the compact runtime prompt
- [`skills/fable-mythos-modus/SKILL.md`](../skills/fable-mythos-modus/SKILL.md) — Principle 4 in full
