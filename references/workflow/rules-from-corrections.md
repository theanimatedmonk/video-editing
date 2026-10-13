# Turn every correction into a rule

When the person gives a note ("the sound effects are too loud", "that bird looks cheap", "the export has no audio"), do two things:

1. Fix the video.
2. Add a rule to `rules/RULES.md` so the same note never has to be given twice.

## Rule format

```markdown
- **<short rule, imperative>** (<area>, <YYYY-MM-DD>)
  Why: <what went wrong, in one line>
  Check: <how to verify it next time: a command, a number, a thing to look at>
```

Areas: cut, audio, type, motion, transitions, illustration, export, review.

Good rules are specific and testable ("sound effects sit 4 dB under the music bed", not "effects should be subtle"). If a rule can be checked by a script, add the check to a script in `scripts/` and mention it in the rule.

Commit the rule with the skill so it travels to every project.
