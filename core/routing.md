# Dynamic Routing

> The harness is NOT a fixed 7-agent fleet on every task. It routes by risk tier: trivial work uses no agents; critical work uses the full fleet including the adversary. This kills the cost problem (3 identical thinking clones on every normal change) while keeping the verification depth where it matters.

## Routing table

| Risk tier | Phase 0 (scouts) | Phase 1 (implement) | Phase 2 (verify) | Done Gate |
|---|---|---|---|---|
| **trivial** | none | main agent alone | none | main agent's self-check |
| **standard** | none | main agent (self-tests) | reliability-verifier (clean checkout) | Done Gate |
| **complex** | reliability-scout + reliability-spec-critic + reliability-test-designer (parallel) | reliability-lead (self-tests) | reliability-verifier (clean checkout) | Done Gate |
| **critical** | complex + (optionally) mythos-singleshot-thinking-intelligence (legacy fallback) | reliability-lead (self-tests) | reliability-verifier (clean checkout) + reliability-adversary (isolated worktree) | Done Gate |

## Risk-tier classification

The spec-critic proposes the tier; the orchestrator confirms it. Classification criteria:

- **trivial** — typo, 1-line fix, CSS value change, import addition. No logic / behavior / architecture branch touched. The main agent handles it directly; no fleet.
- **standard** — small bugfix or feature with clear spec and existing test coverage. Main agent implements + self-tests; one verifier on clean checkout.
- **complex** — multi-file change, refactoring, API/schema change, non-obvious bug, or anything touching security/concurrency-adjacent code. Full orthogonal scouts (parallel) → lead → verifier.
- **critical** — security-sensitive, data-loss-sensitive, irreversible (migration, deployment), or high-blast-radius. Complex fleet + adversary in isolated worktree. The adversary is mandatory here, not optional.

**On ambiguity** ("trivial or not?") → bump UP, not down. In doubt, verify.

## Why not 3 identical thinking clones on every task

The legacy design fired `mythos-singleshot-thinking-intelligence` 3× in parallel on every non-trivial task. Three instances with the same model, same prompt, same context, same role tend to produce stylistic variants of the same assumption. Published multi-agent research confirms:

- Orthogonal roles (codebase / spec / verification) produce genuine diversity; identical clones do not.
- Simple tasks often do not benefit from a large agent fleet; coordination cost can eat the benefit.
- Non-blocking, long-lived agents beat a blocking orchestrator with a fixed pipeline.

The orthogonal scouts (reliability-scout / -spec-critic / -test-designer) are the default Phase 0. The legacy 3× MST fleet is kept as an optional fallback, used at critical tier or on explicit request.

## Orchestrator contract

The orchestrator (main agent) is the router. Its responsibilities:

1. **Classify** the task into a risk tier (default: standard; bump up on ambiguity).
2. **Dispatch** Phase 0 scouts in parallel (complex / critical only).
3. **Collect** scout outputs; check for `blocking_unknowns` before authorizing the lead to implement.
4. **Dispatch** the lead (standard: the main agent itself implements; complex / critical: reliability-lead subagent).
5. **Receive** the frozen patch + self-verification evidence from the lead.
6. **Dispatch** the verifier with a fresh worktree at `base_commit` + the frozen patch.
7. **Dispatch** the adversary (critical only) with an isolated worktree.
8. **Read** the verification report(s); apply the Done Gate.
9. **On PARTIALLY_VERIFIED / BLOCKED** — bundle findings into a repair brief; loop (max 3); then escalate to user.

## Cost notes

- Trivial tasks cost zero subagent invocations.
- Standard tasks cost one verifier invocation.
- Complex tasks cost 3 scouts + 1 lead + 1 verifier = 5 invocations.
- Critical tasks cost up to 3 scouts + 1 lead + 1 verifier + 1 adversary = 6 invocations.
- Each repair loop adds 1 lead + 1 verifier (+ 1 adversary at critical) = 2-3 invocations.

Compare to the legacy fixed pipeline (3 MST + 1 executor + 1 verifier + 1 adversary + 1 synthesizer = 7 invocations on every non-trivial task). Dynamic routing is cheaper on trivial / standard work and the same or cheaper on complex work, with real diversity instead of stylistic clones.

## When the orchestrator IS the lead

At standard tier, the main agent implements directly and self-tests. This is fine — the cost is in the independent clean-checkout verification, not in spawning a lead subagent for a small change. At complex / critical tier, the lead is a subagent so the main agent can retain global context while the lead focuses.

## Override (user-specified)

1. **Task contract:** The user may force a `risk_tier` in the task contract (`risk_tier: critical`). The router honors the user's choice even if classification would have picked a lower tier.
2. **FORCE MAP phrases (binding):** If the user says any of `feuer den map mode`, `fire map mode`, `MAP Mode`, `starte MAP`, `run MAP`, `full MAP`, `alle 11 agents`, `full reliability fleet` (case-insensitive), the orchestrator MUST run the full registered MAP fleet autonomously (see AGENTS.md "FORCE MAP Override"). Dynamic skip is forbidden for that turn.
3. **Agent runtime names** are always bare: `mythos-executor`, not `1-mythos-executor`. Numbered filenames in the repo are source organization only.

## Goal Mode interaction (anti-hang)

Do **not** nest ZCode/OpenCode/Grok Goal Mode as a multi-hour outer loop around full MAP fleets.
MAP subagents must be short, foreground (or hard-timeout ≤ 20 min), and chunked (max 3–5 files per executor unit).
If Goal Mode is active, use it only as a checklist; execute each MAP unit as a bounded subagent, never as a detached background marathon.

