#!/usr/bin/env python3
import argparse, os, json, pathlib, time, sys
from typing import Dict, Any, Tuple, List
import jsonschema

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial

# Load schema at module level
SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../../schemas/song_map.schema.json'
)

with open(SCHEMA_PATH) as f:
    SONG_MAP_SCHEMA = json.load(f)

def validate_song_map(song_map: dict) -> Tuple[bool, List[str]]:
    """Validate Song Map against schema.

    Returns:
        (is_valid, error_messages)
    """
    try:
        jsonschema.validate(song_map, SONG_MAP_SCHEMA)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [e.message]
    except jsonschema.SchemaError as e:
        return False, [f"Schema error: {e.message}"]

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
    ap.add_argument("--infile", help="Path to original audio file for duration (optional)")
    ap.add_argument("--out", required=True, help="Output folder")
    args = ap.parse_args()

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    # Infer partials directory from output directory and job ID
    partials_dir = pathlib.Path(args.out) / args.id

    song_map = build_minimal_song_map(args.id, args.infile)

    # Merge any existing partials (drop-in JSONs named <id>.<stage>.json)
    if partials_dir.exists():
        for shard in partials_dir.glob(f"{args.id}.*.json"):
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

    # Validate song map before writing
    is_valid, errors = validate_song_map(song_map)
    if not is_valid:
        print(f"ERROR: Invalid Song Map: {'; '.join(errors)}", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.join(args.out, f"{args.id}.song_map.json")
    with open(out_path, 'w') as f:
        json.dump(song_map, f, indent=2)
    print(json.dumps(song_map))

if __name__ == "__main__":
    main()
