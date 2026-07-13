# Reliability Roadmap

> This document tracks the P2 / P3 goals for the reliability harness: the features that move it from "structurally stronger prompting" toward "frontier-level agentik". Derived from the external analysis (`anpassungen.md`) and from published multi-agent research.

## Current state (after P0 / P1)

What the harness already enforces structurally:

- Dynamic routing by risk tier (trivial / standard / complex / critical).
- Orthogonal read-only scouts (codebase / spec / verification) instead of 3 identical thinking clones.
- Lead engineer MUST self-test before handoff.
- Independent clean-checkout verifier on a fresh worktree with a frozen patch.
- Adversary at critical tier only, in an isolated worktree.
- Deterministic Done Gate — an LLM cannot override a failed test.
- Task Contract schema (`core/task-contract.schema.json`) and Verification Report schema (`core/verification-report.schema.json`).
- Evidence Ledger (`core/evidence-ledger.md`) — append-only, compaction-proof.
- Evaluation Blindness hard rule (no grader-gaming, no "who is observing me?" reasoning).
- Auditability replaces Detectability; Evidence Traceability replaces Plausible Deniability.
- Least-privilege `tools:` frontmatter on every agent.
- Idempotent managed-block installer for `AGENTS.md`.

What it does NOT yet do — see the P2 / P3 sections below.

## P2 — Real agentik

Goals that move the harness from "best-effort prompting with structural gates" to "persistent, memory-equipped, language-aware agents".

### 1. Long-lived agents instead of restart-per-subtask

Today each subagent starts fresh. A long-lived scout that has already mapped the codebase once should retain that map for follow-up tasks in the same session.

- **Goal:** agents persist across turns within a session, with incremental context updates.
- **Open question:** platform support in OpenCode (subagent lifecycle) and ZCode (foreground / background subagents).

### 2. Persistent structured task memory

Today the Task Contract is re-derived per task. A structured memory would let the harness carry contracts, evidence, and residual unknowns across tasks in the same project.

- **Goal:** a project-scoped memory store (separate from the Evidence Ledger, which is per-task) that holds cross-task invariants, known-fragile areas, and previously-resolved ambiguities.
- **Format:** structured (JSON / YAML), versioned in `.reliability/` or similar, gitignored or committed by choice.

### 3. Compaction that never drops Task Contract or Evidence Ledger

OpenCode / ZCode compact long contexts. The harness must mark the Task Contract and Evidence Ledger as must-preserve.

- **Goal:** orchestrator explicitly tags these as compaction-proof. Compaction may summarize prose; it MUST NOT drop ledger entries or contract MUSTs.
- **Today:** documented as an invariant in `core/evidence-ledger.md`; not yet machine-enforced.

### 4. Async subagents (where the platform allows)

ZCode custom subagents currently run in the foreground; OpenCode subagents are invoked via the task tool. Both make a fixed blocking pipeline expensive.

- **Goal:** long-running scouts (especially the test-designer running its repro) run async; the orchestrator collects results when ready rather than blocking.
- **Open question:** platform async support.

### 5. Programmatic reliability tools / custom tool calling

Today the harness reasons in prose. A custom tool that returns `git diff --name-only` vs `allowed_scope`, or that runs the verification commands and emits a structured report, would be more reliable than prose reasoning.

- **Goal:** custom OpenCode tools:
  - `check-scope` — diff vs. allowed_scope, returns scope_violations[].
  - `run-verification` — runs the verifier's command list, returns structured evidence[].
  - `done-gate` — reads the ledger + contract, returns VERIFIED / PARTIALLY_VERIFIED / BLOCKED with the failing conditions.
- **Today:** these are prose procedures in `core/runtime-rules.md`.

### 6. Repair loops driven by structured findings

Today the repair brief is prose. A structured repair brief (machine-readable list of failing ACs + scope violations + adversary findings) would let the lead focus on exactly what the gate rejected.

- **Goal:** the Done Gate emits a structured repair brief the lead consumes directly.

### 7. Language / framework-specific check modules

Different stacks need different verification commands (jest vs pytest vs cargo test vs go test). Today the test-designer derives them from repo docs / CI; a library of per-stack modules would be more reliable.

- **Goal:** a `modules/<stack>.md` library (python, node, rust, go, etc.) that the test-designer loads on demand.

## P3 — Frontier level

Goals that approach documented frontier-model coding strength via tooling, not via pretending to move weights.

### 1. Property-based testing

Hypothesis (Python), fast-check (JS), proptest (Rust), gopter (Go). Generate edge cases the human-written test suite misses.

- **Goal:** the test-designer proposes property-based tests for any function with a clear invariant.

### 2. Fuzzing and sanitizers

libFuzzer, AFL, AddressSanitizer, ThreadSanitizer, MemorySanitizer. The adversary at critical tier should be able to invoke these.

- **Goal:** adversary runs fuzz targets in its isolated worktree and reports crashes as CRITICAL findings.

### 3. Mutation testing for critical logic

mutmut (Python), Stryker (JS), cargo-mutants (Rust). If mutating the patch does not fail any test, the test suite is insufficient.

- **Goal:** at critical tier, mutation testing runs against the patch; surviving mutants become findings.

### 4. Differential tests against old version or reference implementation

Run the old and new version side by side on the same inputs; any divergence is either the intended fix or a regression.

- **Goal:** the verifier runs differential tests when a reference behavior exists.

### 5. Optional second model or static analyzer as independent checker

A different model (or a static analyzer: Semgrep, CodeQL, PSRule) has different blind spots than GLM-5.2.

- **Goal:** at critical tier, the verifier optionally delegates the static-analysis pass to a different engine.

### 6. Telemetry on real failure modes and continuous prompt / harness ablation

The harness should measure itself. Which phase catches which error? Which prompt ablation improves `false_done_rate`?

- **Goal:** opt-in telemetry feeds the empirical benchmark plan (`docs/EMPIRICAL-BENCHMARK-PLAN.md`).

## Explicitly out of scope

- "Activate latent Mythos processes" — impossible; those live in weights, not prompts.
- "100% / 1:1 Mythos parity" — dishonest claim; removed from all copy.
- Guaranteeing no false-done ever — the goal is **never falsely claim done**, which is a different and achievable target.
