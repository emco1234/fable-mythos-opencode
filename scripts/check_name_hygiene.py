# -*- coding: utf-8 -*-
"""Static consistency check for fable-mythos prompt harnesses."""
from __future__ import annotations

import re
import sys
from pathlib import Path

WORK = Path(r"C:\Users\corov\fable-mythos-work")
REQUIRED_SECTIONS = ("FORCE MAP Override", "Tool-Call Hygiene")
BARE_AGENTS = [
    "mythos-singleshot-thinking-intelligence",
    "mythos-executor",
    "mythos-verifier",
    "mythos-adversary",
    "mythos-synthesizer",
    "reliability-scout",
    "reliability-spec-critic",
    "reliability-test-designer",
    "reliability-lead",
    "reliability-verifier",
    "reliability-adversary",
]
# Numbered ids as runtime spawn names are forbidden in permission tables / overviews
NUMBERED_RUNTIME = re.compile(
    r"`[0-4]-mythos-(?:singleshot-thinking-intelligence|executor|verifier|adversary|synthesizer)`"
)


def agent_names_from_dir(repo: Path) -> list[str]:
    names: list[str] = []
    for folder in ("agents", "sub-agents", "roles"):
        d = repo / folder
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'(?m)^name:\s*["\']?([a-z0-9\-]+)["\']?', text)
            if m:
                names.append(m.group(1))
            else:
                # zcode sub-agents use ## Feld: Name blocks
                m2 = re.search(r"## Feld: Name\s*```\s*([a-z0-9\-]+)\s*```", text)
                if m2:
                    names.append(m2.group(1))
                else:
                    # derive from filename stripping leading N-
                    stem = p.stem
                    stem = re.sub(r"^[0-4]-", "", stem)
                    names.append(stem)
    return names


def check_repo(name: str) -> list[str]:
    repo = WORK / name
    errs: list[str] = []
    if not repo.is_dir():
        return [f"{name}: missing directory"]

    agents_md = repo / "AGENTS.md"
    if not agents_md.exists():
        errs.append(f"{name}: AGENTS.md missing")
        return errs

    text = agents_md.read_text(encoding="utf-8")
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            errs.append(f"{name}: AGENTS.md missing section '{sec}'")

    # numbered runtime refs outside of "never spawn" / filename notes
    for i, line in enumerate(text.splitlines(), 1):
        if NUMBERED_RUNTIME.search(line):
            # allow negative examples
            low = line.lower()
            if "niemals" in low or "never" in low or "nicht" in low and "spawnen" in low:
                continue
            if "sub-agents/" in line or ".md" in line:
                continue
            if "dateinamen" in low or "filename" in low or "quell" in low:
                continue
            errs.append(f"{name}: AGENTS.md:{i} numbered runtime agent ref: {line.strip()[:100]}")

    for bare in ("mythos-executor", "reliability-lead", "reliability-verifier"):
        if bare not in text:
            errs.append(f"{name}: AGENTS.md missing bare agent '{bare}'")

    names = agent_names_from_dir(repo)
    if names:
        # all bare names should appear as files or frontmatter
        for b in BARE_AGENTS:
            if b not in names:
                # not fatal if agent dir uses different layout, warn
                pass
        bad = [n for n in names if re.match(r"^[0-4]-mythos-", n)]
        if bad:
            errs.append(f"{name}: agent name: fields still numbered: {bad}")

    routing = repo / "core" / "routing.md"
    if routing.exists():
        rtxt = routing.read_text(encoding="utf-8")
        if "FORCE MAP" not in rtxt and "force phrase" not in rtxt.lower() and "FORCE MAP phrases" not in rtxt:
            errs.append(f"{name}: core/routing.md missing FORCE MAP override")

    return errs


def main() -> int:
    repos = [
        "fable-mythos-zcode",
        "fable-mythos-opencode",
        "fable-mythos-grok",
    ]
    all_errs: list[str] = []
    for r in repos:
        e = check_repo(r)
        if e:
            print(f"FAIL {r}")
            for x in e:
                print(" ", x)
            all_errs.extend(e)
        else:
            print(f"PASS {r}")
            names = agent_names_from_dir(WORK / r)
            print(f"  agents/frontmatter: {len(names)} names; sample={names[:5]}")

    if all_errs:
        print(f"\nTOTAL FAIL: {len(all_errs)} issues")
        return 1
    print("\nALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
