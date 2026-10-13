# Vector songbirds (fly in arcs, bank, beat wings, chirp)

Three flat-shaded songbirds swoop around a subject (a mic held up to the camera), chirp with sound-wave marks synced to a chirp sound effect, then scatter outward as the shot moves on. A plain circular orbit with birds glued to the tangent looked like tumbling toys; what works is arcs over the top of the subject with a partial bank.

## Bird SVG (faces right, viewBox 160×110, ~176×121 px on screen)

Per bird: tail fan, far wing (darker, 55% opacity), gradient body, belly, head, cheek patch, two-part beak, eye with highlight, tucked feet, near wing with feather tips. Palettes that read well on photos:

| Bird | body (top→bottom) | belly | wing | head | beak |
|---|---|---|---|---|---|
| Roller teal | #6fe3d0 → #1f9e9a | #f2c38b | #2a8fc2 → #155e86 | #2fb3a6 | #2a2a33 |
| Golden oriole | #f5c26b → #e08a12 | #ffe2a6 | #3a3a46 → #1d1d24 | #f0a01d | #d9534f |
| Rosy starling | #f8dbe3 → #e79bb0 | #fff1f4 | #34343f → #1b1b22 | #1b1b22 | #f2b33d |

```html
<svg class="bird" viewBox="0 0 160 110">
  <defs>
    <linearGradient id="body-0" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fe3d0"/><stop offset="1" stop-color="#1f9e9a"/></linearGradient>
    <linearGradient id="wingfill-0" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a8fc2"/><stop offset="1" stop-color="#155e86"/></linearGradient>
  </defs>
  <path d="M46 60 L6 46 Q4 52 10 56 L4 62 Q6 68 12 66 L6 74 Q10 78 16 74 L48 70 Z" fill="url(#wingfill-0)"/>
  <g class="wing-far"><path d="M84 52 C78 30 62 16 44 14 C50 26 54 38 66 52 Z" fill="#155e86" opacity="0.55"/></g>
  <path d="M42 64 C42 44 66 34 94 38 C110 40 122 50 120 64 C118 80 96 90 72 88 C56 86 42 78 42 64 Z" fill="url(#body-0)"/>
  <path d="M58 76 C70 86 98 86 112 72 C108 84 92 90 74 89 C66 88 60 84 58 76 Z" fill="#f2c38b"/>
  <circle cx="116" cy="44" r="19" fill="#2fb3a6"/>
  <path d="M104 50 C108 58 118 60 126 54 C122 62 110 64 104 56 Z" fill="#f7d9a8" opacity="0.9"/>
  <path d="M132 38 L152 44 L133 47 Z" fill="#2a2a33"/>
  <path d="M133 47 L149 46 L134 51 Z" fill="#2a2a33" opacity="0.75"/>
  <circle cx="122" cy="40" r="4.6" fill="#0b0b10"/><circle cx="123.6" cy="38.6" r="1.6" fill="#fff"/>
  <path d="M80 87 L76 95 M88 87 L86 95" stroke="#2a2a33" stroke-width="3" stroke-linecap="round"/>
  <g class="wing">
    <path d="M86 52 C80 28 60 10 34 8 C38 14 36 18 40 22 C36 24 38 30 44 32 C40 36 44 42 50 42 C48 48 56 54 64 56 C72 60 82 58 86 52 Z" fill="url(#wingfill-0)"/>
    <path d="M80 50 C72 36 60 26 46 20 M78 54 C68 44 56 38 46 34" stroke="#fff" stroke-opacity="0.22" stroke-width="2" fill="none" stroke-linecap="round"/>
  </g>
</svg>
```

Give gradient ids a per-bird suffix. Add `filter: drop-shadow(0 6px 14px rgba(0,0,0,.55))` to the svg so it reads on busy photos.

## Rig: orbit → radius → bank (bird) and level (chirp marks)

```html
<div id="birds" style="position:absolute; left:960px; top:0">          <!-- centre on the subject -->
  <div class="orbit" id="orbit-0">                                      <!-- rotates around the centre -->
    <div class="rad" id="rad-0" style="left: 300px">                    <!-- radius; tween x to scatter -->
      <div class="rad" id="bank-0"><svg class="bird" id="bird-0">…</svg></div>
      <div class="rad" id="level-0"><svg class="chirp" id="chirp-0">…</svg></div>
    </div>
  </div>
</div>
```

All rig divs: `position:absolute; left:0; top:0; width:0; height:0`.

## Motion

```js
const ARCS = [[-205, 150], [-130, 125], [-80, 115]];   // [start angle, sweep] — spread so birds never stack
const RADII = [300, 320, 230];                          // keep the top of the arc clear of the headline
ARCS.forEach(([a0, span], i) => {
  const at = 1.05 + i * 0.12, dur = 1.5 - i * 0.12, a1 = a0 + span;
  const bank = (a) => -0.4 * a + 54;                     // heading = 0.6 × tangent: a gentle bank, not a tumble
  tl.fromTo("#bird-" + i, { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.5)" }, at);
  tl.fromTo("#orbit-" + i, { rotate: a0 }, { rotate: a1, duration: dur, ease: "power1.inOut" }, at);
  tl.fromTo("#bank-" + i, { rotate: bank(a0) }, { rotate: bank(a1), duration: dur, ease: "power1.inOut" }, at);
  tl.fromTo("#level-" + i, { rotate: -a0 }, { rotate: -a1, duration: dur, ease: "power1.inOut" }, at);   // chirps stay upright
  tl.fromTo("#bird-" + i + " .wing", { scaleY: 1, transformOrigin: "86px 52px" },
    { scaleY: -0.55, duration: 0.09, ease: "sine.inOut", yoyo: true, repeat: 15 }, at);
  tl.fromTo("#bird-" + i + " .wing-far", { scaleY: 1, transformOrigin: "84px 52px" },
    { scaleY: -0.4, duration: 0.09, ease: "sine.inOut", yoyo: true, repeat: 15 }, at + 0.03);   // a beat behind
  tl.to("#rad-" + i, { x: 900, duration: 0.45, ease: "power2.in" }, 2.2 + i * 0.05);           // scatter
  tl.to("#bird-" + i, { opacity: 0, duration: 0.3, ease: "power1.in" }, 2.32 + i * 0.05);
});
// chirp marks: three stroked arcs, popped in time with the sound
[[0, 1.12], [1, 1.32], [2, 1.55], [0, 1.78], [1, 2.0]].forEach(([i, t]) => {
  tl.fromTo("#chirp-" + i, { scale: 0.4, opacity: 0 }, { scale: 1.15, opacity: 1, duration: 0.14, ease: "power2.out", immediateRender: false }, t);
  tl.to("#chirp-" + i, { opacity: 0, scale: 1.4, duration: 0.2, ease: "power1.in" }, t + 0.14);
});
```

If the subject is zooming while the birds fly, tween the `#birds` container's `y` to follow the subject.

Sound: a chirp effect on its own `<audio>`, and duck the music under it (see `audio-rules.md`).
