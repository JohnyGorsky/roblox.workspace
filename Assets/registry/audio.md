# Audio — shared catalog

Our own uploads (creator `johnygorsky10`, owned). Pulled 2026-07-18 — **first 20 (more exist; expand via
keyword search)**. All Defender SFX/music. See [README](README.md).

| Name | rbxassetid (SoundId) | Project | Notes |
|------|----------------------|---------|-------|
| shark_attack_music | 140118514053949 | defender | music |
| pig-attack | 139588447817895 | defender | mob SFX |
| zombie_noticed_me | 138451405512346 | defender | mob SFX |
| level_completed | 138409734628557 | defender | UI/progression |
| skeletpon_hit | 138287768368871 | defender | mob SFX (sic) |
| shark7 | 133738469846673 | defender | mob SFX |
| monster_roar | 131065551334147 | defender | mob SFX |
| golem_roar | 130915528673907 | defender | mob SFX |
| skeleton_run | 130842853954416 | defender | mob SFX |
| dragon_hurt | 129952034291785 | defender | mob SFX |
| skeleton_roar | 129287092516321 | defender | mob SFX |
| pig-killed | 125997883726975 | defender | mob SFX |
| item_drop | 125050168809089 | defender | UI/loot |
| ######### (unnamed) | 124226923957822 | defender? | verify/rename |
| arrival | 121730547426887 | defender | SFX |
| golem_die | 120281850228156 | defender | mob SFX |
| player_attacked | 117259006391295 | defender | player SFX |
| dragon_attack | 115693608420368 | defender | mob SFX |
| apple-bite | 115016866323591 | defender | consumable SFX |
| armor_equip | 113580094004391 | defender | equip SFX |

## Jungle / Last River — our uploads (creator `johnygorsky10`, owned). Added 2026-07-20 (Job #064 lobby)

| Name | rbxassetid (SoundId) | Project | Notes |
|------|----------------------|---------|-------|
| lobby_intro_music | 135826546197884 | jungle | lobby theme (music loop) |
| morning_starts | **88638394432005** | jungle | music/stinger — day starts. ⚠️ **re-uploaded 2026-08-02**; the original `98066971477923` is dead |
| night_starts_2 | **75443344927115** | jungle | music/stinger — night starts, 11.0 s. ⚠️ **Third asset, DIFFERENT source audio** — the first two both failed moderation. See the note below |
| battle_starts | 79506043370965 | jungle | music/stinger — combat start |
| Jungle day ambience 1 | 116462724806689 | jungle | ambient bed — birds+insects (2D loop) |
| Jungle day ambience 2 | 120011248667884 | jungle | ambient bed variant |
| wind-breeze | 93331028777865 | jungle | ambient — light wind layer |
| water-splashes | 115704936377395 | jungle | positional SFX — dock/shore |
| crackle-campfire | 113774133604878 | jungle | positional SFX — campfire |
| cicadas | 128204240690640 | jungle | ambient one-shots — wildlife calls |
| rope_creak | 99642631685891 | jungle | positional creak @ watchtowers (LobbySoundscape) |
| timer_countdown | 116568191818931 | jungle | launch-pad countdown tick (LobbyServer, positional on pad) |
| ui_mouse_click | 89108158102227 | jungle | UI button click (UIClick.local.luau) |

> ✅ **`night_starts` took three assets to land — and the lesson is worth keeping.** The first two,
> `99602574849976` and then `95532390211599` (a re-upload of the *same*
> `assets/Objects/Ambient/night_starts.mp3`), both failed the same way: `GetProductInfo` succeeded — asset
> exists, AssetTypeId 3, owned by `johnygorsky10` — but `Sound.IsLoaded` stayed **false** and the runtime
> said *"Asset is not approved for the requester"*.
>
> **Diagnosis:** two uploads of one file failing identically, while its sibling `morning_starts`
> re-uploaded cleanly on the first try, meant the problem was **the audio itself** (Roblox's
> copyright/content check), not the pipeline, the account, or per-experience permissions. So the fix was
> *different source audio*, not a third upload of the same mp3 — `night_starts_2` `75443344927115` loads
> fine, 11.0 s.
>
> **Rule of thumb:** if an upload won't play, check whether a SIBLING upload from the same session works.
> If it does, stop re-uploading and change the file. Resolved: `roblox.jungle.game/todo/0044`.

