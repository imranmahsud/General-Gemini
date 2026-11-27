> See [source and execution notes](../PROVENANCE.md).

# Animated 3D Characters (rigged GLB pipeline)

> **Asset reference for game-generation.** Use for ANIMATED (rigged, multi-clip)
> GLB characters in 3D games — walk/run/attack clips, FBX→GLB conversion that
> preserves all clips, CC0 character sources, the Meshy image→3D→rig→animations
> pipeline, and the procedural branch for non-humanoid creatures. **Mandatory for
> every 3D asset — creating a model or animating it; never model or animate 3D
> without this reference.** Static-only meshes follow the same image→3D steps
> (`game-meshy-api.md`) and stop before the rigging step.
> Style: concept/reference images for 3D follow the
> 3D rules in `game-stylization.md` §8 (white background, three-quarter
> isometric view, formula in the concept prompt, token in `texture_prompt`).

> **OpenMotion replacement:** pick a bundled CC0 character first. The upstream image→3D→rig→animation recipe uses `image_to_3d`, `should_texture`, `enable_rigging`, `enable_animation`, `animation_action_id` and extra clips via `3d_rigging`. There is no built-in equivalent for these model families or animation preset discovery. Only an actually available provider may support such operations; inspect its live schema and price and obtain approval. Otherwise use the bundled GLBs or a supplied local Blender workflow. No raw-provider fallback is authorized automatically, and no shared workspace-credit pool exists.

`sam_3_3d` only makes STATIC meshes. When the user
needs characters that walk/run/attack in Three.js or a game engine, use this
pipeline. Verified end-to-end on 2026-06-10 in the Higgsfield sandbox.
The upstream scripts (not bundled here) are reconstructions of that verified logic —
smoke-test on a small asset before a long batch run.

## Decision table

| Need | Path |
|---|---|
| Stylized game character, fast, zero manual steps | CC0 packs (KayKit/Quaternius) → convert → done |
| CUSTOM character from text/image, zero manual steps, free | 2D→3D rig-transfer pipeline (Step 4 below) — fully local, but skinning quality is rough on image-to-3D meshes; user rejected it for production. Prefer the native 3D tool |
| Custom-look humanoid, best skinning quality | Generate T-pose ref → user runs Mixamo manually (no API!) → user gives FBX → convert here |
| Fully automated 2D→animated GLB, best quality, paid | **Optional external 3D recipe (not built in)**: inspect `image_to_3d`, select an action with the available provider animation catalogue (no built-in OpenMotion rigging preset service), then create with texture, rigging, animation, A-pose, and the chosen integer action ID. Extra clips use `3d_rigging` on the result GLB, then merge locally. **Before any submit read `game-meshy-input-rules.md`.** OpenMotion uses configured providers, current quoted prices and approval; there is no built-in 3D/rigging adapter. Use bundled GLBs if unavailable. |
| Non-humanoid CREATURE (dragon, quadruped, snake, spider, fish) | The auto-rig is humanoid-only (non-bipeds rig poorly or fail). Options: (a) Tripo3D API — rig types quadruped/hexapod/octopod/avian/serpentine/aquatic + locomotion presets (needs Tripo key, unverified); (b) **Procedural branch — VERIFIED on a dragon**: build skeleton+weights+sine-based clips in headless Blender, `game-procedural-animation.md` + `scripts/proc_rig_dragon.py`/`proc_weights.py`/`proc_anim_dragon.py` |
| Non-rigged props (doors, drones, slimes, turrets) | Procedural animation in Three.js code — no rig needed |

**Mixamo has NO official API.** Internal REST API exists but auto-rig marker
placement is interactive-only; browser automation is fragile (Adobe login,
captcha). Don't promise Mixamo automation — frame it as "one manual step,
once per character".

### Optional provider parameter recipe (no built-in 3D adapter)

```text
Parameter translation brief (not a shell command). Map only supported fields; do not forward historical flags blindly.
DISCOVER/INSPECT available model using openmotion_media_use action=models: image_to_3d
OPTIONAL external animation catalogue (not bundled) --query idle --json
REQUEST via openmotion_generate_asset after supported-schema mapping, stated cost and approval: image_to_3d \
  --image ./character-reference.png \
  --should_texture true \
  --enable_rigging true \
  --enable_animation true \
  --pose_mode a-pose \
  --animation_action_id <integer> \
  --wait \
  --json

```

Inspect `openmotion_media_use action=models (inspect model) 3d_rigging` before requesting extra clips because the
accepted source-media field is contract-driven.

## Step 1 — Headless Blender in the sandbox (no root)

`apt-get install` fails (no sudo). Use the portable build:

