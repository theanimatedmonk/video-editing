# Rough cut and cut audit

## Rough cut

```bash
npx hyperframes transcribe talk.mp4 --json > edit/words.json          # word timings
python3 scripts/rough_cut.py talk.mp4 --words edit/words.json > edit/cuts.json
```

Defaults that suit talking heads: `--noise -35` dB, `--min-silence 0.45` s (shorter pauses are rhythm, keep them), `--pad 0.12` s (keeps breaths natural), `--word-tail 0.08` s (never end a cut within 80 ms of a word ending). Tune noise to the room: run `ffmpeg -i talk.mp4 -af volumedetect -f null -` and set `--noise` about 10 dB above the quiet floor.

Then remove content, not just silence: false starts, repeated takes (keep the last good one), "um, so, basically" openers. Edit `cuts.json` by hand for these; keep `source_in`/`source_out` and recompute `start` as the running sum of durations.

## Cut audit: check the audio, not the transcript

Transcript word times are rounded and often late by 50–150 ms, so cuts built only from them clip last syllables ("edited using A—"). Every time:

```bash
python3 scripts/edge_check.py talk.mp4 edit/cuts.json            # exit 1 = a cut chops sound
```

It measures the 60 ms just outside every edge. Anything louder than −38 dB is sound being thrown away. Move that edge the suggested way and re-run until it prints PASS. Never skip this because the transcript "looks fine".

## Into HyperFrames

Each segment becomes one clip of the same source on the timeline:

```html
<video id="cut-3" class="clip" src="assets/talk.mp4" data-has-audio="true"
  data-start="{start}" data-duration="{duration}" data-media-start="{source_in}" data-track-index="0"></video>
```

Alternate `data-track-index` 0/1 between neighbours so Studio shows each cut clearly. Jump cuts in talking heads hide better with a small punch-in (scale 1 → 1.08 on every other cut, on a wrapper, not on the video).
