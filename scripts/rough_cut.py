"""Rough cut: remove dead air from talking footage, keeping every word whole.

    python3 rough_cut.py <media> [--noise -35] [--min-silence 0.45] [--pad 0.12]
                         [--words transcript.json] [--word-tail 0.08] [--min-keep 0.3]

1. ffmpeg silencedetect finds pauses longer than --min-silence below --noise dB.
2. Everything else is kept, padded by --pad on both sides (breaths stay natural).
3. With --words (word timestamps, e.g. from `hyperframes transcribe --json`), any cut
   that would land inside a word, or less than --word-tail after it ends, is moved
   outside the word. This is the rule that stops clipped last words.

Prints JSON: the keep segments in source time, each with its place on the new timeline,
ready to become <video data-start / data-media-start / data-duration> clips.
Run edge_check.py on the result before building the edit.
"""
import json
import re
import subprocess
import sys


def opt(args, name, default, cast=float):
    if name in args:
        i = args.index(name)
        val = cast(args[i + 1])
        del args[i:i + 2]
        return val
    return default


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
    return float(out.strip())


def silences(path, noise, min_sil):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vn", "-af",
                          f"silencedetect=n={noise}dB:d={min_sil}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    out = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else None
        out.append((s, e))
    return out


def load_words(path):
    """Accepts a list of {text|word, start, end}, {"words": [...]}, or {"segments": [{"words": [...]}]}."""
    data = json.load(open(path))
    if isinstance(data, dict):
        if "words" in data:
            data = data["words"]
        elif "segments" in data:
            data = [w for seg in data["segments"] for w in seg.get("words", [])]
    words = []
    for w in data:
        if "start" in w and "end" in w:
            words.append((float(w["start"]), float(w["end"]), w.get("text") or w.get("word") or ""))
    return sorted(words)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    noise = opt(args, "--noise", -35.0)
    min_sil = opt(args, "--min-silence", 0.45)
    pad = opt(args, "--pad", 0.12)
    tail = opt(args, "--word-tail", 0.08)
    min_keep = opt(args, "--min-keep", 0.3)
    words_path = opt(args, "--words", None, str)
    media = args[0]
    dur = duration(media)

    keep, cursor = [], 0.0
    for s, e in silences(media, noise, min_sil):
        if s > cursor:
            keep.append([cursor, s])
        cursor = e if e is not None else dur
    if cursor < dur:
        keep.append([cursor, dur])

    keep = [[max(0.0, a - pad), min(dur, b + pad)] for a, b in keep]

    moved = []
    if words_path:
        words = load_words(words_path)
        for seg in keep:
            for ws, we, text in words:
                if ws < seg[1] < we + tail:          # the end would clip this word
                    moved.append({"word": text, "edge": "end", "from": round(seg[1], 3), "to": round(we + tail, 3)})
                    seg[1] = min(dur, we + tail)
                if ws - tail < seg[0] < we:          # the start would clip this word
                    moved.append({"word": text, "edge": "start", "from": round(seg[0], 3), "to": round(max(0.0, ws - tail), 3)})
                    seg[0] = max(0.0, ws - tail)

    merged = []
    for a, b in sorted(keep):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    merged = [s for s in merged if s[1] - s[0] >= min_keep]

    t, segments = 0.0, []
    for a, b in merged:
        segments.append({"source_in": round(a, 3), "source_out": round(b, 3),
                         "start": round(t, 3), "duration": round(b - a, 3)})
        t += b - a
    print(json.dumps({
        "media": media,
        "source_duration": round(dur, 3),
        "edited_duration": round(t, 3),
        "removed": round(dur - t, 3),
        "settings": {"noise_db": noise, "min_silence": min_sil, "pad": pad, "word_tail": tail},
        "edges_moved_to_keep_words_whole": moved,
        "segments": segments,
    }, indent=2))


if __name__ == "__main__":
    main()
