# FINDING 0003 — Never create or delete directories inside a Studio Sync root

**Project:** workspace (applies to every game using Studio Sync)
**Severity:** high
**Status:** open
**Opened:** 2026-08-29 — caused by Claude during magnet-sweep job 002

## What happened

A sync-layout probe on `roblox.magnet-sweep` wrote marker files into every candidate location inside the
sync root, then cleaned up with:

```
find . -name "SYNCPROBE_*" -type f -delete
find . -mindepth 1 -type d -empty -delete      # <-- this line
```

Two distinct mistakes, both mine:

1. **It created folders for services that cannot sync** — `StarterGui/`, `StarterPack/`, `Workspace/`,
   `Lighting/`, `SoundService/`, `StarterPlayer/`. These map to nothing.
2. **The cleanup deleted the mapped service folders themselves**, because they were empty once the
   probe files were gone.

**The user's sync connection dropped twice** and they had to reconnect it both times. They noticed
before I did, and told me I was doing something wrong. They were right.

## The second, worse consequence: a false finding

Because the watched directories vanished *in the same operation* as the file deletions, the per-file
deletions were never reported to Studio. The instances lingered.

That was written up as an engine/tooling fact:

> "Deleting a file does not delete the instance. Sync propagates deletion only Studio → disk.
> Consequence: renaming a file leaves a ghost behind that still runs."

**This is false.** Re-tested properly — create the file, confirm it arrives, delete **only** the file,
leave the directory alone — the instance **is** removed. Deletion propagates in both directions.

**A broken watcher is indistinguishable from a one-way sync.** That is the trap, and it is the reason
this finding matters more than "be careful with rm": a tooling mistake got recorded as a property of the
tool, in a file other games are meant to learn from.

## Rules

1. **The directory structure of a sync root is fixed.** Create the mapped service folders once; never
   delete one, and never create a folder that does not map to a synced service.
2. **Pin every mapped folder with a `.gitkeep`** so it can never be empty, and so no `find -type d
   -empty -delete` or equivalent can sweep it. (`.gitkeep` produces no instance — verified.)
3. **Never run a recursive directory delete inside a sync root.** Delete files by name.
4. **When cleaning up a probe, delete files only.** If instances linger, that is a signal the connection
   is damaged — not a fact about the tool.
5. **Before recording any sync behaviour as a finding, re-test it with the folders intact.**

## Check

```
find <syncroot> -mindepth 1 -type d
```

must return exactly the mapped service folders, no more and no fewer. For magnet-sweep that is six:
`ReplicatedFirst ReplicatedStorage ServerScriptService ServerStorage StarterCharacterScripts
StarterPlayerScripts`.

## Applies to

Every game here that uses Studio Sync — Jungle (`sync/`, `lobby/sync/`), Tide and ELEVATOR 13
(`studio_game/`, `studio_lobby/`), magnet-sweep (`studio_game/`). None of the others have a `.gitkeep`
pin on their service folders; adding one is cheap insurance.

## Where it is written down

`roblox.magnet-sweep/docs/PITFALLS.md` **#11b**, and
`roblox.magnet-sweep/docs/systems/places/README.md`. Worth promoting into `GROUND-RULES.md` §2 or the
`roblox-studio` skill, since it is not game-specific.
