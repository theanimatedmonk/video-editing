#!/bin/sh
# Build the review pack for a finished render: frames from every section as contact
# sheets, plus an audio report. Hand the pack to a DIFFERENT model than the one that
# edited (see references/workflow/review-gate.md).
#
#   sh review_pack.sh <render.mp4> <out-dir> [seconds-between-frames]
#
# Out: <out-dir>/review-001.jpg ...  (3x3 tiles, time-stamped)
#      <out-dir>/audio-report.txt    (loudness, true peak, silence check)
set -eu
VIDEO="$1"; OUT="$2"; EVERY="${3:-1}"
mkdir -p "$OUT"
# drawtext needs a real font file on macOS (no fontconfig); fall back to no timestamps
FONT=""
for f in /System/Library/Fonts/Supplemental/Arial.ttf /System/Library/Fonts/Helvetica.ttc /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf; do
  [ -f "$f" ] && FONT="$f" && break
done
STAMP=""
[ -n "$FONT" ] && STAMP="drawtext=fontfile=$FONT:text='%{pts\\:hms}':x=8:y=8:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6,"

ffmpeg -v error -y -i "$VIDEO" \
  -vf "fps=1/$EVERY,scale=640:-2,${STAMP}tile=3x3:padding=4:color=black" \
  -q:v 3 "$OUT/review-%03d.jpg"

{
  echo "render: $VIDEO"
  ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact "$VIDEO"
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$VIDEO" | grep -q .; then
    ffmpeg -hide_banner -i "$VIDEO" -vn -af ebur128=peak=true -f null - 2>&1 \
      | sed -n '/Summary:/,$p' | grep -E "I:|LRA:|Peak:" | sed 's/^ */  /'
    MEAN=$(ffmpeg -hide_banner -i "$VIDEO" -vn -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: \(.*\) dB/\1/p')
    echo "  mean volume: $MEAN dB"
    case "$MEAN" in
      -9[0-9]*|-inf) echo "  WARNING: the audio track is silent (the mix failed or nothing was placed)";;
    esac
    echo "  targets: social/web about -14 LUFS integrated, true peak at or below -1 dBTP"
  else
    echo "  WARNING: no audio track in the render"
  fi
} > "$OUT/audio-report.txt"
cat "$OUT/audio-report.txt"
ls "$OUT"/review-*.jpg | wc -l | xargs echo "review sheets:"
