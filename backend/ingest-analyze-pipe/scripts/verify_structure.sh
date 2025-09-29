#!/usr/bin/env bash
set -euo pipefail
echo "[verify] Checking key files..."
for f in README.md api/openapi.yaml schemas/song_map.schema.json services/packager/main.py; do
  [[ -f "$f" ]] && echo "  ok: $f" || { echo "  MISSING: $f"; exit 1; }
done
echo "[verify] OK"
