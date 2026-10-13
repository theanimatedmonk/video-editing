---
name: video-editing
description: Tested motion recipes for HyperFrames / GSAP videos — glide cuts with horizontal motion blur, glitch text exits, smooth never-parked headline motion, animated vector songbirds that bank and chirp, a big-number-to-logo-orbit reveal, and the audio rules that keep exports from going silent. Use when building or polishing a HyperFrames composition and the ask is smoother or cooler transitions, text that glitches out, nicer text motion, animated birds or characters, a stat reveal, or music ducking under a sound effect.
---

# Video editing recipes

Each recipe below was built and checked in a real HyperFrames film (seek-safe GSAP, one paused timeline per composition, passes `hyperframes check` and the moment-film gate). Open the reference file for the copy-ready code and the timing numbers.

| Recipe | Use it for | File |
|---|---|---|
| Glide cut | scene changes that feel like one continuous glide | `references/glide-cut.md` |
| Glitch exit | headlines that tear into RGB bands as they leave | `references/glitch-exit.md` |
| Smooth line motion | text that drifts in softly and never parks | `references/smooth-line-motion.md` |
| Vector songbirds | cute flying birds that bank along arcs, beat wings, chirp | `references/vector-songbirds.md` |
| Number → orbit | a big stat resolves through pixels, dissolves, becomes tiles orbiting a badge | `references/number-to-orbit.md` |
| Audio rules | music ducking, sound effects, automation format | `references/audio-rules.md` |
| Style notes | the taste calls that landed | `references/style-notes.md` |

## Rules that apply to every recipe

- One move = one tween with one ease. Two moves on one element go on nested wrappers, one property each.
- Never tween `visibility`/`display`/`autoAlpha` on a `.clip`; animate a child.
- No CSS `transform` on an element GSAP also moves; set the start inside `fromTo` (or `tl.set(..., 0)` then `tl.to`).
- Blur a wrapper, never a `<video>` directly.
- Deterministic only: seeded random (`seed = seed * 16807 % 2147483647`), no `Math.random`, no clocks, finite `repeat`.
- A sub-composition timeline cannot reach host elements; anything that crosses a scene cut lives on the root timeline in root seconds.
