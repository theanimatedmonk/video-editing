---
name: video-editing
description: The user's video editing workflow and tested motion recipes for HyperFrames / GSAP. Use for any request to edit, cut, or polish a video ("edit this reel", "cut the dead air", "make it like this reference", "review the render"): it routes to a format, runs the pipeline (asset plan approved first, watch the footage, rough cut, audio edge check on every cut, build, review by a different model, every correction saved as a rule). Also use for glide cuts with motion blur, glitch text exits, smooth headline motion, animated vector songbirds, a big-number-to-logo-orbit reveal, music ducking, and audio automation that keeps exports from going silent.
---

# Video editing

## Start here, every time

1. Read `rules/RULES.md`. Every rule there is a past correction; do not make it again.
2. Pick the format from `references/workflow/formats.md` (the router). If two fit, ask.
3. Run the pipeline in `references/workflow/pipeline.md`, stage by stage. Stage 0 (asset plan) waits for the person's approval.
4. When the person gives a note, fix it AND add a rule (`references/workflow/rules-from-corrections.md`).

## Workflow stages

| Stage | Guide | Script |
|---|---|---|
| Asset plan + fact check (approval) | `references/workflow/asset-plan.md` | |
| Watch footage / a reference | `references/workflow/watch-reference.md` | `scripts/watch.sh`, `scripts/shot_stats.py` |
| Rough cut (dead air, keep words whole) | `references/workflow/rough-cut.md` | `scripts/rough_cut.py` |
| Cut audit (listen to every edge) | `references/workflow/rough-cut.md` | `scripts/edge_check.py` |
| Learn a style from a reference | `references/workflow/style-from-reference.md` | `scripts/watch.sh` |
| Review gate (a different model) | `references/workflow/review-gate.md` | `scripts/review_pack.sh` |

Scripts need only `ffmpeg`/`ffprobe` and Python 3 (standard library). Run them with paths to the skill folder, e.g. `python3 ~/.claude/skills/video-editing/scripts/rough_cut.py talk.mp4`.

## Motion recipes

| Recipe | Use it for | File |
|---|---|---|
| Glide cut | scene changes that feel like one continuous glide | `references/glide-cut.md` |
| Glitch exit | headlines that tear into RGB bands as they leave | `references/glitch-exit.md` |
| Smooth line motion | text that drifts in softly and never parks | `references/smooth-line-motion.md` |
| Vector songbirds | shaded birds that bank along arcs, beat wings, chirp | `references/vector-songbirds.md` |
| Number → orbit | a big stat resolves through pixels, dissolves, becomes tiles orbiting a badge | `references/number-to-orbit.md` |
| Audio rules | music ducking, sound effects, automation format | `references/audio-rules.md` |
| Style notes | the taste calls that landed | `references/style-notes.md` |

## Rules for every HyperFrames build

- One move = one tween with one ease. Two moves on one element go on nested wrappers, one property each.
- Never tween `visibility`/`display`/`autoAlpha` on a `.clip`; animate a child.
- No CSS `transform` on an element GSAP also moves; set the start inside `fromTo` (or `tl.set(..., 0)` then `tl.to`).
- Blur a wrapper, never a `<video>` directly.
- Deterministic only: seeded random (`seed = seed * 16807 % 2147483647`), no `Math.random`, no clocks, finite `repeat`.
- A sub-composition timeline cannot reach host elements; anything that crosses a scene cut lives on the root timeline in root seconds.
- Editing and reviewing are separate jobs: never sign off your own render without the review gate.
