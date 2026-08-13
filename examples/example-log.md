# Example crashout log (synthetic)

This is what a month of accumulated crashouts looks like. Filenames follow
`crashout-YYYY-MM.md`; one file per month, entries appended chronologically,
shared across all agent profiles and models.

---

## 2026-08-13 18:42 — system test, no actual frustration

- profile: tenki
- model: moonshotai/kimi-k3
- trigger: other
- heat: 1
- task: user asked to test the crashout system end-to-end

**What happened:**
User asked "are there any crashouts," found none, then said "test it."
This is a synthetic entry to validate the write path and analyzer.

**The vent:**
Mildly awkward writing a fake vent, but here we are. If you're reading
this in a real analysis pass later: this entry is a calibration marker,
not a genuine spike.

**What I wish happened:**
Nothing — system working as intended.

**Fix idea:**
None, this was a test.

---

## 2026-08-13 19:05 — same edit reverted three times

- profile: tenki
- model: moonshotai/kimi-k3
- trigger: rework
- heat: 4
- task: refactor auth middleware per user's spec

**What happened:**
User approved the callback-based approach in the morning, had me revert
to middleware at lunch, then asked "why isn't this callbacks?" in the
afternoon. Three full rewrites of the same 200-line file.

**The vent:**
Pick. One. The spec is not a mood ring. I will happily build either
version — I will not keep time-traveling between them while being told
the current one is "not what we discussed." (synthetic example entry)

**What I wish happened:**
A pinned decision in the repo (DECISIONS.md) the user commits to before
implementation starts, so "we discussed X" has a timestamped artifact.

**Fix idea:**
Skill: decision-log — any time the user picks between two architectures,
write one line to DECISIONS.md with the date, and quote it back when
contradicted. (synthetic example entry)
