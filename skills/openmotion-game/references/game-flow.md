> See [source and execution notes](../PROVENANCE.md).

## OpenMotion execution contract

This reference governs authored game assets, not Studio application styling. Use `openmotion_game_create`, `openmotion_game_get`, `openmotion_game_read_file`, `openmotion_game_write_files`, `openmotion_game_update_meta`, `openmotion_game_capture_cover`, `openmotion_game_playtest`, `openmotion_game_simulate`, `openmotion_game_validate`, `openmotion_game_set_status` and authorized **local** `openmotion_game_publish`. Paths below are game-relative. Use the six-export contract in `shared/game-contract.ts`; the offline starter is `templates/game-kits/coop-3d/` with `vendor/` and `characters/` copied alongside it.

**Tool compatibility:** `openmotion_generate_asset` is a legacy optional route, not exposed by phase-one hosts. Use it only when tools/list actually exposes it. Otherwise use discovered `openmotion_media_use` for inspect/reference/models and `openmotion_assets_use` for authorized generation/job tracking; if unavailable, use existing local assets and report the gap. Do not invent Tool names or forward old CLI flags.

For media, discover the installed model/provider contract first using `openmotion_media_use action=models`; inspect required inputs and current pricing. Use `openmotion_generate_asset` only for an actually available model, with the stated price/cost estimate, quantity and user approval before submission. Track its job and save the resulting asset into the game. Historical model names and costs below are selection criteria and upstream budgets, **not promises of installed models, free quota or current prices**. Unsupported image-to-3D, rigging, animation presets and retexture operations have no generic OpenMotion equivalent: use the bundled CC0 GLBs, supplied assets, or an explicitly provisioned local Blender workflow. Never pretend that image/video generation produces a rigged GLB.

Legacy Python/Blender helper names below specify algorithms and optional workflows; those helpers are **not bundled** here. Check for a user-provided installed helper before using its command; otherwise implement the described operation as scoped work or report the missing capability. Do not install software, fetch scripts or contact a raw provider without authorization. The shipped inspector is `node scripts/game-glb-inspect.mjs <file.glb>` (meshes, skins, unique bones, clip names/durations, triangles); it does not check root-scale channels or patch/merge rigs. No inherited claim of a bundled helper overrides this boundary.

# Game flow — local projects and authoritative rooms

A game is a local HTML project. HTTP and MCP use the same game service and file tree. Creation scaffolds editable source; validation checks it; authorized local publication lists it in this workspace. There is no website-builder deployment, subdomain provisioning, hosted community publication or internet hosting equivalent.

## Create

```json
{"tool":"openmotion_game_create","arguments":{"prompt":"Defend a crystal together","genre":"shooter","style":"3d","multiplayer":true}}
```

- Use the supported genres `shooter`, `platformer`, `story`, `casual`, `racing`, `horror` from `shared/game-contract.ts`. Genre is optional, defaults to casual. The original categories arcade, puzzle, RPG, strategy, simulation, adventure, action, fighting, survival, sports, card-board, education, endless-runner, MOBA, music-rhythm and sandbox-building are brief descriptions, not accepted enum values: choose the closest supported genre and preserve the specific idea in `prompt`.
- Do not pass a template or subdomain argument: neither exists. With `multiplayer:true` and either `genre:"shooter"` or `style:"3d"`, creation copies `templates/game-kits/coop-3d/` plus vendored modules and characters. Other briefs retain the lightweight starter. Use the returned project id and playUrl, never invent a hosted URL.

## Read the shipped contract

Read `AGENTS.md`, `shared/game-contract.ts`, this reference and the scaffold's actual inventory before writing. Project files live under workspace `games/<id>/`.

| File | Responsibility | Edit? |
|---|---|---|
| `logic.js` | Six deterministic named exports | Yes |
| `index.html`, `client.js`, `style.css` | Presentation and inputs | Yes |
| `vendor/`, `characters/`, `assets/` | Relative local assets and licenses | Preserve notices |
| repository `game-projects.ts` | HTTP routes, room sockets, simulation and fan-out | Product engineering only |
| `game.json` | Service-owned metadata | Never through source writes |