```bash
cd <workspace> && mkdir -p blender && cd blender
curl -sL -o blender.tar.xz https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz   # ~336MB, run in background
tar xf blender.tar.xz
```

Binary fails with `libSM.so.6: cannot open shared object file`. Fix without
root by downloading debs to a local apt state and extracting:

```bash
mkdir -p aptstate aptcache libs deb
apt-get -o Dir::State::Lists=./aptstate -o Dir::Cache=./aptcache -o Debug::NoLocking=1 update
cd deb && apt-get -o Dir::State::Lists=../aptstate -o Dir::Cache=../aptcache -o Debug::NoLocking=1 \
  download libsm6 libice6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libgl1 libglx0 libglvnd0 libegl1 libopengl0
for d in *.deb; do dpkg -x "$d" ../libs/; done
export LD_LIBRARY_PATH=<workspace>/blender/libs/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
./blender-4.2.3-linux-x64/blender -b --version   # must print version
```

Pitfall: plain `apt-get download libsm6` fails with "Unable to locate package"
because the default list dir is unreadable — the local `Dir::State::Lists`
override is mandatory.

## Step 2 — FBX → GLB with ALL animation clips

**CRITICAL PITFALL:** naive `import_scene.fbx` + `export_scene.gltf` exports
only ONE clip (the active action, e.g. `Rig|T-Pose`) even when 76 actions
imported. Fix: push every action onto an NLA track before export, and export
with `export_animation_mode='NLA_TRACKS'`. Use `scripts/fbx2glb.py`:

```bash
blender -b -P scripts/fbx2glb.py -- input.fbx output.glb
```

This also strips the `Rig|` prefix so Three.js clip names are clean
(`Idle`, `Walking_A`, ...), recomputes normals outward, and forces materials
to OPAQUE (see Material pitfall below).

## Step 3 — Verify the GLB

Run `node scripts/game-glb-inspect.mjs output.glb` (no dependencies); for the additional upstream checks use a separately supplied `glb_inspect.py` — prints clip count,
clip names, skins/meshes/images, material alphaMode, and root-bone scale
channels per clip. A correct character GLB has skins ≥ 1 and the expected
clip count. If clips == 1 and the name contains `T-Pose`, the NLA step was
skipped. If any clip's root scale ≠ 1.0, see the Meshy scale pitfall below.

## Step 4 — 2D image → animated GLB (rig transfer, fully automated, verified)

Full chain with zero manual steps and no external services:

1. `z_image` text-to-image: character in **strict T-pose**, 3/4 view, plain
   white background, full body, matte materials (3d-generation composition
   rules). T-pose matters — the donor skeleton's rest pose is T-pose.
2. `sam_3_3d` on that image → static textured GLB (no skins, no anims).
3. `scripts/rig_transfer.py` — borrows the skeleton + ALL animations from a
   rigged donor FBX (KayKit knight or any Mixamo rig):
   `blender -b -P scripts/rig_transfer.py -- target_static.glb donor.fbx out.glb`
   It scales/aligns the donor armature to the target's bbox, transfers skin
   weights, fixes normals, exports all clips via NLA tracks.

**Critical pitfalls baked into the script (do not regress):**
- `parent_set(type='ARMATURE_AUTO')` (bone heat) FAILS on image-to-3D meshes
  ("failed to find solution for one or more bones") — photogrammetry-style
  topology. Use **Data Transfer of vertex weights from the donor's body
  meshes** instead (`data_transfer`, `VGROUP_WEIGHTS`, `POLYINTERP_NEAREST`).
- `data_transfer` direction: with `use_reverse_transfer=False` it goes
  **ACTIVE → SELECTED** — the weight source must be the ACTIVE object. Getting
  this backwards silently produces 0 weighted verts (and `skins: 0` in the
  exported GLB). Always verify weighted-vert count > 0 before export.
- One donor (e.g. a one-time manual Mixamo session, or KayKit) animates
  unlimited generated characters — the donor is reusable.

Quality limits to state honestly: skinning quality depends on donor/target
proportion similarity; humanoid T-pose targets only; thin dangling parts
(capes, skirts) inherit approximate weights.

## Step 5 — Meshy clip merge + root-scale check (MANDATORY for Meshy)

Meshy returns one GLB per animation. Two merge options:

- **No Blender needed (preferred for Meshy outputs, VERIFIED on a live run
  2026-06-11):** `python3 scripts/glb_merge_anims.py rigged.glb walk.glb:Walk
  run.glb:Run idle.glb:Idle attack.glb:Attack out.glb` — stdlib-only, remaps
  clips by node NAME, applies the root-scale fix and OPAQUE patch
  automatically.
