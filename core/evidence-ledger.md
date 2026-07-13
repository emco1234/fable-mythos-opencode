# Evidence Ledger

> A persistent, structured record of every verification-relevant observation in a task. Written by the lead (self-verification), the verifier (clean-checkout), and the adversary (critical tier). Consumed by the deterministic Done Gate.

## Purpose

The Evidence Ledger solves two failure modes:

1. **Context compaction drops load-bearing details.** Long trajectories get compacted; without a persistent, explicitly-protected ledger, an early failing test or a preserved-invariant constraint silently disappears. The ledger is **never** dropped by compaction — it is marked as must-preserve context.
2. **"X% confident" without calibration.** The ledger replaces uncalibrated percentages with concrete, observable evidence. Status is derived from the ledger contents, not from vibes.

## Structure

The ledger is an append-only list of evidence entries. Each entry matches the `evidence[]` item shape in `core/verification-report.schema.json`:

```yaml
- task_id: task-2026-07-13-<slug>
  phase: self-verification | clean-checkout | adversary
  agent: reliability-lead | reliability-verifier | reliability-adversary
  command: "npm test -- --grep AC1"
  result: |
    FAIL  src/foo.test.js
      ● foo › returns empty array on null input
        Expected: []
        Received: TypeError
  passed: false
  timestamp: 2026-07-13T14:22:03Z
  worktree: /tmp/reliability-verify-7f3a2
  notes: "Pre-existing? No — passes on base_commit. Introduced by patch."
```

## Required fields

- **task_id** — references `task-contract.task_id`.
- **phase** — which phase produced this entry.
- **agent** — which agent produced this entry.
- **command** — exact command executed.
- **result** — observed output, quoted (not paraphrased). Load-bearing detail preserved.
- **passed** — oracle result.
- **timestamp** — for ordering and for separating pre-existing vs. newly-introduced failures.
- **worktree** — where the command ran (lead's working dir vs. verifier's clean checkout vs. adversary's isolated worktree).
- **notes** — optional context (e.g., "pre-existing failure, not introduced by patch").

## Invariants

1. **Append-only.** Never edit or delete an entry. Corrections are new entries that reference the old one.
2. **Compaction-proof.** The orchestrator MUST mark the ledger as must-preserve context. Compaction may summarize prose; it MUST NOT drop ledger entries.
3. **No entry without an executed command.** `result` is observed output, not a prediction.
4. **Quoted, not paraphrased.** If a test failure message says `Expected: []  Received: TypeError`, that is what goes in `result`.
5. **Mapped to acceptance criteria.** Every AC in the contract must have at least one ledger entry (PASS or FAIL). UNVERIFIED ACs are an explicit status, not an omission.

## Done Gate consumption

The Done Gate reads the ledger and derives status:

- Every MUST → at least one entry with `passed: true`.
- Every AC → PASS backed by an entry.
- No entry with `passed: false` and severity CRITICAL/HIGH remains unresolved.
- Final clean-checkout entries exist (not just lead self-verification entries).

If the ledger is empty or missing required entries, status is UNVERIFIED — never VERIFIED.

## Pre-existing vs. newly-introduced failures

The ledger separates them via timestamp + worktree:

- Failures observed in the verifier's clean-checkout worktree on `base_commit` (before applying the patch) are **pre-existing**.
- Failures observed only after applying the patch are **newly-introduced**.

Only newly-introduced failures count against the patch. Pre-existing failures are documented but do not block VERIFIED (unless the contract explicitly required fixing them).

## Relationship to schemas

- `core/task-contract.schema.json` — defines what the ledger must back (MUSTs, acceptance_criteria).
- `core/verification-report.schema.json` — the ledger's `evidence[]` section is the structured projection the Done Gate reads.