### Lobby SFX batch 2 — uploaded 2026-07-20 22:40 (Job #064). Source files: `assets/Objects/Ambient/Sound_wave_2/*.mp3`

**Uploaded + owned, NOT yet wired into any script** — wiring is the next step (see ASSETS.md §1.12).
All 11 IDs verified in Studio 2026-07-30 (`GetProductInfo` → name match, AssetTypeId 3 = Audio).

| Name | rbxassetid (SoundId) | Project | Intended trigger |
|------|----------------------|---------|------------------|
| open_close | 89724136900326 | jungle | panel open / close (shop, skills, bounties, robux) |
| prompt | 83771530109851 | jungle | ProximityPrompt appear / hold-complete |
| joined_pad | 118942668007111 | jungle | player steps on / off a party pad |
| leader_assigned | 83295373162555 | jungle | first player on an empty pad becomes leader |
| teleport_woosh | 74173367633003 | jungle | party launch → teleport whoosh |
| purchase_success | 108328452137259 | jungle | purchase confirmed |
| failed_or_not_allowed | 95777104498740 | jungle | purchase fail / action not allowed / error |
| upgrade_applied | 98721741422623 | jungle | boat / skill upgrade bought & applied |
| rank_completed_or_mission_completed | 135669512865613 | jungle | rank-up / mission-complete stinger |
| footsteps_wood | 74260976253608 | jungle | footsteps on wood (dock, stall decks) |
| running_on_sand | 113877578461119 | jungle | running on sand (airfield clearing) |

### GAME place — plane-crash intro, uploaded 2026-08-02 (Job #072)

The cold-open sequence: the crew rides a plane in from the west, the engine fails, it dives and crashes
at the spawn base, and they wake in the wreckage. **Uploaded + owned; wiring is Job #072 step 3.**

**2D** = non-positional (heard in the cabin / in your head). **Positional** = attached to the plane or
the wreck, so it moves and falls off with distance.

| Name | rbxassetid (SoundId) | Project | Role in the sequence |
|------|----------------------|---------|----------------------|
| plane_flying | 131906456545456 | jungle | prop-engine drone — **2D loop**, the bed under the whole cruise |
| engine_fail | 109868059978369 | jungle | engine sputter/stall — 2D one-shot, cues the descent |
| stall_alarm | 112730854260419 | jungle | cockpit warning — 2D short loop, stall → impact (keep low under the engine) |
| wind_rush | 96421007219531 | jungle | dive rush — 2D loop, **fade IN across the 9 s descent**, don't play flat |
| crash_sound | 107234930559671 | jungle | 🔴 the impact — 2D one-shot; the cut to black lands on this |
| metal_debris | 139877854727588 | jungle | wreckage settling — **positional @ wreck**, ~1–2 s after impact |
| ear_ringing | 134266191078049 | jungle | tinnitus as you come round — 2D one-shot, fading |
| fire_sound | 99475771894138 | jungle | burning wreck — **positional @ wreck**, loop; full for ~45 s then fades to smoke |

### GAME place — boat engine, uploaded 2026-08-02 (Job #073)

The boat's **live** engine: a one-shot when someone takes the helm, then a loop whose volume and pitch
track how hard the boat is actually working. Both **positional on the boat's `Motor` part** (welded at the
stern) so the engine is heard from the right place and falls off with distance for the rest of the crew.

