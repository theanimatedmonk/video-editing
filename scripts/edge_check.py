"""Edge check: listen to every cut, not the transcript.

    python3 edge_check.py <media> <cuts.json> [--window 0.06] [--loud -38]

For each kept segment, measures the audio just OUTSIDE each edge (the part being thrown
away). If that sliver is loud, the cut is chopping sound: usually the first or last
syllable of a word. Transcripts round word times, so only the audio can prove a clean cut.

cuts.json: rough_cut.py output, or {"segments": [{"source_in": s, "source_out": e}, ...]}.
Prints each suspicious edge with a suggested fix and exits 1 if any are found.
"""
import json
import re
import subprocess
import sys


def opt(args, name, default):
    if name in args:
        i = args.index(name)
        val = float(args[i + 1])
        del args[i:i + 2]
        return val
    return default


def mean_db(path, start, length):
    if length <= 0.005:
        return -91.0
    err = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{max(0.0, start):.3f}", "-t", f"{length:.3f}",
                          "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[0-9.]+|-inf) dB", err)
    return -91.0 if not m or m.group(1) == "-inf" else float(m.group(1))


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    window = opt(args, "--window", 0.06)
    loud = opt(args, "--loud", -38.0)
    media, cuts_path = args[0], args[1]
    segs = json.load(open(cuts_path))["segments"]
    problems = []
    for i, s in enumerate(segs):
        a, b = s["source_in"], s["source_out"]
        before = mean_db(media, a - window, window) if a > 0 else -91.0
        after = mean_db(media, b, window)
        if i > 0 and before > loud:
            problems.append(f"segment {i} start {a:.3f}s: {before:.1f} dB right before the cut -> move start earlier (~{a - window:.3f}s)")
        if after > loud:
            problems.append(f"segment {i} end {b:.3f}s: {after:.1f} dB right after the cut -> move end later (~{b + window:.3f}s)")
    print(f"{len(segs)} segments, {2 * len(segs)} edges checked, window {window}s, loud above {loud} dB")
    for p in problems:
        print("  CLIPPED  " + p)
    print("PASS: every edge lands in quiet" if not problems else f"FAIL: {len(problems)} edge(s) cut into sound")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