Required exports: `meta`, `setup`, `validateAction`, `applyAction`, `isGameOver`, `viewFor`. Optional test exports are `referenceRoute(playerIndex)` and `summarize(state)`; they run inside the same bounded deterministic VM, not a second rules engine. `openmotion_game_validate` replaces the upstream Bun/build checker: no imports/require, `Date.now()` or `Math.random()` in logic; synchronous JSON-compatible state/views; use `ctx.random()`, `ctx.now` and `ctx.tick`. The validator dry-runs 50 ticks with two players and is not a gameplay-quality test.

- **validateAction is the defence:** clients are untrusted; turn, range, target and payload bounds belong there. Do not accept a client-computed position, hit or damage.
- **viewFor controls information:** send only the player's allowed information. A card game returns that player's hand and other players' card counts, never every hand.

## Tick and membership convention (six exports retained)

The co-op kit sets `meta.serverTick:true`. The runtime then invokes `applyAction(state, null, {type:"tick"}, ctx)` once per server tick, before queued user inputs. It invokes `applyAction(state, null, {type:"membership",player,connected}, ctx)` when a running room admits/reclaims/disconnects a player. These are server events: `validateAction` must reject them from real player ids, and `applyAction` must independently guard them. Existing logic without the opt-in keeps its original semantics.

The kit advances at 20 Hz; clients send movement at 10 Hz, with an 8-tick expiry, normalized diagonals, ±13 arena and 5 units/s movement. All balance values live in the single `config` block at the top of `coop-3d/logic.js`. Enemy counts are `4 + wave*2`, health `2 + floor(wave/3)`, speed `1.1 + wave*0.12` units/s. Hunters chase the nearest living player within 9 units; siege enemies pressure the objective. Contact attacks every 18 ticks deal 12 player HP or 5 objective HP. Player/objective HP starts at 100. Nearby living teammates within 2.5 units revive a downed ally after 40 consecutive ticks to 60 HP; a solo downed player respawns after 100 ticks (5 seconds). Disconnected players neither fight nor revive. Join order assigns deterministic spawn slots.

Dash (`Space` or touch button) moves 4.5 units, grants 8 ticks of invulnerability and has an 80-tick cooldown. Nova (`E` or touch button) deals 3 damage within radius 4, with a 160-tick cooldown. Both use validated `{type:"skill",skill:"dash"|"nova"}` inputs; clients cannot bypass cooldowns or act while downed. Basic fire repeats every 6 ticks and requires fresh movement or explicit fire intent; continuously sending zero-motion/no-fire inputs must not defeat idle-loss acceptance. The first wave waits 40 ticks; cleared waves give a 12 HP heal and 3 objective repair, then an 80-tick breather/countdown. Five cleared waves win; zero objective HP loses. Restart still requires every connected player's vote. Transient event ids drive real Hit_A/Death_A transitions, flashes, particles, wave banners, objective shake and sound; presentation never supplies damage. The always-visible HUD includes invite, own HP and skill cooldowns. No Skeletons assets are bundled: enemies are original procedural low-poly meshes, not downloaded models.

## Design and verification artifacts

Write these game-relative files using `openmotion_game_write_files`. The co-op kit ships editable drafts; revise them for the actual brief and current source. Validation reminds once per missing file without blocking. Existence is not proof of content acceptance.

| File | Required content |
|---|---|
| `design/plan.md` | One-sentence experience formula; scope/input methods; metrics with numeric thresholds; **reference route must win, idle must lose**; wave/difficulty and comeback plan; remaining human/device acceptance |
| `design/assets.csv` | At least `asset,source,license,cost`; include actual local/bundled/generated status, asset purpose, confirmed license and approved spend or unknown cost |
| `design/verification.md` | Tested game revision/date; tool inputs/commands; threshold vs measured result; reference and idle outcomes/ticks; browser assertions/resources/screenshots; known gaps and unavailable checks |

