# Copywriting for video: on-screen lines that tell one story

On-screen copy is read in about a second per line, with no sound, over moving pictures. Each line has to earn its place AND hand off to the next, so the lines read in order make one story.

## 1. Write the story before the lines

Fill this in first, in plain words:

| Beat | Job | Birdie example |
|---|---|---|
| Hook | the viewer's itch, as a question they have asked themselves | Who's singing outside your window? |
| Answer | the product's promise, as an action the viewer can take | Know any birdcall |
| Proof | a concrete number or result, shown, not claimed | 100+ species in your logbook |
| Turn | what life looks like after | Every call, logged and replayable |
| Call to action | one action, echoing the hook | Try Birdie at your window |

Read only the lines, in order, out loud. A stranger must get the pitch with no pictures. If a line could be swapped with another without breaking the flow, the story isn't cohesive yet.

## 2. Line craft

- **Questions end with "?"**: a hook question without it reads as a statement. Statements take no full stop on screen.
- **Six words or fewer per line**; one line on screen at a time.
- **Verbs the viewer does** ("Know", "Try", "Hear"), not features the product has ("AI-powered identification").
- **Concrete beats vague**: "100+ species" over "lots of birds"; "in your logbook" over "saved".
- **Callback**: the call to action repeats a word from the hook ("your window") so the film closes the loop.
- **Second person**: "your window", "your logbook". The viewer is the hero, the product is the tool.
- **No orphans**: never a lone "Meet" or "Introducing" on its own line.
- **Every claim is checked**: a number on screen must be true today (asset plan, stage 0).

## 3. Break a line for emphasis

A long hook reads better broken over rows at different sizes. The stressed word becomes its own row: biggest, in the accent colour.

```
Who's singing        <- 124 px, ink
outside              <- 210 px, accent (the surprising word)
your window?         <- 124 px, ink, ends the question
```

Break on meaning, not on width: each row should be a phrase you would pause after when speaking. Rows land one after another (about 0.25 s apart), the block glides as one, and all rows leave together (see `smooth-line-motion.md`, `glitch-exit.md`).

```html
<div class="ln-carry" id="hook-carry"><div id="hook-line">
  <div id="hk-1" class="hk-part line-text glitch" data-text="Who's singing">Who's singing</div>
  <div id="hk-2" class="hk-part line-text glitch" data-text="outside">outside</div>
  <div id="hk-3" class="hk-part line-text glitch" data-text="your window?">your window?</div>
</div></div>
```

```js
function stackLife(carrySel, rowSels, at, out, gap) {
  tl.set(carrySel, { x: 0 }, 0);
  tl.to(carrySel, { x: -80, duration: out + 0.5 - at, ease: "none" }, at);
  rowSels.forEach((sel, k) => {
    const el = document.querySelector(sel);
    tl.fromTo(el, { x: 56, opacity: 0, filter: "blur(8px)" },
      { x: 0, opacity: 1, filter: "blur(0px)", duration: 0.9, ease: "power3.out" }, at + k * gap);
    glitchOut(el, out + k * 0.04, sel);       // from glitch-exit.md
  });
}
stackLife("#hook-carry", ["#hk-1", "#hk-2", "#hk-3"], 0.3, 2.7, 0.25);
```

## 4. Big type over photos

Big words over a bright photo fail contrast (accent amber measured 2.5:1 on concrete). Put a soft shade behind the text block, not a box:

```css
#hook-scrim { position: absolute; inset: 0; opacity: 0;
  background: linear-gradient(90deg, rgba(7,8,13,.82) 0%, rgba(7,8,13,.6) 38%, rgba(7,8,13,0) 62%); }
```

Fade it in as the photo fills the frame and out when the photo leaves. Aim for 3:1 or better (`hyperframes check` measures it).

## 5. Before → after (from the Birdie film)

| Before | After | Why |
|---|---|---|
| Who's singing outside your window | Who's singing / **outside** / your window? | a question needs its "?"; rows add rhythm; the surprising word gets the size |
| Name any bird from one call | Know any birdcall | shorter, a verb the viewer does, one idea |
| 37 species / collected in your logbook | 100+ species / in your logbook | the bigger true number; the plate finishes the phrase instead of repeating it |
