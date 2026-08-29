# FINDING 0002 — `roblox-animation` skill states two engine facts backwards

**Project:** workspace
**Severity:** high (was logged med; raised after verification)
**Status:** open
**Opened:** 2026-08-29 — surfaced by the independent review on magnet-sweep job 001

## Why this matters more than a normal finding

GROUND-RULES §6 makes consulting these skills **mandatory** before writing Luau. Both facts below are
stated confidently and are wrong, so the rule currently propagates them into every game. MAGNET SWEEP is
the first to have built an architecture on top of them; the errors were caught in review, but only
because the reviewer checked the engine rather than trusting the skill.

Neither error produces a script error. Both fail silently.

## Error 1 — the animation priority ladder is inverted

`.claude/skills/roblox-animation/SKILL.md:21`

```
- **Priority** decides who wins on shared joints: `Idle<Movement<Action<Action2/3/4<Core(1000)`.
```

**`Core` is the LOWEST priority, not the highest.** Verified against
`raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/enums/AnimationPriority.yaml`,
which orders them explicitly and describes Core as *"Lowest priority, intended for use by Roblox default
animations and catalog animation bundles."*

The trap is exactly what the current line highlights: `Core`'s numeric **value** is 1000 while
`Action4` is 5. **The enum does not order by value.** Citing `(1000)` actively reinforces the wrong
reading.

Correct order, highest first:

```
Action4 > Action3 > Action2 > Action > Movement > Idle > Core
```

**Consequence if unfixed:** an NPC or robot attack clip set to `Core` — the natural choice if you
believe this line — loses to `Idle` and never renders. It looks like a rig or blending bug.

## Error 2 — "play NPC animations client-side" is wrong for server-owned NPCs

`.claude/skills/roblox-animation/SKILL.md:24` — *"Play NPC anims **client-side** (they replicate via the
Animator …)"*
`.claude/skills/roblox-animation/reference/animation.md:80` — *"Play NPC animations **client-side**
(replicates cheaply via the Animator)."*

`Animator` replication is **conditional**, and the condition is the opposite of what this says. From
`classes/Animator.yaml`, verbatim:

> "If an `Animator` is a descendant of a `Humanoid` or `AnimationController` in a **player's Character**,
> animations started on that player's client will be replicated to the server and other clients."
>
> "If the `Animator` is **not** a descendant of a player character, its animations **must be loaded and
> started on the server to replicate**."

So the advice is right for a **player's own character** and wrong for every **server-spawned NPC** — the
case the line is explicitly about. A `LocalScript` animating a server-owned NPC animates it for that one
client and nobody else.

**Consequence if unfixed:** every other player sees the NPC slide around in its rest pose. Diagnosing
that from the animating client is nearly impossible, because on that machine it looks correct.

The legitimate adjacent pattern is *server broadcasts an event, every client plays locally* — which
needs an explicit remote and is not what "play client-side" reads as.

## Suggested wording

```
- **Priority** decides who wins on shared joints, highest first:
  `Action4 > Action3 > Action2 > Action > Movement > Idle > Core`.
  ⚠️ `Core` is the LOWEST despite its value being 1000 — the enum does not order by value.
  Action anims must outrank Movement/Idle to be seen.
- **Cache/reuse tracks**; don't reload the same Animation (`LoadAnimation` always makes a NEW track —
  use `GetTrackByAnimationId` to look one up).
- **Where to play:** a player's OWN character → client (it replicates). A server-spawned NPC → **server**
  (an Animator not under a player character must be started server-side to replicate at all). To drive
  NPC animation from clients, broadcast an event from the server and have every client play locally.
```

## Also check, same sweep

Surfaced by the same review, not yet independently confirmed here:

- `roblox-animation/reference/animation.md:88` repeats the client-side advice.
- `roblox-optimization` and `roblox-ai` carry the same phrasing — defensible only if read as "server
  broadcasts, all clients play".
- `roblox-physics/SKILL.md:90-91` says `AlignPosition.MaxForce` is a scalar with no per-axis mask;
  `MaxAxesForce` + `ForceLimitMode = PerAxis` is exactly that mask.
- `roblox-vfx/SKILL.md:16` says `Lighting.Technology` "NO LONGER EXISTS". It exists, is
  `RobloxScriptSecurity` on read *and* write, and is superseded by `LightingStyle` +
  `PrioritizeLightingQuality`.
- `roblox-animation:61`'s `[unverified]` flag on the `AnimationConstraint` supersession can be promoted —
  it is confirmed on both the Motor6D and AnimationConstraint pages.

## The sourcing rule that would have prevented this

Three of the errors found in that review trace to `create.roblox.com` rendering deprecation status onto
the wrong member. **For deprecation, security level and enum ordering, use the raw YAML**, which carries
the real `tags:` / `security:` / `deprecation_message:` blocks:

```
https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/<classes|enums>/<Name>.yaml
```

Worth adding to `roblox-dev` as a standing rule.

## Where this is already written down

`roblox.magnet-sweep/docs/PITFALLS.md` entries **45-47**, and the corrected facts are in
`roblox.magnet-sweep/docs/systems/robot-rig/README.md` §1.
