# findings/ — deferred-bug log

Bugs/issues noticed mid-flight but **too busy to fix now**, so they're never lost. One markdown file per
finding, numbered `NNNN` (0000+), `Status: open` → `fixed`. Feeds bug-fix / code-review passes.

## Use (shared `job.py`)
- **Log it fast:** `python tools/job.py finding --project <game> "Short title" ["symptom"] [--severity low|med|high] [--where <file/system>]`
  → `findings/NNNN-title.md` (symptom / where / repro / fix-idea).
- **Mark fixed:** `python tools/job.py resolve --project <game> finding NNNN ["fixed in Job NNN / commit"]`.
- **List:** `python tools/job.py list --project <game> finding [--open]`; or `grep -rl "Status:\*\* open" findings/`.
- A finding worth a real fix → promote to a **Job**.