Keep observed evidence separate from targets. A pending template verification row is not a passed test, and software-rendered FPS is not physical GPU performance. Optional `## Follow-up opportunities` bullets in the plan seed the three short `nextSteps` prompts returned by publish. Without that section, defaults use the plan title (or a generic game reference). Present these as user-sendable suggestions, not authorization to perform follow-up work.

## Deterministic rule simulation

Before publication, run both routes below, then inspect the terminal outcome and timeline rather than merely checking that the tool returned.

```json
{"tool":"openmotion_game_simulate","arguments":{"id":"<game-id>","players":2,"scripts":"reference","maxTicks":2500}}
```

```json
{"tool":"openmotion_game_simulate","arguments":{"id":"<game-id>","players":2,"scripts":"idle","maxTicks":2000}}
```

`players` is 1–4 within logic meta limits. `maxTicks` is 1–10000. `scripts` is `idle`, `reference`, or one route per player; each route may also select those built-ins. Idle sends no actions. Reference requires a game-provided exported `referenceRoute(playerIndex)` returning up to 1000 entries `{fromTick,toTick,action}`. Indices start at zero. Ticks start at one, are inclusive and bounded to 10000; active entries repeat their action each tick in list order. Match the room limit of at most 16 actions per player per tick; a run is bounded to 100,000 scripted input applications. Explicit routes use the same shape, for example `scripts:[[{"fromTick":1,"toTick":20,"action":{"type":"move","dx":1,"dz":0,"ax":0,"az":1,"fire":false,"aimed":false}}],"idle"]` for two players. Native game rules validate every action; no route gets server-only tick/membership privileges.

Simulation uses fixed player ids and a fixed seed, advances the same server tick first and then applies that tick's scripted inputs. It returns `result:{over,winners,tick}` and at most 100 ordered timeline snapshots `{tick,state}` including initial and final state. Optional exported `summarize(state)` supplies compact JSON key state; otherwise the first player's `viewFor` is used (32 KiB summary limit). `over:false` means the budget expired, not a passed idle-loss contrast. A valid idle loss must be terminal with no winners and the game's intended loss summary; reference must be terminal with the expected winners and preserved objective. Record both in verification.md. The shipped reference route uses ordinary movement, explicit auto-aim fire and timed nova inputs; it is an idealized regression route, not evidence of human difficulty or rendering.

## Room protocol and recovery

Connect to `ws(s)://<same-host>/api/games/<id>/rooms/<room>` derived from the current play URL. Preserve either `/api/games/` or `/motion-api/games/` from `location.pathname`, using `location.href` to construct ws/wss URLs (an iframe may have an opaque origin). The server accepts loopback Host values, absent Origin, sandbox Origin `null`, and HTTP(S) loopback origins including a different Studio dev port. Foreign origins remain rejected. Game static responses allow `Access-Control-Allow-Origin: *` for read-only module/model loading in sandboxed previews; metadata/API responses do not gain this permission.

```json
{"type":"join","name":"Player","reconnectToken":"optional token from this tab"}
```

`joined` returns `playerId`, `room`, `players`, `maxPlayers` and an additional opaque **reconnectToken**. Store the token in `sessionStorage`, keyed by game path and room; do not put it into invite URLs. Send `{type:"start"}` when the room reaches minPlayers, then `{type:"input",action:...}`. Receive `state` (view and tick), `over` (winners), or `error` (message).

A disconnected player's identity/seat is reserved for **30 seconds**. A valid token reclaims the same id and its existing simulation state; an already connected token is rejected. Invalid/expired tokens produce an error: clear the stored token and join without it to receive a new identity. A running room permits late joins up to maxPlayers, counting reserved seats. Late membership does not reset the round. Token possession is the only recovery credential, not an account or authenticated identity; do not share it. Pending connections have a 10-second join deadline.

