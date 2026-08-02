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
| morning_starts | 98066971477923 | jungle | music/stinger — plays when day starts |
| night_starts | 99602574849976 | jungle | music/stinger — plays when night starts |
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

> **Why a new fire sound when `crackle-campfire` exists:** the campfire loop (`113774133604878`, wired in
> the lobby) is a small domestic fire and reads far too thin for a burning aircraft. It is still useful
> **layered underneath** `fire_sound` for close-up crackle. Also unuploaded locally:
> `assets/Objects/Boat/Sounds/boat_on_fire.mp3`.
>
> **Not sourced (optional, low priority):** a distant plane pass to foreshadow the aircraft before it
> clears the ridge.
