# Watch: see the footage before cutting it

Transcripts lie about pictures. Before editing footage, or copying a reference's style, actually look at it.

```bash
sh scripts/watch.sh <video> edit/watch/<name> 2      # frames at 2 fps -> 4x4 time-stamped sheets (8 s per sheet)
npx hyperframes transcribe edit/watch/<name>/audio.wav --json > edit/watch/<name>/words.json
```

Then read every `sheet-NNN.jpg` in order (`manifest.txt` says what each covers) and write notes as you go: what is on screen, when the speaker looks away, where the screen recording shows the click, where a shot is unusable (blur, someone walking through, a frozen frame).

- 2 fps catches every cut and gesture in talking footage. For fast montage or UI animation, use 4–6 fps on just that range (`ffmpeg -ss A -to B`).
- `shots.json` lists hard cuts (scene detection). Zero cuts in a long clip means one continuous take.
- Read sheets before trusting the transcript for timing; read the audio (`edge_check.py`) before trusting either for cut points.

## Finding moments

Combine the transcript (what is said) with the sheets (what is shown): the strongest hook is usually where both peak together: a reveal on screen while the voice lands the point.
