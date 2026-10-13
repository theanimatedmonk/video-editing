# Stage 0: asset plan (wait for approval)

Before editing anything, write `edit/asset-plan.md` and stop until the person approves it. A wrong plan costs one message to fix; a wrong render costs a re-render.

## What goes in the plan

1. **Deliverable**: length, aspect ratio, platform, format (from `formats.md`).
2. **Every input, classified**: one row per file.

| File | Kind | Use | Notes |
|---|---|---|---|
| `talk.mp4` | A-roll (face + voice) | spine of the edit | 12:40 raw, dead air to cut |
| `screen.mov` | screen recording | B-roll during the demo | silent: mute |
| `logo.svg` | brand mark | end card only | |
| `mic.png` | photo | hook, full-screen zoom | 582 px wide: soft above about 2x |

Kinds: A-roll, B-roll, screen recording, photo, logo, chart/data, music, sound effect, voiceover.

3. **Every visual still needed**: what is missing and where it will come from (library search, generation, a screenshot to capture). Paid generation is named here so the person approves the spend.
4. **Every claim fact-checked**: each number, name, price or quote that appears on screen, checked against its live source (open the page). Record the source URL and the date checked. A claim that cannot be verified is flagged, not shown.
5. **Beat outline**: one line per section: time range, what is seen, what is said or written.
6. **Sound plan**: music mood, which effects, where the music ducks.

## Rules

- Measure inputs first (`ffprobe`, `watch.sh`), never guess durations or resolutions.
- Small images get a warning: shown above 2x their pixel size they go soft.
- End the plan with an explicit question: "Approve this plan, or tell me what to change."
