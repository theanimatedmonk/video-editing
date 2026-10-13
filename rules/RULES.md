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
