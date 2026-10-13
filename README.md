# video-editing

A Claude Code skill: a full video-editing workflow plus tested motion recipes for HyperFrames / GSAP compositions.

Install: clone into `~/.claude/skills/video-editing` (the folder name is the skill name). Needs `ffmpeg`, `ffprobe` and Python 3; no Python packages.

## Workflow (`references/workflow/`)

| Stage | What it does |
|---|---|
| `formats.md` | the router: picks one edit format (talking-head reel, podcast clips, product promo, screen-recording explainer, …) |
| `pipeline.md` | the stages in order, and where the person approves |
| `asset-plan.md` | stage 0: classify every input, fact-check every on-screen claim, wait for approval |
| `watch-reference.md` | look at footage as 2 fps contact sheets before cutting |
| `rough-cut.md` | cut dead air keeping words whole, then audit every cut edge by ear (the audio, not the transcript) |
| `style-from-reference.md` | measure a reference video (pacing, layout mix, captions, type, colour) and turn it into a style skill |
| `review-gate.md` | a different model reviews frames from every section and the audio numbers |
| `rules-from-corrections.md` | every note becomes a rule in `rules/RULES.md` |

## Scripts (`scripts/`)

| Script | Does |
|---|---|
| `watch.sh <video> <out> [fps]` | time-stamped 4x4 contact sheets, audio for transcription, shot list |
| `shot_stats.py <video>` | cut times, cuts per minute, mean and median shot length |
| `rough_cut.py <media> [--words words.json]` | keep segments without dead air; moves edges off words |
| `edge_check.py <media> <cuts.json>` | fails if any cut chops sound |
| `review_pack.sh <render> <out>` | review contact sheets + loudness, true peak and silent-export check |

## Motion recipes (`references/`)

Glide cut, glitch exit, smooth line motion, vector songbirds, number → orbit, audio rules, style notes.

## Rules (`rules/RULES.md`)

The growing list of corrections. Read before every edit; add to it after every note.
