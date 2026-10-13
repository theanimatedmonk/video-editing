# Smooth line motion (drift in, never park)

Fast slam-ins (most of the travel in the first fifth) read as jarring. What landed instead: the line fades in from a soft blur with a small slide, while a wrapper carries it left at a constant speed for its whole life. The speeds add up, so it never stops dead and never jerks.

```html
<div class="ln-carry"><h2 id="my-line" class="line-text">Every call, logged and replayable</h2></div>
```

```js
function lineIn(sel, at, end) {
  const el = document.querySelector(sel);
  const carry = el.parentElement;
  tl.set(carry, { x: 0 }, 0);
  tl.to(carry, { x: -80, duration: end - at, ease: "none" }, at);          // steady glide
  tl.fromTo(el, { x: 56, opacity: 0, filter: "blur(8px)" },
    { x: 0, opacity: 1, filter: "blur(0px)", duration: 0.9, ease: "power3.out" }, at);  // soft arrival
}
```

- Carry: ~80 px over the line's life is ~0.5–1 px per frame: visible, calm.
- Read time: keep a line on screen about 0.3 s per word + 0.5 s, then leave (see `glitch-exit.md`).
- An end-card line can use the same arrival and keep its carry to the last frame.
- Do not scale text slowly (under ~4% per second): thin strokes shimmer. Move it for real or hold it.
