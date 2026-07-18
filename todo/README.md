# todo/ — quick-capture task queue

Lightweight queue for **thoughts, small tasks, tweaks, reminders** — lighter than `Planned/` (future
*features* that become Jobs) and `Jobs/` (full tracked work). One markdown file per item, numbered `NNNN`
(0000+), with a greppable `Status:` line.

## Use (shared `job.py`)
- **Capture fast** (don't break flow):
  `python tools/job.py todo --project <workspace|defender|jungle> "Short title" ["optional note"]`
  → `todo/NNNN-short-title.md` with `**Status:** open`.
- **Mark done:** `python tools/job.py resolve --project <game> todo NNNN ["what/where"]` → flips the Status line.
- **See the queue:** `python tools/job.py list --project <game> todo [--open]`  (`[ ]`=open, `[x]`=done),
  or `grep -rl "Status:\*\* open" todo/`.
- **Promote** a todo that turns into real work into a **Job** (or a `Planned/` feature).

_todo vs findings:_ todo = things to do; findings = bugs noticed but deferred.
