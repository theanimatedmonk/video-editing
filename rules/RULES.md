# Rules learned from corrections

Read before every edit. Add one whenever a note is given (format in `references/workflow/rules-from-corrections.md`).

- **Write audio automation as `{"version":1,"lanes":[...]}`** (export, 2026-10-13)
  Why: the unversioned `{"volume":[...]}` passed `hyperframes check`, then the export dropped all audio ("Unsupported automation version").
  Check: `grep data-automation` shows `"version":1`; `review_pack.sh` audio report is not near −91 dB.

- **Headlines in bold sans, not a serif** (type, 2026-10-13)
  Why: a serif (Instrument Serif) was tried and rejected; the bolder sans was "better".
  Check: headline `font-weight` 800, system sans or Inter.

- **Transitions glide, never snap** (transitions, 2026-10-13)
  Why: asked for "very smooth and cool" transitions.
  Check: every scene change uses the glide cut (`references/glide-cut.md`); both sides of each cut are moving.

- **Text arrives softly and keeps drifting; it glitches away when leaving** (motion, 2026-10-13)
  Why: fast slam-in arrivals felt "jarring".
  Check: no headline parks; exits use `references/glitch-exit.md`.

- **Illustrated characters must look finished** (illustration, 2026-10-13)
  Why: simple blob birds were rejected; shaded birds with tails, beaks, eyes and banking flight were accepted.
  Check: compare against `references/vector-songbirds.md`.

- **Duck the music under any featured sound** (audio, 2026-10-13)
  Why: chirps had to be heard over the bed.
  Check: music lane dips to about 0.15 for the effect's span.

- **Never trust transcript times for cut points** (cut, from the published workflow this skill follows)
  Why: rounded word times clip last syllables.
  Check: `scripts/edge_check.py` passes on every cut list.

- **Write the on-screen lines as one story before styling them** (copy, 2026-10-14)
  Why: the lines read as separate captions; the person asked for a cohesive story, a "?" on the hook question, and the hook broken into big rows.
  Check: read the lines alone, in order: hook question → answer → proof → turn → call to action that echoes the hook (`references/copywriting.md`).

- **Big type over a photo gets a soft shade behind it** (type, 2026-10-14)
  Why: amber text over a bright photo measured 2.5:1 contrast.
  Check: `hyperframes check` contrast passes (3:1 or better).

- **Promo music is calm and premium; fades are slow** (audio, 2026-10-14)
  Why: the upbeat electronic bed wasn't smooth enough; the person asked for smoother music.
  Check: ambient bed with soft pads; fade-in about 0.8 s, dips ramp over 0.35 s down and 0.7 s up, 2 s fade-out (`references/audio-rules.md`).
