#!/bin/sh
# Watch a video the way a reviewer would: frames sampled at FPS (default 2) tiled into
# contact sheets, the audio pulled out, and a shot list. Read the sheets in order.
#
#   sh watch.sh <video> <out-dir> [fps]
#
# Out: <out-dir>/sheet-001.jpg ...   (4x4 tiles, each stamped with its time)
#      <out-dir>/audio.wav            (16 kHz mono, ready for transcription)
#      <out-dir>/shots.json           (cut times and shot lengths, from shot_stats.py)
#      <out-dir>/manifest.txt         (what each sheet covers)
set -eu
VIDEO="$1"; OUT="$2"; FPS="${3:-2}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
# drawtext needs a real font file on macOS (no fontconfig); fall back to no timestamps
FONT=""
for f in /System/Library/Fonts/Supplemental/Arial.ttf /System/Library/Fonts/Helvetica.ttc /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf; do
  [ -f "$f" ] && FONT="$f" && break
done
STAMP=""
[ -n "$FONT" ] && STAMP="drawtext=fontfile=$FONT:text='%{pts\\:hms}':x=8:y=8:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6,"

DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO")
TILES=16
PER_SHEET=$(python3 -c "print(round($TILES / $FPS, 3))")

ffmpeg -v error -y -i "$VIDEO" \
  -vf "fps=$FPS,scale=480:-2,${STAMP}tile=4x4:padding=4:color=black" \
  -q:v 4 "$OUT/sheet-%03d.jpg"

ffmpeg -v error -y -i "$VIDEO" -vn -ac 1 -ar 16000 "$OUT/audio.wav" 2>/dev/null || echo "no audio track" > "$OUT/audio.txt"

python3 -I "$HERE/shot_stats.py" "$VIDEO" > "$OUT/shots.json"

{
  echo "video: $VIDEO"
  echo "duration: $DUR s, sampled at $FPS fps, $TILES frames per sheet ($PER_SHEET s each)"
  i=0
  for f in "$OUT"/sheet-*.jpg; do
    python3 -c "s=$i*$PER_SHEET; print('$(basename "$f")', f'{s:.1f}s - {s+$PER_SHEET:.1f}s')"
    i=$((i + 1))
  done
} > "$OUT/manifest.txt"
cat "$OUT/manifest.txt"
