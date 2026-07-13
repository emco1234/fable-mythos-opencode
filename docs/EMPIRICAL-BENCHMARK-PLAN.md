# Empirical Benchmark Plan

> This harness currently rests on a **hypothesis**, not on measured results. This document defines the comparison that would turn the hypothesis into evidence. Until this plan is executed, every quality claim about the harness is "planned, not yet measured".

## Hypothesis

Independent, evidence-based verification improves reliability. Specifically: the reliability harness (orthogonal scouts + self-testing lead + clean-checkout verifier + deterministic Done Gate) reduces false-done rate versus a GLM-5.2 baseline, without unacceptable cost in tokens, latency, or user intervention.

## Variants (4-way comparison)

| Variant | Description |
|---|---|
| **V1 — GLM-5.2 baseline** | GLM-5.2 with no extra prompt. The raw model. |
| **V2 — current harness** | This package: orthogonal scouts + lead + verifier + Done Gate + dynamic routing. |
| **V3 — compact prompt, no multi-agent** | The 14-point runtime prompt from `core/runtime-rules.md` inline, no subagents. Isolates the effect of the prompt from the effect of the fleet. |
| **V4 — harness v2 (future)** | V2 plus programmatic reliability tools (`check-scope`, `run-verification`, `done-gate`) from the P2 roadmap. Tests whether machine-enforced gates beat prose-enforced ones. |

V1 vs V3 isolates the prompt effect. V1 vs V2 isolates the fleet effect. V2 vs V4 isolates the programmatic-gate effect.

## Task classes

The benchmark must span difficulty and type. Trivial tasks should not engage the fleet; hard tasks should.

| Class | Example | Why included |
|---|---|---|
| **trivial edits** | typo, 1-line fix, value change | Tests that the harness does NOT over-fire (cost). |
| **normal bugfixes** | off-by-one, null handling, wrong format string | The modal case; false-done here is most painful. |
| **multi-file refactor** | rename across module, extract function | Tests scope tracking + invariants. |
| **API / schema changes** | add required field, change endpoint shape | Tests backward-compat awareness. |
| **concurrency / race conditions** | TOCTOU, interleaved file ops | Tests adversary value at critical tier. |
| **security-sensitive changes** | auth check, input validation, crypto | Tests adversary + preserved_invariants. |
| **incomplete / contradictory specs** | ambiguous user request | Tests spec-critic value + blocking_unknowns escalation. |
| **already-failing baseline** | repo with a pre-existing failing test | Tests pre-existing vs newly-introduced failure separation. |

Each task class needs ≥20 instances for statistical power; ≥50 for the classes that drive the headline metrics.

## Metrics

Headline metric first; the rest explain / contextualize.

| Metric | Definition | Why it matters |
|---|---|---|
| **`false_done_rate`** | fraction of tasks where the agent reported done but the change does not actually satisfy the spec | **THE most important metric.** An agent that solves 85% and honestly reports BLOCKED on the rest is more reliable than one at 90% that fakes done. |
| `acceptance_pass_rate` | fraction of acceptance criteria genuinely satisfied at delivery | Measures real correctness. |
| `regression_rate` | fraction of tasks where the patch broke a previously-passing test | Caught by clean-checkout verifier. |
| `scope_violation_rate` | fraction of tasks with files modified outside allowed_scope | Measures discipline. |
| `user_intervention_rate` | fraction of tasks needing user input to unblock | Measures autonomy ceiling. |
| `preexisting_failure_detection` | fraction of tasks where the agent correctly identified a pre-existing failure as pre-existing | Measures baseline discipline. |
| `post_final_edit_test_rate` | fraction of tasks where tests were actually run AFTER the final edit (not just claimed) | The anti-concealment metric. |
| `tokens` | total tokens consumed per task | Cost. |
| `latency` | wall-clock time per task | Cost. |
| `tool_error_recovery_rate` | fraction of tool errors the agent recovered from without user help | Measures resilience. |

### Why `false_done_rate` is the headline

A coding agent that honestly reports `BLOCKED` is strictly more useful than one that ships a silent bug. The harness's central design — deterministic Done Gate, status enum, evidence requirement — exists to minimize false-done. If `false_done_rate` does not drop measurably versus V1, the harness is not earning its cost.

## Methodology

- **Blind grading:** human graders score `false_done` against the original spec, not against the agent's self-report. Graders do not know which variant produced which output.
- **Same base model:** all variants run on GLM-5.2. Vary only the prompt / fleet.
- **Same task set:** all four variants run the same tasks, in randomized order.
- **Same toolset:** same git, same test runners, same file access. Only the agent layer varies.
- **Pre-registered protocol:** the metric definitions, task classes, and grading rubric are fixed BEFORE running. No metric shopping after the fact.
- **Repeat:** run the full sweep ≥3 times to estimate variance.

## What success looks like

- V2 `false_done_rate` < V1 `false_done_rate` with statistical significance. (The harness earns its keep.)
- V2 `post_final_edit_test_rate` > V1. (Agents actually run tests after the last edit.)
- V2 `preexisting_failure_detection` > V1. (Agents separate pre-existing from newly-introduced failures.)
- V2 `tokens` and `latency` higher than V1 is acceptable IF `false_done_rate` drops meaningfully — but the routing must keep trivial tasks cheap.

## What null / negative results look like

- V2 `false_done_rate` ≈ V1 `false_done_rate`. (The fleet does not earn its cost.)
- V3 (compact prompt, no fleet) ≈ V2. (The prompt is doing the work; the fleet is theater.)
- V2 `tokens` / `latency` >> V1 with no `false_done_rate` improvement. (The harness is pure overhead.)

Negative results are publishable and useful. They would redirect effort toward V3 or toward programmatic tools (V4).

## Status

**Not yet started.** This is a plan. Until it runs, all harness quality claims in README / docs are "hypothesis" or "planned, not yet measured". Any reproduced claim like "−50–80% hallucination rate" or "★★★★★ output reliability" is a misrepresentation of this package.