- Blender path (when the scene needs other edits anyway):
  `blender -b -P scripts/merge_anim_glbs.py -- rigged.glb idle.glb:Idle attack.glb:Attack out.glb`.

**Scale pitfall (verified bug):** Meshy *library* animations (via
`/animations`) can bake a scale factor into the root bone's scale channel
(observed: `Hips` scale 1.176 on `idle` while walk/run from the rig were 1.0)
— the character visibly "grows" when that clip plays. Fix after every merge:
check root-bone scale channels in all clips; if min/max ≠ 1.0, zero the scale
to 1.0 AND divide the same clip's root translation by the same factor
(otherwise the character floats). `merge_anim_glbs.py` does this
automatically; `glb_inspect.py` reports it.

## Material pitfall — alphaMode: BLEND masquerading as inverted normals

FBX import into Blender often sets materials to blend/transparent; the export
inherits it as glTF `alphaMode: BLEND`. In Three.js BLEND renders without
depth-write and sorts by object centers, so back faces (face, helmet
interior) draw ON TOP of front faces — visually identical to inverted
normals, but geometry is fine. Telltale difference: with BLEND you see
correctly-lit "innards"; with truly inverted normals the model is dark/black.

Fix layers (all baked into the scripts):
1. **Geometry**: `normals_make_consistent(inside=False)` on every mesh before
   export. Sanity check: mean dot(poly normal, poly center − mesh centroid)
   should be positive.
2. **Material**: force `alphaMode: OPAQUE` + `doubleSided: true`. Belt and
   suspenders: `scripts/glb_patch.py` (stdlib) patches the JSON chunk of any
   existing GLB directly — use it on files you didn't export yourself.
3. **Renderer side**: thin one-sided surfaces (capes, cloth planes) still look
   "inverted" from the back in Three.js — `material.side = THREE.DoubleSide`.
4. **Cache trap**: after re-exporting a fixed GLB to a deployed site, the CDN
   keeps serving the old file despite hard refresh — rename the asset
   (`knight_v2.glb`) instead of fighting the cache.

## Headless-browser limitation

The upstream controlled browser reported **no WebGL** (`webglAvailable: false`); detect support in the current browser —
a deployed Three.js viewer renders as a blank white canvas in browser_vision
screenshots even when it works fine. Verify via DOM/console probes (button
count, mixer status text, fetch HEAD on the GLB) and ask the user to confirm
visuals in their own browser. Do not conclude "the site is broken" from a
white canvas screenshot.

## CC0 asset sources (no attribution, commercial OK)

- **KayKit Adventurers** — `git clone --depth 1 https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0.git`
  → `addons/kaykit_character_pack_adventures/Characters/gltf/*.glb` already
  contain all 76 clips (Knight, Mage, Rogue, Barbarian + Rogue_Hooded); the
  `Characters/fbx/` versions are the conversion test bed. Clips include Idle,
  Walking_A/B/C, Running_A/B, Jump_*, 1H/2H_Melee_Attack_*, Spellcast_*,
  Block*, Death_A/B, Dodge_*, Hit_*, Sit_*, Cheer, Interact, PickUp, Throw.
- **Quaternius** (quaternius.com) — low-poly animated characters, CC0.
- **Kenney** (kenney.nl/assets) — game kits, CC0.

## Delivery pitfalls

- local asset copying (binary uploads are not exposed by game_write_files) REJECTS `.glb` ("Invalid or blocked file extension") —
  copy the binary GLB with authorized local filesystem access; do not encode it into game_write_files. A ZIP upload is not required for local publication.
- In Three.js consume via `GLTFLoader` + `AnimationMixer`;
  `mixer.clipAction(THREE.AnimationClip.findByName(gltf.animations, 'Idle'))`.
- Cross-fade clips: `next.reset().fadeIn(0.25).play(); prev.fadeOut(0.25)`.
- **Disk overflow (happened once):** portable Blender (~1.5 GB unpacked) +
  multi-GLB batches can fill the sandbox disk; the system may wipe and
  recreate the whole workspace mid-task. Mirror deliverables early (deployed
  site folder, uploaded zips, CDN links) and clean up tarballs/intermediates
  as you go — losing the workspace must not lose the assets.

## Support files

