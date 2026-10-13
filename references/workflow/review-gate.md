# Review gate: a different model reviews the render

The model that made the edit is blind to its own mistakes. After a render, a *different* model looks at frames from every section and listens to the numbers, and lists problems before the person sees anything.

## Build the pack

```bash
sh scripts/review_pack.sh renders/final.mp4 edit/review 1     # one frame per second, 3x3 sheets + audio report
```

`audio-report.txt` catches the silent-export class of bug: a mean volume near −91 dB, or no audio track, means the mix failed.

## Run the reviewer

Spawn a subagent on a different model from the editor (for example `model: "sonnet"` when editing on Opus, or the reverse), give it the pack paths and this brief, and tell it not to edit files:

> You are reviewing a finished video before the client sees it. Read every `review-NNN.jpg` in order (each tile is stamped with its time) and `audio-report.txt`. List every problem with its timestamp: text cut off or overlapping, a line on screen too briefly to read (under about 0.3 s per word), frames that are empty or frozen, a jump that reads as a glitch, a logo or claim that looks wrong, captions out of the safe area, colour or brightness jumps between shots, audio too quiet (below about −16 LUFS) or clipping (true peak above −1 dBTP), silent stretches. Rank by severity. Say "no issues" only if you looked at every sheet.

If `GEMINI_API_KEY` is set, `npx hyperframes snapshot --at <times> --describe "<question>"` gives a second independent look at specific moments.

## After the review

Fix every high-severity item, re-render, and re-run the pack until the reviewer finds nothing high. Then show the person. Anything the reviewer caught that a rule could have prevented goes into `rules/RULES.md`.
