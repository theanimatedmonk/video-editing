# Audio rules

## Volume automation must be versioned (or the export goes silent)

The renderer rejects the unversioned shape with `Unsupported automation version: undefined` and drops all audio, while `hyperframes check` still passes. Always write:

```html
<audio id="music" src="assets/bed.wav" data-start="0" data-duration="25.5" data-volume="0.55"
  data-automation='{"version":1,"lanes":[{"target":"volume","points":[
    {"t":0,"v":0},{"t":0.4,"v":1},
    {"t":0.9,"v":1},{"t":1.15,"v":0.15},{"t":2.4,"v":0.15},{"t":2.8,"v":1},
    {"t":24,"v":1},{"t":25.5,"v":0}]}]}'></audio>
```

Never the old `{"volume":[...]}` form. `t` is seconds from the clip's own start; `data-volume` stays the static level.

## Ducking under a featured sound

Dip the music to ~0.15 over 0.25 s just before the effect, hold, and recover over ~0.4 s after it (the middle points above). Give the effect its own `<audio>` with an `id`, trimmed with `data-media-start`, and a short fade-out lane at its tail.

## Sound effects on cuts

A whoosh's hit lands `peakOffset` seconds into the file: start it `peakOffset` before the cut. Keep whooshes around volume 0.6 under a 0.55 music bed.

## Footage sound

Keep a clip's own sound on its `<video data-has-audio="true">` (no `muted`); mute silent screen recordings. Two audible clips must not share one `data-track-index` at overlapping times.

## Choosing and smoothing the music bed

- Preferred bed: a **lofi beat** (search "chill lofi hip hop instrumental, relaxed groove, warm piano"). Upbeat electronic was too busy; calm ambient was the step between. Pick a track at least as long as the film; library lofi tracks are often 7–24 s, so search twice before looping.
- Match loudness when swapping tracks: `ffmpeg -t <dur> -i bed.wav -af ebur128 -f null -` and compare the integrated `I:` values; keep `data-volume` when they are within 1 LU, otherwise scale it by 10^(−ΔLU/20) (e.g. 4 LU louder → × 0.64).
- Smooth envelope: fade in over about 0.8 s, take a dip down over about 0.35 s and back up over about 0.7 s, and fade out over the last 2 s. Shorter ramps sound like a fader being yanked.

```json
{"version":1,"lanes":[{"target":"volume","points":[
  {"t":0,"v":0},{"t":0.8,"v":0.9},{"t":1.0,"v":0.9},{"t":1.35,"v":0.2},
  {"t":2.3,"v":0.2},{"t":3.0,"v":1},{"t":23.5,"v":1},{"t":25.5,"v":0}]}]}
```

- Studio rewrites the attribute with `&quot;` entities after you edit in the app. Replace the whole `data-automation="..."` or `'...'` attribute with a regex rather than a plain string match, then grep to confirm the new points landed.
