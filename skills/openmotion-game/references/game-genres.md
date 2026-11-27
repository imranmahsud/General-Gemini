# Genre recipes and quality floor

Read this after the design system and before writing code. Pick the recipe that matches the brief (or the closest one for a free-form brief), copy its acceptance list into `design/plan.md`, and verify each item in `design/verification.md`. These are floors, not ceilings.

## 1. Quality floor for every game

**Game-first screen.** The playfield fills the viewport from the first frame. The title or end card is one small centered overlay (title, one-line goal, one big button) that disappears on the first input. Never lay the page out as a landing page: no hero headline, marketing slogan or feature list beside the game, no game framed in a small box inside a web page. HUD text stays on the edges and stays short. One tap, click, Enter or Space starts the game within one second of load.

**Readable goal in three seconds.** The first screen states the goal in under 12 words and shows the controls as short key or touch hints. A first-time player must know what to do without reading a paragraph.

**Feel (juice).** Every player action and every important event gets feedback within one frame: at least three of screen shake, hit-stop, particles, floating score or damage numbers, flash, squash and stretch, and a synthesized WebAudio sound. Count and name them in `design/verification.md`.

**Session shape.** One run lasts 30–120 s for arcade and party games (story and puzzle games may run longer but must checkpoint). Difficulty ramps on a stated curve. Death or loss to restart takes two seconds or less. Show the score and a locally stored best score at the end.

**Art floor.** Use one palette with named roles from the style formula. Characters and key objects need a readable silhouette (a head, a face, a shape language), not bare circles or boxes. Prefer bundled CC0 assets (`characters/` KayKit models in 3D drafts) over primitives, and code-drawn sprites with outlines, highlights and two-tone shading over flat fills. If the user approves paid generation, use it for the cover and the 2–6 most visible sprites first. Never ship placeholder geometry as the hero.

**Touch.** Implement touch controls that fit the genre (tap, drag, on-screen stick, big buttons at least 56 px). Portrait games must be fully playable at 390×844 with thumbs.

**Test hook.** Expose `window.__omGame = { getState, getStats, sendAction }`; `getState()` returns `selfId`, `players[selfId]` with `x`/`z`, `phase` (`playing`, `win`, `loss` or the kit's phases) and `result`. Export `pilot(state)` and build `referenceRoute` from it so `openmotion_game_simulate` proves the game can be won and that idle loses.

## 2. Starter kits

- **coop-3d**: multiplayer shooter or 3D briefs. Three.js arena, KayKit Mage/Knight, rooms, revive, waves.
- **arcade-2d**: everything else. A full-screen canvas, fixed-step local loop over `logic.js`, keyboard, mouse, touch and one-button input, juice helpers, best score, a portrait/landscape switch and the test hook. It ships a tiny "catch sparks, dodge rocks" sample. Replace the sample rules, art and strings, but keep the loop, input layer, hook and pilot/referenceRoute pattern. For 3D single-player briefs, keep the arcade-2d input, loop and hook, and render with the vendored Three.js.
- If your draft lacks the kit you need, read it from `templates/game-kits/<kit>/` when your host can read files. Otherwise build the same structure yourself.

## 3. Recipes

Each recipe lists the core loop, the must-haves and the acceptance checks.

**Platformer.** Run, jump, reach the exit. Must have: coyote time (about 0.1 s), jump buffering, variable jump height, a camera that leads the player, at least one full level with a checkpoint and an exit, at least two hazard or enemy types, stomp or attack, collectibles with a count. Pixel style: integer scaling and `image-rendering: pixelated`. Accept: reference route reaches the exit; idle loses on a timer or hazard; touch has left, right and jump.

**One-button / hypercasual.** One input (tap, click, Space, Enter) does everything. Must have: under 3 s to understand, a skill timing window that tightens over time, instant restart, score plus best, a near-miss or perfect bonus, strong juice on every input. Accept: only one input is bound; difficulty measurably ramps (log the window or speed per minute); death to restart ≤ 2 s.

**Racing.** Laps or a timed course with rivals. Must have: track bounds, at least two AI racers that follow a racing line and can overtake, a position readout (1st/2nd/…), lap or checkpoint counter, boost or drift, a finish screen with place and time. Accept: reference finishes first; idle finishes last or times out; touch has steer and throttle.

**Horror / puzzle escape.** Explore, find clues, escape under threat. Must have: at least two chained puzzles (for example find a code → open a safe), a threat with telegraphed approach (sound or light cues), a fail state, darkness with a light source, fog and an ambient sound bed, a readable interaction prompt. Accept: reference escapes; idle is caught or runs out of time; every clue is reachable on touch.

**Story / visual novel.** Read, choose, reach an ending. Must have: a portrait or background per scene in one consistent style, a typewriter text box that a tap completes and a second tap advances, at least three choices that change later text, at least two distinct endings, a chapter or scene restart, a choice log or back-log. Accept: the reference route reaches an ending; an alternate route reaches a different ending; text is readable at 390×844.

**Co-op survival (zombies and friends).** The coop-3d kit's loop with enemies themed to the brief. Must have: three or more enemy types, waves with a boss, revive, ammo or resource pickups, a reason to stand together. Accept: the multiplayer checks in the flow reference plus reference-win and idle-loss with 1 and 2 players.

**Versus reaction / party.** 2–4 players compete in short rounds. Must have: the server decides signal timing and order (clients never send their own timestamps), a false-start penalty, 10–20 rounds in about a minute, a live scoreboard and a final ranking, big portrait buttons. Accept: two clients in one room see the same round; the earlier server-received tap wins; a false start is penalized.

## 4. Playable ads (pull-the-pin, eat-and-grow, crowd runner, merge)

A playable ad is a 15–60 s mini game that sells itself in the first touch. Must have:
- **Portrait first**: design at 9:16 (`ORIENTATION = 'portrait'` in arcade-2d); set metadata `orientation: "portrait"` when the tool supports it.
- **Instant play**: interactive on the first frame. Show a hand or finger tutorial animation on the exact element to touch until the first input. No title screen.
- **Satisfying physics or numbers**: many small bodies (coins, balls, crowd members) with cheap custom physics; big growing numbers, ×2/×5 gates, combo popups.
- **Short levels**: 3–8 levels of 10–20 s each, with an obvious first win, a near-fail on level 2 or 3 and a twist (moving parts, a thief, a boss).
- **End card**: after the last level or a fail, show a full-screen end card with the score, "Play again" and a clear call to action button (text from the brief, default "Play the full game").
- **Performance**: cap the body count; keep 60 fps at 390×844 in software rendering by using 2D canvas or instanced meshes.

**Pull the pin.** Pins are draggable or tappable bars that block chambers. Pulling a pin releases its contents under gravity. Wrong order spills into hazards. Accept: each level has exactly one correct order that the reference performs; idle never wins.

**Eat and grow.** Swallow smaller things to grow; avoid bigger ones; size thresholds unlock bigger prey; a timer per area; upgrades between rounds. Accept: size visibly scales the camera; reference reaches the final size; idle fails the timer.

**Crowd runner.** A crowd auto-runs forward, the player steers through +N / ×N gates, and the crowd fights an army or boss whose number must be lower. Accept: the gate math is correct; the reference beats the boss; idle loses at the first red gate or the boss.