- `scripts/fbx2glb.py` — Blender CLI converter preserving all clips (NLA tracks, normals fix, OPAQUE).
- `scripts/glb_inspect.py` — stdlib GLB inspector: clips, skins, alphaMode, root-scale channels.
- `scripts/glb_patch.py` — stdlib JSON-chunk patcher: force OPAQUE/doubleSided on any GLB.
- `scripts/rig_transfer.py` — static GLB + rigged donor FBX → animated GLB (Step 4).
- `scripts/glb_merge_anims.py` — stdlib merger of single-clip GLBs (Meshy outputs) + root-scale fix, no Blender (Step 5, verified live).
- `scripts/merge_anim_glbs.py` — same merge via Blender CLI (when Blender is already in play).
- `scripts/proc_rig_dragon.py` — procedural skeleton from bbox analysis (non-humanoids).
- `scripts/proc_weights.py` — distance-based skin weights (ARMATURE_AUTO is broken headless).
- `scripts/proc_anim_dragon.py` — sine-based idle/fly clips baked to keyframes.
- `game-meshy-api.md` — verified Meshy API pipeline: image→3D→rig→animations, endpoints, action_id catalog, stuck-refine recovery, costs.
- `game-meshy-input-rules.md` — MANDATORY pre-submit rules: input-image validation (character sheets MUST be cropped to one figure or split into multi-image views; pose_mode), low-poly paths (`model_type: lowpoly` vs `target_polycount`), polycount budgets per asset class, payload templates. Read BEFORE building any Meshy request.
- `game-procedural-animation.md` — non-humanoid branch: skeleton/weights/clip recipes per creature type, vision-QC loop, phase-sampling pitfall.

## Exact offline character-kit path

1. Pick `templates/game-kits/characters/Mage.glb` (caster) or `Knight.glb` (melee); keep `LICENSE-KayKit.txt`. Both keep 12 common clips (Idle, Walking_A, Running_A, Jump_Full_Short, Dodge_Forward, Spellcast_Shoot, 1H_Melee_Attack_Chop, 1H_Ranged_Shoot, Block, Hit_A, Death_A, Cheer) and 41 bones, trimmed from the 76-clip originals to stay under 1 MiB. See the character README for measured durations; fetch the full KayKit pack for other clips.
2. Run `node scripts/game-glb-inspect.mjs templates/game-kits/characters/Mage.glb` (or Knight) before choosing clip names. Check skins ≥1, bone count, triangle count, and nonzero moving clips. Poses have duration zero. The inspector does not merge clips or validate root scale.
3. Copy the selected GLB and local `vendor/` into the game. Import `./vendor/three.module.min.js`, `./vendor/GLTFLoader.js`, `./vendor/SkeletonUtils.js`. Load `./characters/Mage.glb`; use `SkeletonUtils.clone(gltf.scene)` per player, never Object3D.clone for independent skinned rigs.
4. Explicit clip map: idle → `Idle`, run → `Running_A`, attack → `Spellcast_Shoot` (Mage) or `1H_Melee_Attack_Slice_Horizontal` (Knight), hit → `Hit_A`, death → `Death_A`. Resolve with `THREE.AnimationClip.findByName`; report missing clips instead of silently assuming them. The starter switches idle/run/attack, plays Hit_A for authoritative hurt events and Death_A while downed, then returns to idle/run after a server revive.
5. Create one `THREE.AnimationMixer` per clone. On a state transition call `next.reset().fadeIn(0.25).play(); previous?.fadeOut(0.25)`; update each visible mixer's delta every render. For one-shot death/hit set `LoopOnce`, `clampWhenFinished=true`, and transition deliberately; do not reset the same clip every frame.
6. Measure a Box3 before scaling: set the current starter character height to 2.4 world units (the previous 1.8-unit skeleton was smaller), offset by `-box.min.y * scale` so feet sit on the ground. In the supplied kit +Y is up and +Z is forward; face `Math.atan2(aimX, aimZ)` and confirm the facing visually. Keep root scale stable across clips; test feet and material opacity in the browser.
7. Merge static geometry with the local `BufferGeometryUtils.mergeGeometries` once after applying transforms. Share materials. Never merge skinned bodies into a static mesh. Instance enemy swarms/projectile beams; do not create one draw-call mesh per enemy.
8. Enforce the fixed starter performance budget in `game-flow.md`: 20 Hz simulation/10 Hz inputs, 4 animated players, ≤64 enemies, ≤32 beams, ≤100 draws, ≤100k rendered triangles, DPR≤1.5, 60 fps desktop/30 fps weakest target. Mage is 5,683 mesh-definition triangles; Knight is 6,952. Verify renderer.info and measured frame times; counts alone do not establish fps.
9. Stop hidden/background rendering and audio; free obsolete mixers, geometry/materials/textures on scene teardown (shared resources only once). Test actual keyboard/mouse and touch play, load/error recovery, clip crossfades and two local clients. Human visual acceptance remains separate.
