# Learn a style from a reference video

When the person says "make it like this one", measure the reference and turn the numbers into a style document, then into a skill.

## Measure

```bash
sh scripts/watch.sh reference.mp4 edit/ref 2
npx hyperframes transcribe edit/ref/audio.wav --json > edit/ref/words.json
```

From `shots.json` and the sheets, fill in:

| Measure | How |
|---|---|
| Pacing | `cuts_per_minute`, `median_shot` from shots.json |
| Layout mix | tag each sheet frame: full face / split screen / full canvas (no face) / screen recording / text card; report % of frames per tag |
| Captions | position (lower third? centre?), words per caption, case, highlight colour, font weight |
| Type | display and body faces (or nearest free match), sizes relative to frame height |
| Colour | background, 2–3 accents (sample from frames) |
| Motion | how text enters and leaves, transition types and how often each appears, zooms and punch-ins per minute |
| Sound | music under speech? effects on cuts? how loud relative to voice |
| Speech | words per minute (words.json count / duration), hook length before the first cut |

Example of the output: "31% full face, 24% split screen, 45% full canvas with no face; median shot 2.1 s; captions centred, 2–3 words, uppercase, yellow highlight on the stressed word."

## Turn it into a skill

Write `references/styles/<style-name>.md` with the measured numbers as rules ("a face-only stretch never exceeds 6 s", "every 3rd cut is a split screen"), the palette and type, and one example timeline. Add a row for it in `formats.md`. The same method works for colour grading, typography and animation styles.
