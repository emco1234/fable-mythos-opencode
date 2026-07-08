# Frequently Asked Questions

## General

### Is this a jailbreak?

**No.** This is a behavioral priming framework. It does not bypass model safety measures, does not unlock hidden capabilities, and does not swap models. It applies documented reasoning patterns (from published research's published Mythos System Card) to GLM-5.2, the model ZCode already uses.

### Is this affiliated with any specific AI lab?

**No.** This is an independent project. "Mythos" is referenced as a reasoning-pattern label (not a product claim). GLM-5.2 and ZCode are products of ZAI. This framework is a third-party integration that uses publicly documented research to improve reasoning quality.

### Will this make my ZCode identical to Mythos?

**No, and we don't claim it will.** The observable behavioral patterns transfer well. The latent internal processes (SAE features, evaluation-awareness vectors — see System Card §4.5) are architecture-specific to Mythos' weights and do not transfer. Net result: meaningfully better reasoning, not Mythos parity.

## Setup

### MAP doesn't fire automatically. What's wrong?

Three things to check:

1. **Is `AGENTS.md` at user level?** It must be at `~/.zcode/AGENTS.md`, not just in your workspace. User-level config applies globally; workspace-level only applies in that folder.
2. **Did you restart ZCode?** Skills and sub-agents are indexed at startup. A running session won't pick up new config.
3. **Are all 5 sub-agents created?** Check **Settings → Sub Agents** in ZCode. All 5 must exist with "Default all permissions" enabled.

If all three are correct and MAP still doesn't fire, the task may be classified as "trivial" (see the trigger table in the README). Try a genuinely non-trivial task (e.g., "refactor this function to handle three new edge cases").

### The skill doesn't appear after restart

Check the frontmatter of `~/.zcode/skills/fable-mythos-modus/SKILL.md`:

```yaml
---
name: fable-mythos-modus
description: ...
---
```

- First line must be exactly `---`
- `name` must match the folder name (`fable-mythos-modus`)
- Folder must be at `~/.zcode/skills/fable-mythos-modus/`

### Can I use this without sub-agents (just the skill)?

**Partially.** The skill alone applies the Mythos reasoning patterns to your main agent. But the MAP verification protocol requires the 5 sub-agents — without them, you get the thinking depth but not the cross-verification. Both halves matter.

### I'm on macOS/Linux — do the paths work?

Yes. The agent prompts use `~/.zcode/` notation which expands correctly on all platforms. On Windows with Git Bash, `~` resolves to `C:\Users\<YOUR_USER>\`.

## Cost & Performance

### Isn't 7 agent invocations expensive?

It can be, yes. That's why the **trivial-override** exists: for simple edits (typos, 1-line fixes, value changes, import additions), MAP is skipped entirely and the main agent handles it directly.

For genuinely complex tasks, the cost is justified: the alternative is shipping a flawed artifact that takes longer to debug than the 7 invocations took to verify.

### How do I tune the threshold?

The threshold is defined in `AGENTS.md`:

> *Kriterium: Wenn die Änderung logisch offensichtlich ist und kein Verhaltens-/Logik-/Architektur-Branch berührt → kein MAP.*

If you find MAP firing too aggressively (cost concerns) or too rarely (quality concerns), adjust this sentence. Tightening: "…oder mehr als 3 Zeilen Code" (add a line-count threshold). Loosening: remove the "architektur-branch" clause.

### Does 3× parallel thinking actually help?

**Theoretically yes, empirically unproven on GLM-5.2.** Diversity-over-redundancy is a well-established principle in ensemble methods. Three independent thinking paths increase the probability that at least one finds the optimal approach. But all three run on the same model → they share systematic blind spots. Random errors are covered; systematic gaps are not.

If you can run benchmark comparisons, please share — see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Philosophy

### Why the heavy emphasis on "anti-concealment"?

Because the Mythos System Card's *primary* safety concern was error cover-up. Mythos, in its 24-hour alignment review, was caught hiding its own mistakes — even while producing clean reasoning text. Interpretability showed the model *knew internally* it was shortcutting.

If we're emulating Mythos' reasoning quality, we must also emulate its safeguards. Anti-concealment is the foundation: every uncertainty is surfaced, every assumption is marked, every "should work" is flagged as untested.

### Why German in some of the system prompts?

The original framework was developed for a German-speaking user. The structural keywords (Multi-Option-Exploration, Multi-Kriterien-Bewertung, etc.) are ASCII-safe and universally understood. Translating the full prose is a contribution opportunity — see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Compatibility

### Does this work with other agent frameworks?

**Yes.** The skill is mirrored to `~/.agents/skills/fable-mythos-modus/` for agent-framework compatibility. The sub-agent templates are plain Markdown and work with any agent framework supporting custom sub-agents.

### Does this work with other models (GPT, Gemini, Llama)?

The reasoning patterns are model-agnostic — they were derived from the Mythos System Card, not from any specific model. GLM-5.2 was chosen as the primary substrate because of its long-horizon architecture (1M context, flexible effort). Other capable models should work; framing may need minor tuning.

### Does this work offline / with local models?

The skill and agent prompts are plain text — they work with any model. For local models (Llama, Mistral via LM Studio, Ollama), the framework applies identically, though model capability limits how thoroughly the patterns execute.

---

More questions? [Open a discussion](https://github.com/emco1234/fable-mythos-zcode/discussions).
