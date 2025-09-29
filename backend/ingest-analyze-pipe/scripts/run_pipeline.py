#!/usr/bin/env python3
"""Run the stubbed ingest→analyze→package pipeline locally."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW = ROOT / "tmp" / "raw" / "demo.wav"
DEFAULT_PARTIALS = ROOT / "tmp" / "partials"
DEFAULT_FINAL = ROOT / "tmp" / "final"
DEFAULT_STEMS = ROOT / "tmp" / "stems"


def ensure_pythonpath(env: dict[str, str]) -> dict[str, str]:
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(ROOT), existing)))
    return env


def run_module(module: str, *module_args: str) -> None:
    env = ensure_pythonpath(os.environ.copy())
    cmd = [sys.executable, "-m", module, *module_args]
    subprocess.run(cmd, check=True, env=env)


def purge_for_job(job_id: str, partials_dir: Path, final_dir: Path) -> None:
    for shard in partials_dir.glob(f"{job_id}.*.json"):
        shard.unlink()
    final_path = final_dir / f"{job_id}.song_map.json"
    if final_path.exists():
        final_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local song-map pipeline")
    parser.add_argument("--id", default="demo", help="Job identifier")
    parser.add_argument("--raw", default=str(DEFAULT_RAW), help="Input WAV path")
    parser.add_argument("--partials", default=str(DEFAULT_PARTIALS), help="Directory for partial JSON outputs")
    parser.add_argument("--final", default=str(DEFAULT_FINAL), help="Directory for final Song Map outputs")
    parser.add_argument("--stems", default=str(DEFAULT_STEMS), help="Directory for separated stems")
    parser.add_argument("--clean", action="store_true", help="Remove existing outputs for the job before running")
    args = parser.parse_args()

    raw_path = Path(args.raw).expanduser().resolve()
    partials_dir = Path(args.partials).expanduser().resolve()
    final_dir = Path(args.final).expanduser().resolve()
    stems_dir = Path(args.stems).expanduser().resolve()

    partials_dir.mkdir(parents=True, exist_ok=True)
    final_dir.mkdir(parents=True, exist_ok=True)
    stems_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        purge_for_job(args.id, partials_dir, final_dir)

    run_module(
        "services.ingest.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.separation.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
        "--stems-dir",
        str(stems_dir),
    )
    run_module(
        "services.beats_key.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.chords.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.structure.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.asr.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.melody_bass.main",
        "--id",
        args.id,
        "--infile",
        str(raw_path),
        "--out",
        str(partials_dir),
    )
    run_module(
        "services.packager.main",
        "--id",
        args.id,
        "--raw",
        str(raw_path),
        "--partials",
        str(partials_dir),
        "--out",
        str(final_dir),
    )

    final_path = final_dir / f"{args.id}.song_map.json"
    print(f"Pipeline complete → {final_path}")


if __name__ == "__main__":
    main()
