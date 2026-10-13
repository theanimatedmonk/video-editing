# The edit pipeline

Every edit runs these stages in order. Each stage has one job and one output, so a problem is caught where it is made, not after a render.

| # | Stage | Output | Stop for approval? |
|---|---|---|---|
| 0 | Asset plan (`asset-plan.md`) | `edit/asset-plan.md` | **Yes**: the person approves before any edit |
| 1 | Watch (`watch-reference.md`) | contact sheets, transcript, shot list for every input and reference | no |
| 2 | Rough cut (`rough-cut.md`) | `edit/cuts.json` | no |
| 3 | Cut audit (`rough-cut.md`, edge check) | edge-check PASS | no: fix and re-run until it passes |
| 4 | Format pick (`formats.md`) | the format named in the plan | no |
| 5 | Build | HyperFrames composition (motion recipes in `../`) | no |
| 6 | Sound | music bed, effects, ducking (`../audio-rules.md`) | no |
| 7 | Checks | `hyperframes check` (and the film gate for launch films) pass | no |
| 8 | Preview | the person watches in Studio and gives notes | **Yes** |
| 9 | Review gate (`review-gate.md`) | a different model's issue list, fixed | no |
| 10 | Rules (`rules-from-corrections.md`) | every note from the person became a rule in `rules/RULES.md` | no |

Keep edit artifacts in an `edit/` folder beside the project (not inside the app's own folders): `asset-plan.md`, `watch/`, `cuts.json`, `review/`.

Before stage 0, read `rules/RULES.md`. Every rule there came from a past correction.
