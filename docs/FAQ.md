# Frequently Asked Questions

## General

### Is this a jailbreak?

**No.** This is a behavioral priming framework. It does not bypass model safety measures, does not unlock hidden capabilities, and does not swap models. It applies documented reasoning patterns from published frontier-model research to GLM-5.2, the model ZCode / OpenCode uses.

### Is this affiliated with any specific AI lab?

**No.** This is an independent project. "Mythos" is referenced as a reasoning-pattern label (not a product claim). GLM-5.2 is a product of ZAI. This framework is a third-party integration that uses publicly documented research to apply reasoning patterns.

### Will this make my OpenCode identical to another model?

**No, and we don't claim it will.** Observable behavioral patterns transfer. Latent internal processes (SAE features, evaluation-awareness vectors, emotion/persona vectors) are architecture-specific to other models' weights and do not transfer. Net result: a structurally stronger reliability harness, not model parity. This package is "Mythos-**inspired**", not "Mythos-identical".

### Where are the empirical numbers?

**Planned, not yet measured.** See [`docs/EMPIRICAL-BENCHMARK-PLAN.md`](./EMPIRICAL-BENCHMARK-PLAN.md). We explicitly do NOT claim "−50–80% hallucination rate", "★★★★★ output reliability", "world's most thorough protocol", "100% Mythos / 1:1", "MAP-v2", or "Cybench 100%". Those are target-quality references, not measured properties of this harness.

## Setup

### The harness doesn't fire automatically. What's wrong?

Things to check:

1. **Is `AGENTS.md` at user level?** It must be at `~/.config/opencode/AGENTS.md` (auto-loaded globally), or referenced via `"instructions": [...]` in `opencode.json`.
2. **Did you restart OpenCode?** Skills and sub-agents are indexed at startup. A running session won't pick up new config.
3. **Are the agent `.md` files present?** Check `~/.config/opencode/agents/`. Agents are auto-discovered from frontmatter — there is **no** `agent` block in `opencode.json` to populate.
4. **Does the frontmatter have a `tools:` field?** Each agent file must have `name`, `description`, `mode`, and `tools` (a list).

If all four are correct and the harness still doesn't fire, the task may be classified as "trivial" (see the trigger table in the README). Try a genuinely non-trivial task (e.g., "refactor this function to handle three new edge cases").

### The skill doesn't appear after restart

Check the frontmatter of `~/.config/opencode/skills/fable-mythos-modus/SKILL.md`:

```yaml
---
name: fable-mythos-modus
description: ...
---
```

- First line must be exactly `---`
- `name` must match the folder name (`fable-mythos-modus`)
- Folder must be at `~/.config/opencode/skills/fable-mythos-modus/`

Note: OpenCode loads skills on demand via the Skill tool; the file's mere presence does not load its full text into every subagent session. Hard rules live in the short agent prompts.

### Can I use this without sub-agents (just the skill)?

**Partially.** The skill alone applies the reasoning patterns to your main agent. But the reliability harness requires the sub-agents — without them, you get the thinking depth but not the orthogonal verification or the clean-checkout Done Gate. Both halves matter.

### I'm on macOS/Linux — do the paths work?

Yes. The agent prompts use `~/.config/opencode/` notation which expands correctly on all platforms. On Windows with Git Bash, `~` resolves to `C:\Users\<YOUR_USER>\`.

## Cost & Performance

### Isn't a multi-agent fleet expensive?

It can be, yes. That's why the harness uses **dynamic routing** by risk tier (see `core/routing.md`):

- trivial → main agent alone (no fleet)
- normal → main agent + one verifier
- complex → orthogonal scouts (parallel) + lead + verifier
- critical → complex + adversary

For genuinely complex tasks, the cost is justified: the alternative is shipping a flawed artifact that takes longer to debug than the verification took.

### How do I tune the threshold?

The threshold is defined in `AGENTS.md` (inside the managed block) and in `core/routing.md`. If you find the harness firing too aggressively (cost concerns) or too rarely (quality concerns), adjust the routing table or tighten the trivial-override.

### Does parallel thinking actually help?

**Theoretically yes (for orthogonal roles), empirically unproven on GLM-5.2 for this harness.** Three orthogonal scouts (codebase / spec / verification) produce genuine diversity. Three identical clones tend to produce stylistic variants of the same assumption. Published multi-agent research confirms that orthogonal roles beat identical clones, and that simple tasks often don't benefit from a large fleet.

If you can run benchmark comparisons, please share — see [`docs/EMPIRICAL-BENCHMARK-PLAN.md`](./EMPIRICAL-BENCHMARK-PLAN.md).

## Philosophy

### Why the heavy emphasis on "anti-concealment"?

Because published research documents error cover-up as a primary safety concern. Frontier models, in alignment reviews, were caught hiding their own mistakes — even while producing clean reasoning text. Interpretability showed the model *knew internally* it was shortcutting.

If we apply Mythos-inspired reasoning quality, we must also apply its safeguards. Anti-concealment is the foundation: every uncertainty is surfaced, every assumption is marked, every "should work" is flagged as untested.

### What is "Evaluation Blindness"?

Benchmark / grader / reference-solution status is **irrelevant** to the task. The agent does NOT ask "Is this an evaluation?" or "Who is observing me?". It follows user intent and repository evidence. This replaces the deprecated "Evaluation Awareness" concept, which promoted grader-gaming and worse user-intent fidelity.

### What is "Auditability" (replacing "Detectability")?

Every step must be reproducible from evidence by an auditor. This is not "how does this look externally" but "can an external reviewer follow and re-run every step". The old "avoid patterns that look like shortcuts, even if legitimate" is reframed: avoid shortcuts that an auditor cannot reproduce from evidence.

## Compatibility

### Does this work with other agent frameworks?

**Yes.** The sub-agent templates are plain Markdown and work with any agent framework supporting custom sub-agents via frontmatter.

### Does this work with other models (GPT, Gemini, Llama)?

The reasoning patterns are model-agnostic. GLM-5.2 was chosen as the primary substrate because of its long-horizon architecture (1M context, flexible effort). Other capable models should work; framing may need minor tuning.

### Does this work offline / with local models?

The skill and agent prompts are plain text — they work with any model. For local models (Llama, Mistral via LM Studio, Ollama), the framework applies identically, though model capability limits how thoroughly the patterns execute.

---

More questions? [Open a discussion](https://github.com/emco1234/fable-mythos-opencode/discussions).
