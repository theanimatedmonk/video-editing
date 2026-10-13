# Glide cut (cut-the-curve + horizontal motion blur)

At every scene change the outgoing scene accelerates left and the incoming scene arrives from the right already moving. The two eases are the halves of one `power4.inOut`, so the speed matches at the cut, and a horizontal blur peaks exactly as the cut lands.

| Side | Move | Ease | Time |
|---|---|---|---|
| Outgoing | `x: 0 → -230`, opacity → 0 | `power4.in` | last 0.33 s of the scene |
| Incoming | `x: 230 → 0`, opacity 0.35 → 1 | `power4.out` | first 0.4 s |
| Blur | stdDeviation `"0 0" → "10 0"` out, `"10 0" → "0 0"` in | same eases | same times |

230 px is about 12% of a 1920 frame. Never push fully off screen.

## Markup (one filter per section, applied to the moving wrapper)

```html
<svg width="0" height="0" style="position: absolute">
  <filter id="hb-scene" x="-10%" y="-5%" width="120%" height="110%" color-interpolation-filters="sRGB">
    <feGaussianBlur id="hb-scene-blur" stdDeviation="0 0"></feGaussianBlur>
  </filter>
</svg>
<div id="scene-hero" style="filter: url(#hb-scene)">…</div>
```

For a phone/video card, put the filter on an inner wrapper around the `<video>` so the card's own `filter` tweens (zoom-through blur) don't fight it.

## Timeline

```js
// outgoing (END = this scene's duration)
tl.to("#scene-hero", { x: -230, duration: 0.33, ease: "power4.in" }, END - 0.33);
tl.to("#scene-hero", { opacity: 0, duration: 0.31, ease: "power2.in" }, END - 0.33);
tl.fromTo("#hb-scene-blur", { attr: { stdDeviation: "0 0" } },
  { attr: { stdDeviation: "10 0" }, duration: 0.33, ease: "power4.in", immediateRender: false }, END - 0.33);

// incoming (next scene, local time 0)
tl.fromTo("#next-hero", { x: 230, opacity: 0.35 },
  { x: 0, opacity: 1, duration: 0.4, ease: "power4.out", immediateRender: true }, 0);
tl.fromTo("#hb-next-blur", { attr: { stdDeviation: "10 0" } },
  { attr: { stdDeviation: "0 0" }, duration: 0.4, ease: "power4.out", immediateRender: true }, 0);
```

`stdDeviation="10 0"` blurs only horizontally — a real motion streak, not a soft-focus fog.

## Carriers make it feel premium

Pair the glide with one object that crosses the cut on a single root-timeline tween (`expo.inOut`, ~0.9 s, straddling the cut): a glowing dot flying from the hardware into the app's "Listening" pill, a logo travelling from a badge into the corner and then into the end card.
