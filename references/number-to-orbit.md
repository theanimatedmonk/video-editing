# Number → orbit ("a headline quantity expands into the ecosystem")

Mechanic taken from a launch-film moment and rebuilt fresh: a big number resolves left→right through a pixel front inside a hairline panel, holds, dissolves from both ends toward the centre while the panel narrows into a square, then upright tiles swirl in clockwise on a collapsing radius and keep orbiting a centre badge (where the brand mark is revealed) until they exit clockwise one by one.

Swap the slots: the number (`37 species`), a label plate, the tiles (product photos/logos), the badge content.

## Key structure

```html
<div class="m-rule" id="m-rule-top" style="top: 320px"></div>
<div class="m-rule" id="m-rule-bot" style="top: 760px"></div>
<div id="m-panel"></div>                                     <!-- 1500×440, fill clearly off the ground colour -->
<div id="m-count-wrap"><div id="m-count-box">
  <div id="m-count">37 species</div>                        <!-- clip-path: inset(0% 100% 0% 0%) to start -->
  <div class="m-band" id="m-band-r"></div><div class="m-band" id="m-band-a"></div><div class="m-band" id="m-band-b"></div>
</div></div>
<div id="m-plate">collected in your logbook</div>
<div id="m-badge"><div id="m-disc-out"></div><div id="m-disc-in"></div></div>
<div id="m-orbit">                                          <!-- at the frame centre -->
  <div class="m-spin"><div class="m-spin2">
    <!-- per tile i (8 tiles, 45° apart) -->
    <div class="m-arm" style="rotate: 45deg"><div class="m-radial" id="m-rad-1"><div class="m-up" style="rotate: -45deg">
      <div class="m-up2"><div class="m-up3"><div class="m-tile" id="m-tile-1"><img src="…"></div></div></div>
    </div></div></div>
  </div></div>
</div>
```

`m-spin`/`m-spin2` rotate the ring; `m-up2`/`m-up3` counter-rotate by the same amounts so tiles stay upright.

## Timeline (T = when the number starts)

```js
// pixel fronts: seeded squares in 48 px bands
let seed = 11;
const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
document.querySelectorAll(".m-band").forEach((band) => {
  for (let y = 0; y < 220; y += 14) for (let x = 0; x < 48; x += 14) {
    if (rnd() < 0.45) continue;
    const s = document.createElement("div"); s.className = "m-px";
    s.style.left = x + "px"; s.style.top = y + 6 + "px"; s.style.opacity = (0.35 + rnd() * 0.65).toFixed(2);
    band.appendChild(s);
  }
});
const W = document.getElementById("m-count").offsetWidth;

// panel opens slightly before the number so the frame is never empty
tl.fromTo("#m-panel", { opacity: 0, scaleX: 0.2 }, { opacity: 1, scaleX: 1, duration: 0.9, ease: "expo.out" }, T - 0.28);
tl.fromTo("#m-count-wrap", { scale: 0.55, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.75, ease: "power3.out" }, T + 0.05);
tl.fromTo("#m-count", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.7, ease: "power2.out" }, T + 0.05);
tl.fromTo("#m-band-r", { x: -24, opacity: 1 }, { x: W - 24, duration: 0.7, ease: "power2.out" }, T + 0.05);   // front rides the edge

// dissolve from both ends
const D = T + 1.25;
tl.to("#m-count", { clipPath: "inset(0% 50% 0% 50%)", duration: 0.45, ease: "power2.in" }, D);
tl.fromTo("#m-band-a", { x: -24, opacity: 1 }, { x: W / 2 - 24, duration: 0.45, ease: "power2.in" }, D);
tl.fromTo("#m-band-b", { x: W - 24, opacity: 1 }, { x: W / 2 - 24, duration: 0.45, ease: "power2.in" }, D);
tl.to("#m-panel", { scaleX: 0.36, scaleY: 1.2, duration: 0.55, ease: "power3.inOut" }, D + 0.05);

// tiles swirl in and orbit; a second spin layer accelerates the exit (never stops moving)
const O = D + 0.35;
tl.fromTo(".m-tile", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power1.out" }, O);
tl.fromTo(".m-radial", { x: 640 }, { x: 340, duration: 0.8, ease: "expo.out" }, O);
tl.fromTo(".m-spin", { rotate: -120 }, { rotate: 60, duration: 2.0, ease: "expo.out" }, O);
tl.fromTo(".m-up2", { rotate: 120 }, { rotate: -60, duration: 2.0, ease: "expo.out" }, O);
tl.fromTo(".m-spin2", { rotate: 0 }, { rotate: 150, duration: 1.5, ease: "power2.in" }, O + 1.5);
tl.fromTo(".m-up3", { rotate: 0 }, { rotate: -150, duration: 1.5, ease: "power2.in" }, O + 1.5);
tl.fromTo("#m-disc-out", { opacity: 0, scale: 0.45 }, { opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, O + 0.3);

// tiles leave clockwise, one after another — LINEAR radius so the radial speed dominates the orbit (no wobble)
const X = O + 2.05;
for (let i = 0; i < 8; i++) {
  const k = (i + 3) % 8;
  tl.to("#m-rad-" + k, { x: 1150, duration: 0.45, ease: "none" }, X + i * 0.05);
  tl.to("#m-tile-" + k, { opacity: 0, duration: 0.3, ease: "power1.in" }, X + 0.12 + i * 0.05);
}
```

Lessons: hide the number's wrapper (opacity 0) until it starts — a clip-path alone still counts as "on screen" text; a single radius tween (no in-then-out "breathe") avoids a tiny reversal that reads as jitter.
