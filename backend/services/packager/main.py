#!/usr/bin/env python3
import argparse, os, json, pathlib, time
from typing import Dict, Any

from services.common.audio import guess_duration_sec
from services.common.utils import write_json

def build_minimal_song_map(job_id: str, raw_path: str) -> Dict[str, Any]:
    dur = guess_duration_sec(raw_path) if raw_path and os.path.exists(raw_path) else 0.0
    return {
        "id": job_id,
        "duration_sec": dur,
        "meter": {"numerator": 4, "denominator": 4},
        "tempo": {"bpm_global": 120.0, "curve": [[0.0, 120.0]], "confidence": 0.5},
        "beats": [],
        "downbeats": [],
        "key": [],
        "chords": [],
        "sections": [],
        "lyrics": [],
        "performance": {"melody": [], "bass": []},
        "provenance": {
            "separation": "pending",
            "asr": "pending",
            "harmony": "pending",
            "git_sha": "dev",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    }

def main():
    ap = argparse.ArgumentParser(description="Packager - merge partials into canonical Song Map")
    ap.add_argument("--id", required=True, help="Job ID (e.g., yt_xxx)")
    ap.add_argument("--partials", default="tmp/partials", help="Folder with per-stage JSON shards")
    ap.add_argument("--raw", help="Path to raw WAV for duration (optional)")
    ap.add_argument("--out", default="tmp/final", help="Output folder")
    args = ap.parse_args()

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    song_map = build_minimal_song_map(args.id, args.raw)

    # Merge any existing partials (drop-in JSONs named <id>.<stage>.json)
    parts_dir = pathlib.Path(args.partials)
    if parts_dir.exists():
        for shard in parts_dir.glob(f"{args.id}.*.json"):
            try:
                with open(shard, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Trivial merge: append known keys if present
                for k in ("beats","downbeats","key","chords","sections","lyrics"):
                    if k in data and isinstance(data[k], list):
                        song_map[k].extend(data[k])
                if "tempo" in data and isinstance(data["tempo"], dict):
                    song_map["tempo"].update(data["tempo"])
                if "performance" in data and isinstance(data["performance"], dict):
                    perf = song_map.setdefault("performance", {"melody": [], "bass": []})
                    for field in ("melody", "bass"):
                        if field in data["performance"] and isinstance(data["performance"][field], list):
                            perf.setdefault(field, [])
                            perf[field].extend(data["performance"][field])
                if "duration_sec" in data and isinstance(data["duration_sec"], (int, float)):
                    song_map["duration_sec"] = max(song_map["duration_sec"], data["duration_sec"])
            except Exception as e:
                print(f"[warn] failed to merge {shard}: {e}")

    out_path = os.path.join(args.out, f"{args.id}.song_map.json")
    write_json(out_path, song_map)
    print(f"[packager] wrote {out_path}")

if __name__ == "__main__":
    main()