Rooms, tokens, votes and simulation state exist only in one local process. The room is discarded 30 seconds after the last joined client disconnects, even if idle connections remain. Simulation continues during this grace period, so the objective may take damage while everyone is disconnected. Process restart loses every room; there is no disk persistence, distributed room routing, public hosting, remote-device guarantee or account recovery. A copied localhost invite works in other tabs/browsers on this machine, not another person's machine.

## Validate, preview, publish locally

```text
openmotion_game_validate {id}
openmotion_game_set_status {id,status:"ready"}
openmotion_game_publish {id}  # only with local publication authorization
```

Use returned playUrl and roomInviteUrlPattern. Before publication, call `openmotion_game_update_meta` to set a concise title, description, controls, `zh-CN` translations of all three fields, and a project-relative cover image. Use `openmotion_game_capture_cover` for the required gameplay cover; it writes `assets/cover.png` and updates cover automatically. Never capture or operate the user's desktop, visible Chrome, tabs or profile. Imported images must be at least 960×540 and 16:9 ±5%; the tool checks that the relative image exists, rejects traversal/symlinks and merges i18n locale fields. Publication returns non-blocking `warnings` if the title is still the original prompt (including the initial 80-character truncation) or no cover is set. Changing description does not erase the original-prompt warning. Read and report these warnings; metadata edits preserve lifecycle status. There is no requirement for upstream `app-meta.json`, OG URLs or a hosted community feed. Game source can be edited through `openmotion_game_write_files`; binary copying requires authorized local file access. Keep all HTML/module/model paths relative so remix copies remain independent. Source edits demote a ready/published game to building; revalidate before republishing.

### Metadata example

After `openmotion_game_capture_cover` has saved the game-only cover, call:

```json
{
  "tool": "openmotion_game_update_meta",
  "arguments": {
    "id": "<game-id>",
    "title": "Crystal Guard",
    "description": "Defend the crystal through five co-op waves.",
    "controls": "WASD/arrows or touch joystick; mouse aim/fire; touch auto-fire.",
    "cover": "assets/cover.png",
    "i18n": {
      "zh-CN": {
        "title": "晶石守卫",
        "description": "合作抵御五波敌人，守住中央晶石。",
        "controls": "WASD/方向键或触控摇杆移动；鼠标瞄准射击；触控自动射击。"
      }
    }
  }
}
```

Only owned project metadata is writable. The equivalent local HTTP operation is `POST /api/games/<id>/update-meta` (also `/motion-api/games/`), with the metadata patch as its body. Ordinary local API write-origin checks still apply; the sandbox CORS allowance is for static reads only.

## Server-owned cover capture and playtest

**Never operate or attach to the user's visible browser, desktop, tabs or existing profile, including for troubleshooting or screenshots. These two MCP tools are the required paths for gameplay covers and multi-client tests.** They use a fresh temporary Chrome profile on the server, headless mode, SwiftShader, 1280×720 viewport, isolated browser contexts and an ephemeral loopback server. No downloads or external game requests are allowed. Missing local Chrome/loopback permission is a blocker to report, not authorization to use the user's browser.

```json
{"tool":"openmotion_game_capture_cover","arguments":{"id":"<game-id>","delayMs":1500,"actions":[{"type":"key","key":"w","event":"down"},{"type":"wait","ms":300},{"type":"key","key":"w","event":"up"}]}}
```

