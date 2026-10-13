"""Shot list and pacing numbers for a video, from ffmpeg scene detection.

    python3 shot_stats.py <video> [--threshold 0.3]

Prints JSON: duration, cut times, shot lengths, cuts per minute, mean and median shot length.
Use it on a reference video to learn its pacing, and on your own render to compare.
"""
import json
import re
import statistics
import subprocess
import sys


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout
    return float(out.strip())


def cuts(path, threshold):
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-an", "-vf",
                           f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
                          capture_output=True, text=True)
    return [round(float(t), 3) for t in re.findall(r"pts_time:([0-9.]+)", proc.stderr)]


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    threshold = 0.3
    if "--threshold" in args:
        i = args.index("--threshold")
        threshold = float(args[i + 1])
        del args[i:i + 2]
    path = args[0]
    dur = duration(path)
    times = cuts(path, threshold)
    bounds = [0.0] + times + [dur]
    shots = [round(b - a, 3) for a, b in zip(bounds, bounds[1:]) if b - a > 0.01]
    print(json.dumps({
        "video": path,
        "duration": round(dur, 3),
        "threshold": threshold,
        "cuts": times,
        "shots": len(shots),
        "cuts_per_minute": round(len(times) / dur * 60, 2) if dur else 0,
        "mean_shot": round(statistics.mean(shots), 3) if shots else 0,
        "median_shot": round(statistics.median(shots), 3) if shots else 0,
        "shot_lengths": shots,
    }, indent=2))


if __name__ == "__main__":
    main()
