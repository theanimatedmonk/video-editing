# Text morph (one word becomes another)

Four ways to turn word A into word B in place, from softest to most literal. All seek-safe: tweens and seeded frame-stepped `tl.set` only. Uses `splitText()` from `text-transitions.md`.

## 1. Gooey blur morph (liquid letters)

The two words melt into each other: an SVG alpha-threshold filter turns overlapping blurs into a liquid blob, so letters look like they flow from one shape into the next. The most "morph-looking" of the four.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="goo-threshold">
    <feColorMatrix in="SourceGraphic" type="matrix"
      values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 255 -140" />
  </filter>
</svg>
<div class="morph" style="filter:url(#goo-threshold)">
  <span class="morph-a">listen</span>
  <span class="morph-b">learn</span>
</div>
```

```css
.morph { display: grid; place-items: center; }
.morph > span { grid-area: 1 / 1; } /* both words share one cell */
```

```js
function gooMorph(aSel, bSel, at, dur = 0.9) {
  // A blurs + fades out while B un-blurs + fades in over the same window; the threshold makes the overlap liquid
  tl.fromTo(aSel, { filter: "blur(0px)", opacity: 1 }, { filter: "blur(10px)", opacity: 0, duration: dur, ease: "power2.inOut" }, at);
  tl.fromTo(bSel, { filter: "blur(10px)", opacity: 0 }, { filter: "blur(0px)", opacity: 1, duration: dur, ease: "power2.inOut" }, at);
}
```

- Text must be one solid colour; the threshold kills gradients and anti-aliasing (edges get a little crisp — that is the look).
- Nothing else may be inside `.morph` (the filter would goo it too). The background stays outside.
- Chain several: A→B at t, B→C at t+1.4, each pair as its own two tweens.

## 2. Scramble morph (decode A into B)

Letters of A churn through random glyphs and land on B, left to right. Same mechanism as the scramble entry, but it starts from a real word.

```js
function scrambleMorph(sel, to, at, { dur = 0.8, fps = 30, glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%&*+=?" } = {}) {
  const el = document.querySelector(sel);
  const from = el.textContent;
  const len = Math.max(from.length, to.length);
  let seed = 0;
  for (const ch of from + to) seed = (seed * 31 + ch.charCodeAt(0)) % 2147483647;
  seed = seed || 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const frames = Math.round(dur * fps);
  for (let f = 0; f <= frames; f++) {
    const p = f / frames;
    const churnStart = p * 1.4 * len;           // letters start churning left to right...
    const settled = Math.floor((p - 0.3) / 0.7 * len); // ...and settle a little behind
    let s = "";
    for (let i = 0; i < len; i++) {
      if (i < settled) s += to[i] ?? "";
      else if (i < churnStart) s += glyphs[Math.floor(rnd() * glyphs.length)];
      else s += from[i] ?? "";
    }
    tl.set(el, { textContent: s }, at + f / fps);
  }
}
```

Fix the element width (or use tabular glyphs) so the line does not twitch while the length changes.

## 3. Letter roll (departure-board swap)

Every letter slot rolls up: the old letter leaves through the top, the new one rises from below, staggered left to right. Readable, mechanical, satisfying on numbers and short words.

```js
function letterRoll(containerSel, from, to, at, { each = 0.035, dur = 0.45 } = {}) {
  const box = document.querySelector(containerSel);
  box.setAttribute("aria-label", to);
  box.textContent = "";
  const len = Math.max(from.length, to.length);
  const outs = [], ins = [];
  for (let i = 0; i < len; i++) {
    const slot = document.createElement("span");
    slot.className = "roll-slot";
    slot.innerHTML = `<span class="roll-a">${from[i] ?? " "}</span><span class="roll-b">${to[i] ?? " "}</span>`;
    box.appendChild(slot);
    outs.push(slot.children[0]); ins.push(slot.children[1]);
  }
  tl.fromTo(outs, { yPercent: 0 }, { yPercent: -110, duration: dur, ease: "power3.in", stagger: each }, at);
  tl.fromTo(ins, { yPercent: 110 }, { yPercent: 0, duration: dur, ease: "power3.out", stagger: each }, at + dur * 0.55);
}
```

```css
.roll-slot { display: inline-grid; overflow: hidden; white-space: pre; }
.roll-slot > span { grid-area: 1 / 1; }
```

Letters that are the same in A and B can skip the roll (filter them out before tweening) so only the changed ones move.

## 4. Shared-letter rearrange (FLIP anagram)

Letters that exist in both words slide to their new places; the rest fade/blur out and in. Best for anagrams and near-words (listen → silent, Birdie → Bird ID).

```js
// build inside document.fonts.ready, before registering the timeline
function rearrange(stageSel, from, to, at, dur = 0.9) {
  const stage = document.querySelector(stageSel); // position: relative
  const lay = (word) => {                          // lay out a word invisibly, read each letter's x
    const row = document.createElement("div");
    row.className = "re-row"; row.style.visibility = "hidden";
    const spans = Array.from(word).map((ch) => { const s = document.createElement("span"); s.textContent = ch; row.appendChild(s); return s; });
    stage.appendChild(row);
    const base = row.getBoundingClientRect().left;
    const xs = spans.map((s) => s.getBoundingClientRect().left - base);
    row.remove();
    return xs;
  };
  const xa = lay(from), xb = lay(to);
  const used = new Set();
  const letters = Array.from(from).map((ch, i) => {
    const j = Array.from(to).findIndex((c, k) => c.toLowerCase() === ch.toLowerCase() && !used.has(k));
    if (j >= 0) used.add(j);
    const s = document.createElement("span");
    s.className = "re-letter"; s.textContent = ch;
    stage.appendChild(s);
    tl.set(s, { x: xa[i] }, 0);
    if (j >= 0) tl.to(s, { x: xb[j], duration: dur, ease: "power3.inOut" }, at + i * 0.02);
    else tl.to(s, { opacity: 0, filter: "blur(8px)", y: -20, duration: dur * 0.5, ease: "power2.in" }, at);
    return { s, j, ch };
  });
  Array.from(to).forEach((ch, k) => {               // letters only in B fade in at their spot
    if (used.has(k)) return;
    const s = document.createElement("span");
    s.className = "re-letter"; s.textContent = ch;
    stage.appendChild(s);
    tl.fromTo(s, { x: xb[k], opacity: 0, filter: "blur(8px)", y: 20 },
      { opacity: 1, filter: "blur(0px)", y: 0, duration: dur * 0.5, ease: "power2.out" }, at + dur * 0.5);
  });
  // matched letters whose case differs: swap the glyph at the midpoint
  letters.forEach(({ s, j, ch }) => { if (j >= 0 && to[j] !== ch) tl.set(s, { textContent: to[j] }, at + dur / 2); });
}
```

```css
.re-row, .re-letter { position: absolute; left: 0; top: 0; white-space: pre; font: inherit; }
```

- Centre the stage yourself: offset the stage by half the difference in word widths, or tween the stage `x` alongside.
- A letter that crosses others reads better with a small arc: add a second tween on a wrapper for `y` (one property per wrapper).

## Picking one

| Feel | Use |
|---|---|
| dreamy, organic, brand reveal | 1 gooey blur |
| tech, AI, decoding | 2 scramble morph |
| stats, prices, short labels | 3 letter roll |
| clever wordplay, anagram, shared letters | 4 rearrange |

For shapes rather than letters (icon → logo, outline text → logo), use GSAP's MorphSVGPlugin (free since GSAP 3.13) on SVG paths: `tl.to("#iconPath", { morphSVG: "#logoPath", duration: 0.9, ease: "power2.inOut" }, at)`. Convert text to outlines first; load the plugin from the same GSAP version as the core.
