#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
STUDIO="/Users/sajal.k/.hyperframes-studio"
DEST_ROOT="$ROOT/hyperframes"

RSYNC_EX=(
  --exclude='*.mp4'
  --exclude='*.mov'
  --exclude='.DS_Store'
  --exclude='.thumbnails'
  --exclude='.waveform-cache'
  --exclude='.hyperframes/requests'
  --exclude='.hyperframes/run-traces'
  --exclude='.hyperframes/live-runs'
  --exclude='.hyperframes/video-state-lock'
  --exclude='.hyperframes/backup'
  --exclude='.hyperframes/references'
)

commit() {
  local msg="$1"
  shift
  git add "$@"
  if git diff --cached --quiet; then
    echo "skip empty: $msg"
    return 0
  fi
  GIT_AUTHOR_NAME=animatedmonk \
  GIT_AUTHOR_EMAIL=isajalkumar247@gmail.com \
  GIT_COMMITTER_NAME=animatedmonk \
  GIT_COMMITTER_EMAIL=isajalkumar247@gmail.com \
  git commit -m "$msg"
}

sync_subset() {
  local src="$1"
  local dest="$2"
  shift 2
  mkdir -p "$dest"
  rsync -a "${RSYNC_EX[@]}" "$@" "$src/" "$dest/"
}

sync_media_use_audio_bundle() {
  local slug="$1"
  local src_name="$2"
  local src="$STUDIO/$src_name/.claude/skills/media-use"
  local dest="$DEST_ROOT/$slug/.claude/skills/media-use"
  mkdir -p "$dest"
  # Full media-use/audio (sfx + refs); matches studio copies of the skill.
  sync_subset "$src/audio" "$dest/audio"
}

sync_hyperframes_state() {
  local slug="$1"
  local src_name="$2"
  local src="$STUDIO/$src_name/.hyperframes"
  local dest="$DEST_ROOT/$slug/.hyperframes"
  sync_subset "$src" "$dest" \
    --include='/' \
    --include='.gitignore' \
    --include='video-state.json' \
    --include='hf-ids-stamped.json' \
    --include='history-id' \
    --include='agent-runs.jsonl' \
    --include='app-history.jsonl' \
    --include='blank-snapshot.json' \
    --include='moved-from.jsonl' \
    --include='artifacts/checks/***' \
    --exclude='*'
}

update_existing_project() {
  local slug="$1"
  local src_name="$2"
  local src="$STUDIO/$src_name"
  local dest="$DEST_ROOT/$slug"

  # 1 — composition + project metadata (+ optional lock / compositions)
  sync_subset "$src" "$dest" \
    --include='/' \
    --include='index.html' \
    --include='hyperframes.json' \
    --include='hyperframes.lock.json' \
    --include='meta.json' \
    --include='project.json' \
    --include='package.json' \
    --include='AGENTS.md' \
    --include='CLAUDE.md' \
    --include='compositions/***' \
    --exclude='*'
  commit "Sync hyperframes/$slug composition and project files" "hyperframes/$slug"

  sync_subset "$src/.claude/skills/hyperframes-core" "$dest/.claude/skills/hyperframes-core"
  commit "Sync hyperframes/$slug hyperframes-core skill" "hyperframes/$slug/.claude/skills/hyperframes-core"

  sync_subset "$src/.claude/skills/hyperframes-studio" "$dest/.claude/skills/hyperframes-studio"
  mkdir -p "$dest/.claude/skills/media-use"
  sync_subset "$src/.claude/skills/media-use" "$dest/.claude/skills/media-use" \
    --include='/' \
    --include='.gitignore' \
    --include='SKILL.md' \
    --include='references/***' \
    --include='luts/***' \
    --exclude='*'
  sync_media_use_audio_bundle "$slug" "$src_name"
  commit "Sync hyperframes/$slug studio and media-use skill" \
    "hyperframes/$slug/.claude/skills/hyperframes-studio" \
    "hyperframes/$slug/.claude/skills/media-use"

  sync_subset "$src/.claude/skills/media-use/scripts" "$dest/.claude/skills/media-use/scripts"
  sync_subset "$src/.claude/skills/media-use/audio/scripts" "$dest/.claude/skills/media-use/audio/scripts"
  commit "Sync hyperframes/$slug media-use scripts" \
    "hyperframes/$slug/.claude/skills/media-use/scripts" \
    "hyperframes/$slug/.claude/skills/media-use/audio/scripts"

  sync_subset "$src/assets" "$dest/assets"
  sync_subset "$src/renders" "$dest/renders" \
    --include='/' \
    --include='*.meta.json' \
    --exclude='*'
  sync_hyperframes_state "$slug" "$src_name"
  commit "Sync hyperframes/$slug assets, renders, and studio state" \
    "hyperframes/$slug/assets" \
    "hyperframes/$slug/renders" \
    "hyperframes/$slug/.hyperframes"

  # Artifact check JSON updates from the studio (commit skips if unchanged).
  rsync -a "${RSYNC_EX[@]}" "$src/.hyperframes/artifacts/checks/" "$dest/.hyperframes/artifacts/checks/" 2>/dev/null || true
  commit "Sync hyperframes/$slug artifact checks" "hyperframes/$slug/.hyperframes/artifacts/checks"
}

push_new_project() {
  local slug="$1"
  local src_name="$2"
  update_existing_project "$slug" "$src_name"
}

cd "$ROOT"

update_existing_project "Shihupalgarh" "Shihupalgarh"
update_existing_project "vikram-vetal" "vikram-vetal"
update_existing_project "vikram-vetal-chapter-1" "Vikram-vetal Chapter 1"
update_existing_project "Birdie" "Birdie"
update_existing_project "Birdie-hardware" "Birdie-hardware"

push_new_project "Pampa-lake" "Pampa-lake"
push_new_project "Untitled" "Untitled"
