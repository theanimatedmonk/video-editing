# Glitch effects (beyond the exit)

The family around `glitch-exit.md`. Same rules: seeded generator, frame-stepped `tl.set` (the stepping IS the digital look), and the element's centre never reverses so jitter gates stay green. Reuses the `.glitch` CSS and `data-text` markup from `glitch-exit.md`.

## Shared seeded generator

```js
function seeded(key) {
  let seed = 0;
  for (const ch of key) seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647;
  seed = seed || 7;
  return () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
}
const band = (rnd) => { const top = Math.floor(rnd() * 80); return [top + "%", Math.max(0, 100 - top - 8 - Math.floor(rnd() * 30)) + "%"]; };
```

## 1. Glitch entry (tear in, snap sharp)

The exit played backwards in spirit: starts torn and flickering, amplitude shrinks, lands perfectly clean. Ends on a hard clean frame.

```js
function glitchIn(sel, at, frames = 12) {
  const el = document.querySelector(sel), rnd = seeded(sel + "in");
  for (let i = 0; i <= frames; i++) {
    const k = 1 - i / frames;                      // 1 → 0, the tear closes
    const last = i === frames;
    const [t1, b1] = band(rnd), [t2, b2] = band(rnd);
    tl.set(el, {
      opacity: last ? 1 : [0.2, 0.7, 0.4, 0.9, 0.6, 1][i % 6],
      skewX: last ? 0 : (rnd() - 0.5) * 14 * k,
      "--ga": last ? 0 : 0.95,
      "--gx1": last ? "0px" : ((rnd() - 0.5) * 40 * k).toFixed(1) + "px",
      "--gx2": last ? "0px" : ((rnd() - 0.5) * 40 * k).toFixed(1) + "px",
      "--gt1": t1, "--gb1": b1, "--gt2": t2, "--gb2": b2,
    }, at + i / 30);
  }
}
```

## 2. Glitch hit (emphasis on a beat, element stays)

A 4–6 frame burst on a line that is already on screen, landing on a beat or a sound effect. Use sparingly: one per scene at most.

```js
function glitchHit(sel, t, frames = 5) {
  const el = document.querySelector(sel), rnd = seeded(sel + t);
  for (let i = 0; i <= frames; i++) {
    const last = i === frames;
    const [t1, b1] = band(rnd), [t2, b2] = band(rnd);
    tl.set(el, {
      skewX: last ? 0 : (rnd() - 0.5) * 10,
      "--ga": last ? 0 : 0.9,
      "--gx1": last ? "0px" : ((rnd() - 0.5) * 30).toFixed(1) + "px",
      "--gx2": last ? "0px" : ((rnd() - 0.5) * 30).toFixed(1) + "px",
      "--gt1": t1, "--gb1": b1, "--gt2": t2, "--gb2": b2,
    }, t + i / 30);
  }
}
```

## 3. Slice displacement (whole block, any element)

For images, cards or a logo, not only text. Stack N copies of the element, each clipped to one horizontal band; bands start shifted sideways and converge to 0 in stepped jumps.

```html
<div class="slices" id="logo-slices">
  <!-- generated: N copies of the same <img>/<svg>, each in .slice -->
</div>
```

```css
.slices { display: grid; }
.slices > .slice { grid-area: 1 / 1; }
```

```js
function buildSlices(sel, n = 8) {
  const box = document.querySelector(sel), src = box.innerHTML;
  box.innerHTML = "";
  const out = [];
  for (let i = 0; i < n; i++) {
    const s = document.createElement("div");
    s.className = "slice";
    s.innerHTML = src;
    s.style.clipPath = `inset(${(i * 100) / n}% 0 ${100 - ((i + 1) * 100) / n}% 0)`;
    box.appendChild(s); out.push(s);
  }
  return out;
}
function sliceIn(slices, at, key, dur = 0.5) {
  const rnd = seeded(key);
  slices.forEach((s) => {
    const dx = (rnd() - 0.5) * 160;
    tl.fromTo(s, { x: dx, opacity: 0 }, { x: 0, opacity: 1, duration: dur, ease: "steps(6)" }, at + rnd() * 0.12);
  });
}
```

`steps(6)` gives the digital stutter; swap to `expo.out` for a smooth "reassemble" version.

## 4. Glitch cut (scene to scene)

Hides a hard cut under 3–4 frames of noise. Put a full-frame overlay above both scenes on the root timeline (anything crossing a cut lives on the root timeline):

```html
<div id="glitch-overlay" class="clip" data-start="0" data-duration="ROOT_LENGTH" data-track-index="90"
     style="position:absolute; inset:0; pointer-events:none;">
  <div class="go-band"></div><div class="go-band"></div><div class="go-band"></div>
</div>
```

```css
.go-band { position: absolute; left: 0; right: 0; height: 6%; opacity: 0; mix-blend-mode: screen; background: linear-gradient(90deg, #ff3d6e, #38e8ff); }
```

```js
function glitchCut(cut) {
  const rnd = seeded("cut" + cut);
  const bands = document.querySelectorAll("#glitch-overlay .go-band");
  for (let f = -2; f <= 2; f++) {
    bands.forEach((b) => tl.set(b, {
      opacity: f === 2 ? 0 : 0.35 + rnd() * 0.5,
      top: (rnd() * 94).toFixed(1) + "%",
      height: (2 + rnd() * 10).toFixed(1) + "%",
      x: ((rnd() - 0.5) * 120).toFixed(0),
    }, cut + f / 30));
  }
  // also shake the outgoing / incoming scene wrappers' x by ±12px on the same frames
}
```

Add a short digital SFX (find_sound_effect "glitch") starting 1 frame before the cut.

## 5. Scanline + noise wash (texture, not a transition)

A static-feeling texture for "retro / VHS / CRT" asks. Pure CSS, no time dependence, so nothing to seek:

```css
.scanlines::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 1px, transparent 1px 3px);
  mix-blend-mode: multiply;
}
```

For moving noise, step a background-position on a noise PNG with `tl.set` every 2 frames (seeded offsets), never a CSS infinite animation.

## Picking one

| Want | Use |
|---|---|
| headline leaves | `glitch-exit.md` |
| headline arrives with attitude | 1 glitch entry |
| punctuate a beat / SFX | 2 glitch hit |
| logo or image arrives / breaks | 3 slice displacement |
| hide a hard scene change | 4 glitch cut |
| retro texture | 5 scanlines |

Taste note: the person likes glitch on exits, soft blur on entries. Default to that pairing; use glitch entries only when the brief is loud or techy.
