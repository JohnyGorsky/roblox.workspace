# Final Summary — Job #009: todo/ and findings/ capture queues

**Project**: `roblox.workspace`
**Completed**: 2026-07-18
**Status**: ✅ Completed & tested

## What was done

Added two lightweight per-project capture queues (alongside `Jobs/` and `Planned/`):
- **`todo/`** — quick tasks/thoughts/reminders, numbered `NNNN` (0000+), greppable `Status: open → resolved`.
- **`findings/`** — bugs noticed but deferred, numbered `NNNN`, `Status: open → fixed` (symptom/where/repro/fix-idea).

Both capture in one command so they never break flow; promote real work to a Job.

## Tooling (extended `roblox.workspace/tools/job.py`)

- `job.py todo --project <p> "Title" ["note"]` → `todo/NNNN-slug.md`.
- `job.py finding --project <p> "Title" ["symptom"] [--severity low|med|high] [--where ...]` → `findings/NNNN-slug.md`.
- `job.py resolve --project <p> <todo|finding> NNNN ["note"]` → flips the `Status:` line (resolved/fixed + date).
- `job.py list --project <p> <todo|finding> [--open]` → `[ ]`=open / `[x]`=done with status.
- 4-digit numbering per project; regex `Status:` flip (no file moves).

## Scaffolded

- `todo/README.md` + `findings/README.md` in **workspace, defender, jungle** (usage docs).
- `GROUND-RULES.md §5` — recorded the convention.

## Verification (tested)

- [x] `todo`/`finding` create with per-project 0000+ numbering.
- [x] `list` shows `[ ]`/`[x]` + status; `--open` filters.
- [x] `resolve` flips the Status line to `fixed/resolved (date) — note` (verified on a throwaway, then removed).
- Seeded genuine todos: workspace `0000` (set up Meshy MCP), jungle `0000` (resolve GAME.md open questions).

## Notes
- Not committed (per rule). `settings.json` already allows `python tools/job.py:*` — no permission change needed.
