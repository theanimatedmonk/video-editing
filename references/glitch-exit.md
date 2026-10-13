# Glitch exit (RGB-split tear while leaving)

The headline tears into pink and cyan bands, skews and flickers out over 0.5 s while it keeps gliding left. The colour copies are CSS pseudo-elements driven by CSS variables, so no extra DOM nodes jump around (the element's own box only skews, its centre never reverses — gates that check for jitter stay green).

## CSS (global)

```css
.glitch { position: relative; --ga: 0; --gx1: 0px; --gx2: 0px; --gt1: 100%; --gb1: 0%; --gt2: 100%; --gb2: 0%; }
.glitch::before, .glitch::after {
  content: attr(data-text); position: absolute; inset: 0;
  opacity: var(--ga); pointer-events: none; mix-blend-mode: screen;
}
.glitch::before { color: #ff3d6e; transform: translateX(var(--gx1)); clip-path: inset(var(--gt1) 0 var(--gb1) 0); }
.glitch::after  { color: #38e8ff; transform: translateX(var(--gx2)); clip-path: inset(var(--gt2) 0 var(--gb2) 0); }
```

Markup repeats the text in `data-text`:

```html
<div class="ln-carry"><h2 id="my-line" class="line-text glitch" data-text="Name any birdcall">Name any birdcall</h2></div>
```

## Timeline (one frame-stepped burst, seeded so every render matches)

```js
function glitchOut(sel, out) {
  const el = document.querySelector(sel);
  let seed = 0;
  for (const ch of sel) seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647;
  seed = seed || 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const band = () => { const top = Math.floor(rnd() * 80); return [top + "%", Math.max(0, 100 - top - 8 - Math.floor(rnd() * 30)) + "%"]; };
  const FLICKER = [1, 0.85, 1, 0.55, 0.9, 0.4, 0.75, 0.25, 0.6, 0.15, 0.35, 0.08, 0.2, 0.04, 0];
  FLICKER.forEach((o, i) => {
    const [t1, b1] = band(), [t2, b2] = band();
    const amp = 8 + i * 4;                         // the tear widens as it dies
    tl.set(el, {
      opacity: o,
      skewX: (rnd() - 0.5) * 14,
      "--ga": i < FLICKER.length - 1 ? 0.95 : 0,
      "--gx1": ((rnd() - 0.5) * 2 * amp).toFixed(1) + "px",
      "--gx2": ((rnd() - 0.5) * 2 * amp).toFixed(1) + "px",
      "--gt1": t1, "--gb1": b1, "--gt2": t2, "--gb2": b2,
    }, out + i / 30);
  });
}
```

Combine with `smooth-line-motion.md`: arrival at `at`, glitch at `out`, carry ends at `out + 0.5`.
