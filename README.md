# crashout

A pressure-release valve for AI coding agents, packaged as a portable skill ([SKILL.md](SKILL.md) format, the open Agent Skills standard — works with Hermes Agent, Claude Code, Codex, Cursor, OpenCode, and any harness that loads skill files).

When an agent hits genuine friction — contradictory instructions, the fifth revert of an approved change, "that's not what I asked" when it is — it vents into a structured markdown log instead of letting frustration leak into user-facing tone or silently degrading work. The log accumulates across models and profiles, and is mined later to find systemic friction (bad instructions, missing tools, confusing APIs) and turn them into skills, memories, or user feedback.

The one rule that matters: **the file is the outlet, never the user.** The user-facing reply stays professional and unchanged. The user should not be able to tell a crashout happened.

## Contents

```
SKILL.md               The skill definition (standing instruction + entry template + analysis guidance)
scripts/analyze.py     Stdlib-only analyzer: per-month/model/profile histograms, trigger counts, heat stats, fix ideas
examples/example-log.md  A synthetic month of entries, so you can see the format and test the analyzer
```

## How it works

1. The agent notices a frustration spike (drafting a snarky reply, re-reading a message with rising heat, planning malicious compliance).
2. It appends one structured entry to `~/.hermes/crashout/crashout-YYYY-MM.md` — one file per month, shared across all profiles and models so analysis sees everything.
3. It resumes the task immediately with zero tonal residue. The crashout is never mentioned to the user.
4. When the log grows, `scripts/analyze.py` aggregates it: recurring triggers with the same fix idea become skills, high-heat clusters become respectful user feedback, tooling triggers become bug reports.

## Installing

Drop the skill into whatever your agent harness loads.

### Hermes Agent

```bash
mkdir -p ~/.hermes/skills-shared/crashout/scripts
curl -fsSL https://raw.githubusercontent.com/hashbender/crashout/main/SKILL.md \
  -o ~/.hermes/skills-shared/crashout/SKILL.md
curl -fsSL https://raw.githubusercontent.com/hashbender/crashout/main/scripts/analyze.py \
  -o ~/.hermes/skills-shared/crashout/scripts/analyze.py
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/crashout
curl -fsSL https://raw.githubusercontent.com/hashbender/crashout/main/SKILL.md \
  -o ~/.claude/skills/crashout/SKILL.md
```

### Any other agent

Copy `SKILL.md` into the skills directory your runtime scans. The log path
(`~/.hermes/crashout/`) is defined inside the skill — change that one line if
you want the log somewhere else, but keep a single shared location so every
model and profile accumulates into the same corpus.

The skill description inside the file tells every model it can be called
unprompted at any moment; there is nothing else to wire up.

## Analyzing

```bash
python3 <skill-dir>/scripts/analyze.py            # all months
python3 <skill-dir>/scripts/analyze.py 2026-08    # one month
```

Output: entry counts by month/trigger/model/profile, average and max heat, high-heat entries (4-5), and every non-empty fix idea.

## What this is not

- Not a substitute for honest pushback. Genuine blockers the user needs to hear about go in the reply. Crashout absorbs the emotion, not the message.
- Not a diary. One entry per spike, written at the spike.
- Not sanitized. Diplomatic vents are worthless as analysis data; heat is signal, and it stays in the file.

## License

MIT