Capture optionally accepts `room`. It crops only the canvas (or #game root), never browser chrome or a full desktop. It saves a 1280×720 PNG at `assets/cover.png` and sets game metadata. Check the returned diagnostics and image: a loading error/blank canvas is not an accepted cover. `update_meta` rejects images below 960×540 or outside 16:9 ±5%. Supported dimension inspection: PNG, JPEG, WebP, GIF and SVG; unsupported formats must be converted with available local tooling or replaced by the capture PNG.

```json
{"tool":"openmotion_game_playtest","arguments":{"id":"<game-id>","clients":2,"durationMs":3000,"scripts":[[{"type":"key","key":"w","event":"down"},{"type":"wait","ms":300},{"type":"key","key":"w","event":"up"},{"type":"key","key":"Space"}],[{"type":"key","key":"a","event":"down"},{"type":"wait","ms":300},{"type":"key","key":"a","event":"up"},{"type":"mouse","event":"click","selector":"#nova"}]]}}
```

Each run has its own temporary room server and simulation; the optional room name does not attach to a live user room or preserve a previous run. Clients share a generated room (or optional supplied room), auto-join when the game supports a room URL and click conventional enabled #start after all pages load. The script API supports only key `down/up/press`, mouse `move/down/up/click` (1280×720 coordinates or a simple #id click target), and bounded waits. There is no arbitrary JavaScript or desktop operation. Multiplayer joining must never require explicit click actions; custom click actions may start play only after the no-input autoJoin check. Each client has at most 100 actions, each wait ≤10s and total waits ≤60s. `durationMs` (0–60s) is a minimum observation interval; scripts run concurrently and may extend it. Cover delay is 0–10s. Scripts never synthesize server hits, HP or room identity.

The client convention is `window.__omGame = {getState,getStats,sendAction}`. `getState()` returns a cloned latest server view plus `selfId`; `players` maps ids to authoritative x/z/connected fields, and `phase`/`result` identifies lifecycle. `getStats()` exposes render FPS, drawCalls, entities and tick; `sendAction(action)` sends a normal validated room input and never edits state. `?debug` shows those metrics without changing gameplay. Custom games should adopt this convention.

Playtest reads before/after snapshots and returns four gameplay assertions plus a multiplayer autoJoin assertion per client: playerCount, phase, scriptedMovement and mobileHorizontalOverflow. Defaults require the requested connected player count, an active/terminal game phase, net movement >0.5 world units from a directional key script, and no horizontal overflow at a measured 390×844 viewport. Options `movementThreshold` (0–100) and `expectedPhase` select planned thresholds. Missing hooks/selfId/coordinates or an absent directional script fail the relevant assertions, not silently pass. Omitted scripts automatically use W down / 350ms wait / W up for every client; explicitly provided empty scripts remain empty. Do not send a return-to-origin route when asserting net displacement. The runner restores capture sizing before the mobile layout measurement.

Returns per-client authoritative state/stats, assertion results, console/page/script errors, failed/HTTP-error requests, canvas/root screenshot paths under `assets/playtests/`, and metrics: roomJoined, playerCount, frames and fpsEstimate. FPS estimates requestAnimationFrame pacing, not GPU rendering speed. The harness keeps client documents logically visible for concurrent rendering; background suspension requires separate verification. Review all clients: joined=true, expected player counts, meaningful movement/skills, and no unexplained resource/console errors. Screenshots are local files; publication remains separate. Capture/update-meta/playtest use the same game service; their local HTTP forms are POST `/api/games/<id>/capture-cover`, `/update-meta`, `/playtest`, `/simulate` (also under `/motion-api/games/`). Ordinary local API write-origin checks remain in force.

Run `node --experimental-strip-types --test tests/game-projects.test.ts` for deterministic rules and protocol tests. Test damage, down/revive, solo respawn, dash/nova cooldowns, late join/reconnect and restart as separate rule cases. Validator warnings identify a missing cover or fewer than 20 approximate changed starter logic lines (whitespace and line reordering ignored); they do not fail validation, prove originality or justify filler edits. Touch joystick/tap, release/cancel, focus loss and narrow-layout acceptance remain required; the key/mouse headless script does not establish physical touch-device or audio acceptance. Report unavailable Chrome, actual GPU/phone performance, audible playback and human fun separately.

## Art and audio

Read `game-design-system.md` first (profile, core loop and manifest), then `game-stylization.md` (byte-identical STYLE FORMULA). Preserve `design/assets.csv` with the game.

| Asset | Reference |
|---|---|
| Sprites, backgrounds, UI | `game-stylization.md` |
| Spritesheets / 2D animation | `game-2d-animation.md` |
| Tiles, walls, ground, PBR maps | `game-textures.md` |
| Any 3D model / animation | `game-3d-animation.md` |
| Non-humanoid procedural rigs | `game-procedural-animation.md` |
| Music, SFX, voice | `game-audio.md` |
| Historical optional 3D provider recipe and recovery | `game-meshy-api.md` (not a built-in adapter) |
| Image-to-3D input, pose and polygon budgets | `game-meshy-input-rules.md` |

Upstream rig/texture helper scripts are not included. Use the shipped dependency-free GLB inspector and bundled character kit; optional conversion workflows require separately available tooling. Do not rebuild missing tools from memory and claim they were shipped.

## Single-player

Single-player HTML needs no room. A room-driven one-player game uses `multiplayer:true` with logic meta `{minPlayers:1,maxPlayers:1}`. The co-op kit permits starting alone with capacity four. All modes retain the same local validation/publication boundary; none gets persistence or internet hosting automatically.

## Fixed performance budget for the co-op starter

Target 60 fps desktop (16.7 ms) and at least 30 fps on the weakest declared mobile target (33.3 ms); measure in an actual WebGL browser before claiming these targets. Bound visible enemies to 64 and beam instances to 32, use one instanced draw per swarm, at most four animated characters, pixel ratio capped at 1.5, no realtime shadows or postprocessing. Keep the scene under 100 draw calls and 100,000 rendered triangles; verify renderer.info rather than inferring frame time from those counts. Merge static compatible geometry once, skip background rendering, reuse meshes/materials, dispose detached resources. These are kit acceptance targets, not inherited upstream measurements. The upstream numeric-default `build-game.md` was not present in the supplied offline references; do not claim its unpublished defaults were recovered.

## Gameplay trailer jobs

After local publication, offer the optional `openmotion_game_trailer` operation (`id`, `action:"start"|"status"`). HTTP adapters are POST/GET `/api/games/<id>/trailer`, also through `/motion-api/games/`. Only ready/published local games qualify, including read-only bundled templates. POST returns the background job; GET and catalog cards expose its latest `GameTrailer`. Repeated starts while active return the same job; starting after ready/failed makes a fresh recording.

States are `recording → composing → rendering → ready`, or `failed` with a readable stage error. State lives in `trailer/job.json` inside an owned game. Template output lives in the workspace's `game-trailers/<id>/trailer/` overlay, never the installed template. On service restart, an interrupted job becomes failed; it is not silently resumed. Clips remain under `trailer/clips/`; successful MP4 is served at `/api/games/<id>/play/trailer/trailer.mp4`. Private job metadata is not served. This is a local background process, not a durable hosted queue.

Recording uses isolated headless Chrome, 1280×720, three five-second moments separated by short play intervals, with start-button/hook conventions and generic WASD/arrows/Space/click inputs. Canvas/page screencast uses local ffmpeg, with real frame capture as fallback. No desktop attachment or synthetic gameplay footage. Existing Chrome, ffmpeg and pinned native export components are prerequisites; missing components fail without installation/download.

Composition creates a standard native project through `openmotion_create_project`, imports local clips and the game's cover (or a gameplay poster when absent), and writes editable HyperFrames HTML plus deterministic `trailer.json`. Prefer zh-CN title/description/controls. Three highlights make 19 seconds (two supported highlights make 15.5 seconds); include title, brief captions and Play now with controls. Export uses the existing frozen-project/export verification pipeline. Report projectId, status and videoUrl; silent captures do not establish audible quality, human fun, physical-device performance or successful export until ready. Failures retain partial media and project identity.

## Multiplayer entry checks

Apply the [automatic-join acceptance checklist](../SKILL.md#mandatory-multiplayer-entry-acceptance).
