#!/usr/bin/env bash
set -euo pipefail

# Bootstraps a local Python environment for the ingest-analyze pipeline.
# Creates .venv, installs service requirements, and verifies ffmpeg.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

log() { printf '>>> %s\n' "$1"; }
warn() { printf '!!! %s\n' "$1" >&2; }

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  warn "Python interpreter '${PYTHON_BIN}' not found. Set PYTHON_BIN to your python3 executable."
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  log "Creating virtual environment at ${VENV_DIR}";
  "$PYTHON_BIN" -m venv "$VENV_DIR"
else
  log "Using existing virtual environment at ${VENV_DIR}";
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

UPGRADE_FLAG=${UPGRADE_PIP:-true}
if [ "$UPGRADE_FLAG" = "true" ]; then
  if ! python -m pip install --upgrade pip setuptools wheel >/dev/null 2>&1; then
    warn "pip upgrade failed (are you offline?). Continuing with existing tooling."
  fi
fi

install_requirements() {
  local req_file="$1"
  if [ ! -f "$req_file" ]; then
    warn "Requirements file ${req_file} not found"
    return
  fi
  log "Installing $(basename "$req_file")"
  if ! python -m pip install -r "$req_file"; then
    warn "Failed to install packages from ${req_file}. Run manually once network access is available."
  fi
}

install_requirements "${ROOT_DIR}/services/packager/requirements.txt"

if ! command -v ffmpeg >/dev/null 2>&1; then
  warn "ffmpeg not detected. Install via 'brew install ffmpeg' (macOS) or 'apt-get install ffmpeg' (Debian/Ubuntu)."
else
  log "ffmpeg located at $(command -v ffmpeg)"
fi

log "Environment ready. Activate with 'source ${VENV_DIR}/bin/activate'."
