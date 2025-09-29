#!/usr/bin/env bash
set -euo pipefail

JOB_ID=${JOB_ID:-demo}
RAW_PATH=${1:-tmp/raw/demo.wav}
PARTIALS_DIR=${PARTIALS_DIR:-tmp/partials}
FINAL_DIR=${FINAL_DIR:-tmp/final}

"$(dirname "$0")/run_pipeline.py" --id "$JOB_ID" --raw "$RAW_PATH" --partials "$PARTIALS_DIR" --final "$FINAL_DIR" --clean
FINAL_PATH="${FINAL_DIR}/${JOB_ID}.song_map.json"
echo "Final Song Map:"
if command -v jq >/dev/null 2>&1; then
  jq . "$FINAL_PATH"
else
  cat "$FINAL_PATH"
fi