| Name | rbxassetid (SoundId) | Project | Role |
|------|----------------------|---------|------|
| boat_engine_starts | 105048345579705 | jungle | engine turning over — one-shot when a player sits in `DriverSeat` |
| speed_boat_loop | 74719520771875 | jungle | engine loop — volume + `PlaybackSpeed` driven per-frame by throttle and real hull speed |
| boat_hit | 131954812341128 | jungle | our boat takes damage — one-shot @ `Hull`, volume scaled by the size of the bite |
| croc_idle (aligator_hissing) | 137066735880685 | jungle | enemy SFX — Crocodile lurking hiss, positional @ Body, fires every 10–22 s while NOT chasing (Job #078) |
| gun_reload | 134765294816468 | jungle | uploaded 2026-08-16 — NOT yet wired |
| gun_empty_clip | 135106168511714 | jungle | uploaded 2026-08-16 — alternate for `empty_gun`, not wired |
| boat_destroyed | 89814954215320 | jungle | uploaded 2026-08-16 — NOT yet wired |
| boat_on_fire | 85716055048481 | jungle | uploaded 2026-08-16 — NOT yet wired |
| boat_engine_starts | 105048345579705 | jungle | uploaded — check against the wired engine loop before adding |
| speed_boat_loop | 74719520771875 | jungle | uploaded — ditto |
| boat_engine_loop_5_sek | 131217762182988 | jungle | uploaded — ditto |
| metal_debris | 139877854727588 | jungle | uploaded — candidate for the boat metal-hit cue |
| AxeSwing | 210946558 | jungle + defender | melee swing whoosh — reused from roblox.defender (Job #079) |
| AxeChop | 8936215056 | jungle + defender | melee HIT, only on a landed blow — reused from roblox.defender (Job #079) |
| Axe Equip | 2304904662 | jungle + defender | equip cue. ⚠️ authored at Volume 10.0 in Defender; Jungle wires it at 0.35 (Job #079) |
| shotgun fire high quality | 129597576449946 | jungle | Creator Store, free (Halflifeperson). Shotgun report — ⚠️ 3.21 s long against a 0.7 s fire interval, so it is RESTARTED not layered (Job #079) |
| shotgun-pump | 113837896417526 | jungle | Creator Store, free (RabbitFan6butreal). The rack between shots, fired 0.18 s after the shot (Job #079) |
| empty_gun | 75733077651437 | jungle | dry-fire click, already in the user's inventory — wired Job #079 |
| croc_attack (monster_bite_1) | 94063943857259 | jungle | enemy SFX — Crocodile bite, positional @ Body, one-shot on each bite (Job #078). Generic monster bite, not gator-specific |
| croc_aggro (aligator_aggro) | 108958436464973 | jungle | enemy SFX — Crocodile locks on; widest rolloff of the set so it carries over the engine (Job #078) |
| animal-hurt | 137192983266942 | jungle | enemy SFX — generic creature hurt. SHARED by Crocodile + Panther (Job #078) |
| animal-die | 120708334083507 | jungle | enemy SFX — generic creature death. SHARED by Crocodile + Panther (Job #078) |

### GAME place — weapons, uploaded 2026-08-02

| Name | rbxassetid (SoundId) | Project | Role |
|------|----------------------|---------|------|
| gun_shot | 138178318678571 | jungle | ✅ WIRED Job #079 (was uploaded 2026-08-02 and unwired) — weapon fire — <span style="color:#f0a020">**uploaded + owned, NOT wired, deliberately**</span> |

> **`gun_shot` is recorded here only.** The user's call while Job #073 was open: *"Do not add sound yet,
> because this will be seperate task, just list it in file."* It belongs with the weapon/turret work
> (`sync/ServerScriptService/Combat/GunServer.server.luau` + `WeaponServer`), not with the ambient job
> that happened to be running when it was uploaded.

> Wired by `sync/StarterPlayer/StarterPlayerScripts/Boat/BoatEngineSound.local.luau` — **client-side on
> purpose.** The volume/pitch change every frame, and driving that from the server would replicate a
> property write per frame to every client for no benefit. The boat is server-owned
> (`SetNetworkOwner(nil)`), so `AssemblyLinearVelocity` and `seat.Throttle` already replicate; each client
> reads those and drives its own local Sound.

> **Superseded local files:** `assets/Objects/Boat/Sounds/` still holds un-uploaded `boat_engine*.mp3`
> candidates. These two uploads are what the game uses; the rest of that folder is still unwired
> (`boat_on_fire`, `boat_destroyed`, `metal_hit_1_sec`).

> **Why a new fire sound when `crackle-campfire` exists:** the campfire loop (`113774133604878`, wired in
> the lobby) is a small domestic fire and reads far too thin for a burning aircraft. It is still useful
> **layered underneath** `fire_sound` for close-up crackle. Also unuploaded locally:
> `assets/Objects/Boat/Sounds/boat_on_fire.mp3`.
>
> **Not sourced (optional, low priority):** a distant plane pass to foreshadow the aircraft before it
> clears the ridge.

---

### In-run HUD cues — **Job #075 (2026-08-02), game place**

**Reused, not re-sourced.** Three of these are filed above under `defender`. They are generic SFX with
nothing Defender-specific in them, and reuse-before-re-source is this registry's stated purpose — so the
Jungle HUD points `Theme.sound` straight at the existing ids rather than uploading duplicates.
⚠️ *Pending the user's OK; swap for Jungle-specific uploads if they'd rather.*

| Theme key | Registry asset | rbxassetid | Originally | Now also used by |
|---|---|---|---|---|
| `pickup` | `item_drop` | 125050168809089 | defender | jungle — loot picked up |
| `hurt` | `player_attacked` | 117259006391295 | defender | jungle — player takes damage |
| `runWin` | `level_completed` | 138409734628557 | defender | jungle — run won (results panel) |
| `zoneEnter` | `battle_starts` | 79506043370965 | jungle | zone-crossing banner |
| `dayBreak` | `morning_starts` | 88638394432005 | jungle | DAWN banner |
| `nightFall` | `night_starts_2` | 75443344927115 | jungle | NIGHTFALL banner |
| `emptyClick` | **`empty_gun`** | **75733077651437** | **jungle** | dry trigger click — turret + handheld, no ammo |

**⏳ NOT YET SOURCED — 5 placeholders.** Declared in `Theme.sound` with an EMPTY id, listed in
`Theme.soundPending`, and already wired at every call site. `UISound` skips an empty id silently (an
*unknown* key still warns), so each one starts working the moment its id is pasted in. Sourcing brief +
search terms: `roblox.jungle.game/ASSETS.md` §5.3.

| Theme key | Fires when | Wanted |
|---|---|---|
| `lowFuel` | fuel crosses below 20% | ~0.5 s single soft beep, not a loop |
| `lowHull` | hull below 30%; boat attacked while you're ashore | ~1 s metallic groan |
| `downed` | you go down | ~1 s low thud + breath |
| `revived` | you get back up | ~1 s rising swell |
| `runLost` | crew wiped | ~2 s somber descending sting |

> **Remember to update BOTH copies of `Theme.luau`** when an id lands — `sync/ReplicatedStorage/UI/` and
> `lobby/sync/ReplicatedStorage/UI/` are byte-identical by contract.

> **`empty_gun` `75733077651437` — uploaded 2026-08-05, VERIFIED PLAYABLE.** Not just `GetProductInfo`:
> name match + `AssetTypeId = 3` + creator `johnygorsky10`, **and** `PreloadAsync` succeeded with
> `IsLoaded = true` and `TimeLength = 0.392 s`. That last part is the check that matters — per the
> `night_starts` note above, an asset can pass `GetProductInfo` three times over and still refuse to load.
>
> Wired to `Theme.sound.emptyClick`, volume 0.45, with a 0.3 s per-cue debounce override in `UISound`
> (the global default is 0.06 s, which would let a 0.39 s sound stack on itself when a player mashes the
> trigger). Consumed by `GunClient` (mounted turret) and `WeaponClient` (handheld).
