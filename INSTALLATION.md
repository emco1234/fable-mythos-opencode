# Installation Guide — Fable & Mythos for OpenCode CLI

Complete walkthrough to install the MAP protocol in OpenCode CLI.

## Prerequisites

- **[OpenCode CLI](https://opencode.ai)** installed (v1.17+ recommended)
- Node.js 18+ (for npm-based installation)
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

# Copy the 5 agent definitions
mkdir -p ~/.config/opencode/agents
cp ~/fable-mythos-opencode/agents/*.md ~/.config/opencode/agents/
```

### Step 2 — Copy the Skill

```bash
mkdir -p ~/.config/opencode/skills
cp -r ~/fable-mythos-opencode/skills/fable-mythos-modus ~/.config/opencode/skills/
```

### Step 3 — Copy the Global Instructions

```bash
# If you don't have an AGENTS.md yet:
cp ~/fable-mythos-opencode/AGENTS.md ~/.config/opencode/AGENTS.md

# If you already have one (e.g., from Oh My OpenAgent), append the content instead:
cat ~/fable-mythos-opencode/AGENTS.md >> ~/.config/opencode/AGENTS.md
```

### Step 4 — Register in opencode.json

Open `~/.config/opencode/opencode.json` and merge the agent definitions from [`opencode.json`](./opencode.json) in this repo.

The key changes:
1. **Add the 5 agents** under `"agent"` (if you want them explicitly registered — OpenCode may also auto-discover from `agents/`)
2. **Ensure AGENTS.md is in instructions**:
   ```json
   "instructions": [
     "~/.config/opencode/AGENTS.md"
   ]
   ```
3. **Ensure permissions allow all tools** (OpenCode defaults to allowing everything, but verify):
   ```json
   "permission": {
     "bash": "allow",
     "read": "allow",
     "write": "allow",
     "edit": "allow",
     "agent": "allow",
     "skill": "allow"
   }
   ```

See the [`opencode.json`](./opencode.json) file in this repo for the full snippet.

### Step 5 — Restart OpenCode

```bash
opencode
```

OpenCode re-reads config at startup. The 5 mythos-* agents and the fable-mythos-modus skill should now be available.

## Verify Installation

### Check agents are available
In OpenCode, the 5 sub-agents should be invokable. Test:
```
Use mythos-executor to analyze this function and explain the trade-offs.
```

### Check skill is loaded
```
List the 10 Mythos principles.
```

The agent should respond with all 10 principles from the `fable-mythos-modus` skill.

### Check MAP fires
Give a genuinely non-trivial coding task:
```
Refactor this function to handle three new edge cases and explain the trade-offs.
```

You should observe the MAP protocol engaging — multiple agents working in sequence, ending with a confidence-rated delivery.

## Compatibility with Oh My OpenAgent (OmO)

If you use [Oh My OpenAgent](https://github.com/code-yeongyu/oh-my-opencode), both packages coexist without conflict:

- **OmO agents** (Sisyphus, Oracle, Prometheus, etc.) are defined in `oh-my-openagent.json`
- **Fable & Mythos agents** (mythos-executor, etc.) are defined in `agents/*.md` and `opencode.json`

They don't interfere. Use OmO for its specialized workflows and Fable & Mythos for the MAP verification protocol.

## Troubleshooting

### Agents not available
- Verify all 5 `.md` files are in `~/.config/opencode/agents/`
- Check frontmatter: each file must have `name`, `description`, `mode`, `tools`
- Verify `"agent"` key in `opencode.json` includes the 5 entries (or rely on auto-discovery)

### Skill not discovered
- Verify `~/.config/opencode/skills/fable-mythos-modus/SKILL.md` exists
- Check the frontmatter: `name` must match the directory name
- Ensure `"skill": "allow"` is set in `permission` block of `opencode.json`

### AGENTS.md not loaded
- Verify `"instructions": ["~/.config/opencode/AGENTS.md"]` is in `opencode.json`
- Check the path expands correctly (use `~/` or absolute path)

### MAP fires too aggressively (cost concerns)
Edit `~/.config/opencode/AGENTS.md` and tighten the trivial-override threshold.

## Uninstallation

```bash
# Remove agents
rm ~/.config/opencode/agents/mythos-*.md

# Remove skill
rm -rf ~/.config/opencode/skills/fable-mythos-modus

# Remove AGENTS.md (or restore from backup if you appended)
# Edit opencode.json to remove the 5 agent entries

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

- Read [`docs/MYTHOS-SYSTEM-CARD-ANALYSIS.md`](./docs/MYTHOS-SYSTEM-CARD-ANALYSIS.md) for the evidence base
- Read [`docs/ANTI-CONCEALMENT.md`](./docs/ANTI-CONCEALMENT.md) for the philosophy
- Star the repo if it helps
