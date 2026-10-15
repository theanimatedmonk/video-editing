# Text transitions (entries, exits, line-to-line swaps)

The widely used text moves, written to be seek-safe in HyperFrames: everything is one tween per property on the root (or scene) timeline, no `Math.random`, no CSS `transform` on anything GSAP moves. Pair with `smooth-line-motion.md` (the line keeps drifting while these play) and `glitch-exit.md` / `glitch-effects.md` for the leave.

## Shared helper: split text into spans (once, at build time)

```js
// by: "chars" | "words". Keeps spaces as real spaces so wrapping still works.
function splitText(el, by = "chars") {
  const text = el.textContent;
  el.setAttribute("aria-label", text);
  el.textContent = "";
  const parts = by === "words" ? text.split(/(\s+)/) : Array.from(text);
  return parts.map((p) => {
    if (/^\s+$/.test(p)) { el.appendChild(document.createTextNode(p)); return null; }
    const s = document.createElement("span");
    s.className = by === "words" ? "w" : "c";
    s.setAttribute("aria-hidden", "true");
    s.textContent = p;
    el.appendChild(s);
    return s;
  }).filter(Boolean);
}
```

```css
.c, .w { display: inline-block; will-change: transform, filter, opacity; }
.mask-row { display: block; overflow: hidden; padding-bottom: 0.08em; } /* descenders stay inside the mask */
```

Fonts change glyph widths, so split and measure inside `document.fonts.ready.then(...)` and register `window.__timelines[id] = tl` only at the end of that callback.

## 1. Soft blur-in per letter (the default entry)

Calm, premium. Letters sharpen from left to right while the whole line glides.

```js
const chars = splitText(document.querySelector("#title"), "chars");
tl.fromTo(chars,
  { opacity: 0, filter: "blur(12px)", y: 18 },
  { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.7, ease: "power3.out", stagger: 0.025 },
  at);
```

Exit = same thing mirrored with `power2.in`, stagger `0.015`, `filter: blur(10px)`, `y: -12`. Keep total stagger under ~0.4 s or long lines feel slow.

## 2. Mask slide-up (rows rise out of an invisible floor)

The editorial / Apple-keynote move. Each row sits in an `overflow:hidden` wrapper; the text inside rises from below.

```html
<h1 class="headline"><span class="mask-row"><span class="row">Every bird</span></span><span class="mask-row"><span class="row">has a name</span></span></h1>
```

```js
tl.fromTo(".headline .row", { yPercent: 110 }, { yPercent: 0, duration: 0.8, ease: "expo.out", stagger: 0.09 }, at);
// leave: rows drop through the top
tl.to(".headline .row", { yPercent: -110, duration: 0.45, ease: "power3.in", stagger: 0.05 }, out);
```

Per-word version: wrap each word in its own `.mask-row` with `display:inline-block`.

## 3. Word cascade (waterfall)

Words drop in one after another already moving, like they were thrown onto the line. Good for punchy hooks.

```js
const words = splitText(document.querySelector("#hook"), "words");
tl.fromTo(words,
  { yPercent: -120, opacity: 0, rotate: -4 },
  { yPercent: 0, opacity: 1, rotate: 0, duration: 0.55, ease: "back.out(1.6)", stagger: 0.07 },
  at);
```

## 4. Scramble / decode

Random glyphs settle into the real letters left to right. Tech, AI, "unlocking" moments. Frame-stepped `tl.set` with a seeded generator, so a scrub to any frame shows the same glyphs.

```js
function scrambleIn(sel, at, { dur = 0.9, fps = 30, glyphs = "!<>-_\\/[]{}=+*^?#ABCDEFGHJKLMNPQRSTUVWXYZ0123456789" } = {}) {
  const el = document.querySelector(sel);
  const final = el.textContent;
  let seed = 0;
  for (const ch of sel + final) seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647;
  seed = seed || 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const frames = Math.round(dur * fps);
  for (let f = 0; f <= frames; f++) {
    const settled = Math.floor((f / frames) * final.length); // letters left of this are final
    let s = "";
    for (let i = 0; i < final.length; i++) {
      if (final[i] === " " || i < settled) s += final[i];
      else s += glyphs[Math.floor(rnd() * glyphs.length)];
    }
    tl.set(el, { textContent: s }, at + f / fps);
  }
}
```

Use a monospace or tabular font (or `font-variant-numeric: tabular-nums` for numbers) so the line width does not jitter while glyphs change. For proportional fonts, fix the element's `width` to the final text's measured width.

## 5. Typewriter with caret

```js
function typeOn(sel, at, cps = 22) {
  const el = document.querySelector(sel);
  const text = el.textContent;
  el.textContent = "";
  for (let i = 1; i <= text.length; i++) tl.set(el, { textContent: text.slice(0, i) }, at + i / cps);
  return at + text.length / cps; // when typing ends
}
```

```css
.typed::after { content: ""; display: inline-block; width: 0.08em; height: 0.9em; margin-left: 0.06em; background: currentColor; vertical-align: -0.08em; }
```

Blink the caret with a finite stepped tween on a CSS variable (`--caret` → `opacity: var(--caret)` on `::after`), `repeat` a fixed count, `ease: "steps(1)"`. Never an infinite CSS animation.

## 6. Line-to-line swap at peak speed (text match cut)

Old line accelerates out, new line arrives already moving the same direction; the swap happens at the fastest moment so the eye reads one move. Blur peaks exactly at the cut.

```js
function textSwap(oldSel, newSel, cut, dist = 160) {
  tl.to(oldSel, { y: -dist, opacity: 0, filter: "blur(10px)", duration: 0.32, ease: "power4.in" }, cut - 0.32);
  tl.fromTo(newSel, { y: dist, opacity: 0, filter: "blur(10px)" },
    { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.42, ease: "power4.out" }, cut);
}
```

Horizontal version = the glide cut (`glide-cut.md`) applied to text only.

## 7. Per-letter slot roll (exit or swap)

Each letter flips up out of its slot one after another, like a departure board. Wrap each `.c` in an `overflow:hidden` inline-block, then:

```js
tl.to(chars, { yPercent: -110, duration: 0.35, ease: "power3.in", stagger: { each: 0.02, from: "start" } }, out);
```

For a swap between two words, see `text-morph.md` (letter roll).

## Picking one

| Feel | Use |
|---|---|
| calm, premium, default | 1 blur-in, leave with glitch exit |
| editorial headline | 2 mask slide-up |
| loud hook | 3 word cascade |
| tech / AI / reveal | 4 scramble |
| chat, prompt, code | 5 typewriter |
| consecutive lines in one scene | 6 swap at peak speed |

## Gotchas

- Do not blur every letter of a long paragraph: many `filter` layers render slowly. Blur the line wrapper instead and stagger only opacity / y.
- `stagger` with `from: "center"` or `"random"` is deterministic in GSAP (random stagger is seeded per tween), but prefer explicit order for repeatable renders across GSAP versions.
- Keep the entry ease `out` and the exit ease `in`; an `inOut` entry looks like it hesitates.
