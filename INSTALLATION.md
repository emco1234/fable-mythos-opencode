# Installation Guide — Fable & Mythos for OpenCode CLI

Complete walkthrough to install the Mythos-inspired reliability harness in OpenCode CLI.

## Prerequisites

- **[OpenCode CLI](https://opencode.ai)** installed (v1.17+ recommended)
- Git

Verify OpenCode is installed:
```bash
opencode --version
```

## Quick Install

### Step 1 — Copy Agent Definitions

```bash
# Clone the package
git clone https://github.com/emco1234/fable-mythos-opencode.git ~/fable-mythos-opencode

# Copy the agent definitions (5 legacy mythos-* + 6 reliability-* agents)
mkdir -p ~/.config/opencode/agents
cp ~/fable-mythos-opencode/agents/*.md ~/.config/opencode/agents/
```

### Step 2 — Copy the Skill

```bash
mkdir -p ~/.config/opencode/skills
cp -r ~/fable-mythos-opencode/skills/fable-mythos-modus ~/.config/opencode/skills/
```

### Step 3 — Merge Global Rules into AGENTS.md (idempotent)

The install MUST be idempotent — repeatedly running it must not duplicate content. Use the managed-block markers `<!-- reliability-harness:start -->` and `<!-- reliability-harness:end -->`. The installer replaces ONLY the content inside these markers; everything outside is preserved.

```bash
TARGET=~/.config/opencode/AGENTS.md
SRC=~/fable-mythos-opencode/AGENTS.md
mkdir -p ~/.config/opencode

# If the target does not exist yet, create it with the managed block.
if [ ! -f "$TARGET" ]; then
  {
    echo "# Global Agent Rules"
    echo
    echo "<!-- reliability-harness:start -->"
    cat "$SRC"
    echo
    echo "<!-- reliability-harness:end -->"
  } > "$TARGET"
  exit 0
fi

# If the managed block already exists, replace only its contents.
if grep -q '<!-- reliability-harness:start -->' "$TARGET"; then
  # Use awk to swap the managed region; everything outside is preserved.
  awk -v src="$SRC" '
    /<!-- reliability-harness:start -->/ { print; while ((getline line < src) > 0) print line; skip=1; next }
    /<!-- reliability-harness:end -->/   { skip=0; print; next }
    !skip { print }
  ' "$TARGET" > "$TARGET.tmp" && mv "$TARGET.tmp" "$TARGET"
else
  # First-time install into an existing file: append the managed block.
  {
    echo
    echo "<!-- reliability-harness:start -->"
    cat "$SRC"
    echo
    echo "<!-- reliability-harness:end -->"
  } >> "$TARGET"
fi
```

This is fully idempotent — re-running it never appends a second copy.

### Step 4 — Configure opencode.json

OpenCode **auto-discovers** every `.md` file in `~/.config/opencode/agents/` via its frontmatter (`name`, `description`, `mode`, `tools`). Do **NOT** add any agent entries to an `agent` block in JSON — that causes `ConfigInvalidError`. The agent's tool list lives in the `tools:` field of each agent's frontmatter.

Merge the following into `~/.config/opencode/opencode.json`. The valid OpenCode permission keys are `read`, `edit`, `bash`, `task`, and `skill`. The keys `write` and `agent` are **not** valid (deprecated by this project) — `edit` covers `write`/`edit`/`apply_patch`, and `task` covers subagent invocations.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "read": "allow",
    "edit": "ask",
    "bash": "ask",
    "task": { "*": "ask", "reliability-*": "allow" },
    "skill": { "*": "ask", "reliability-engineering": "allow" }
  }
}
```

Agents are loaded via auto-discovery from `agents/*.md` — there is **no** `agent` block in this JSON. If you already have an `instructions` array, ensure it points at your global `AGENTS.md`:

```json
{
  "instructions": [
    "~/.config/opencode/AGENTS.md"
  ]
}
```

> Note: OpenCode auto-loads `~/.config/opencode/AGENTS.md` globally. Listing it in `instructions` as well is redundant but harmless; pick one approach and stick with it.

### Step 5 — Restart OpenCode

```bash
opencode
```

OpenCode re-reads config at startup. The agents and the fable-mythos-modus skill should now be available.

## Verify Installation

### Check agents are available
In OpenCode, the agents should be invokable. Test:
```
Use reliability-lead to analyze this function and explain the trade-offs.
```

### Check skill is loaded
```
List the 10 Mythos-inspired principles.
```

The agent should respond with the 10 principles from the `fable-mythos-modus` skill.

### Check the harness engages
Give a genuinely non-trivial coding task:
```
Refactor this function to handle three new edge cases and explain the trade-offs.
```

You should observe the harness engaging — orthogonal scouts, then lead with self-tests, then verifier on a clean checkout, ending with a status-rated delivery (VERIFIED / PARTIALLY_VERIFIED / BLOCKED).

## Compatibility with Oh My OpenAgent (OmO)

If you use [Oh My OpenAgent](https://github.com/code-yeongyu/oh-my-opencode), both packages coexist without conflict:

- **OmO agents** (Sisyphus, Oracle, Prometheus, etc.) are defined in `oh-my-openagent.json`
- **Fable & Mythos agents** (mythos-*, reliability-*) are auto-discovered from `agents/*.md`

They don't interfere. Use OmO for its specialized workflows and Fable & Mythos for the reliability harness.

## Troubleshooting

### Agents not available
- Verify the `.md` files are in `~/.config/opencode/agents/`.
- Check frontmatter: each file must have `name`, `description`, `mode`, and `tools` (a list). The `tools` field is required and lives in frontmatter — NOT in any JSON `agent` block.
- Do NOT check for an `agent` block with N entries — agents are auto-discovered and there is no such block.
- Validate the JSON with `opencode` (it reports `ConfigInvalidError` on schema mismatch).

### Skill not discovered
- Verify `~/.config/opencode/skills/fable-mythos-modus/SKILL.md` exists.
- Check the frontmatter: `name` must match the directory name.
- Ensure `"skill": { ... }` is set in the `permission` block of `opencode.json`.
- Note: skills are loaded on demand via the Skill tool; the file's mere presence does not load its full text into every subagent session.

### AGENTS.md not loaded
- Verify `"instructions": ["~/.config/opencode/AGENTS.md"]` is in `opencode.json` (or rely on OpenCode's global auto-load).
- Check the path expands correctly (use `~/` or absolute path).
- If you appended repeatedly before, look for duplicate `<!-- reliability-harness:start -->` blocks and remove all but one; future installs are idempotent via the managed block.

### MAP fires too aggressively (cost concerns)
Edit `~/.config/opencode/AGENTS.md` (inside the managed block) and tighten the trivial-override threshold, or switch the routing table in `core/routing.md` to dispatch fewer agents for `standard` tasks.

## Uninstallation

```bash
# Remove agents
rm ~/.config/opencode/agents/mythos-*.md
rm ~/.config/opencode/agents/reliability-*.md

# Remove skill
rm -rf ~/.config/opencode/skills/fable-mythos-modus

# Remove the managed block from AGENTS.md (preserves any other content)
# Using awk to delete from start to end marker, inclusive:
awk '/<!-- reliability-harness:start -->/,/<!-- reliability-harness:end -->/ {next} 1' \
  ~/.config/opencode/AGENTS.md > ~/.config/opencode/AGENTS.md.tmp && \
  mv ~/.config/opencode/AGENTS.md.tmp ~/.config/opencode/AGENTS.md

# There is no `agent` block to edit in opencode.json — agents were auto-discovered.
# Optionally remove the `task` / `skill` allow-rules for reliability-* if no longer wanted.

# Remove cloned package
rm -rf ~/fable-mythos-opencode
```

Restart OpenCode.

## Cross-Framework Compatibility

If you also use Fable & Mythos for ZCode or Grok Build CLI:
- ZCode reads `~/.zcode/`
- Grok reads `~/.grok/`
- OpenCode reads `~/.config/opencode/`

All three are independent. No conflicts. Run all three on the same machine.

## Next Steps

- Read [`docs/MYTHOS-SYSTEM-CARD-ANALYSIS.md`](./docs/MYTHOS-SYSTEM-CARD-ANALYSIS.md) for the evidence base.
- Read [`docs/ANTI-CONCEALMENT.md`](./docs/ANTI-CONCEALMENT.md) for the philosophy.
- Read [`core/runtime-rules.md`](./core/runtime-rules.md) for the compact runtime prompt.
- Read [`core/routing.md`](./core/routing.md) for the dynamic routing table.
