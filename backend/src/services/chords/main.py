#!/usr/bin/env python3
import argparse
import json
import pathlib
from typing import Dict, List

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial

def main():
    parser = argparse.ArgumentParser(description="Chords")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "chords"}

    duration = 0.0
    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload["source_path"] = str(src)
        duration = guess_duration_sec(src)

    segment_length = 2.0
    chord_labels = ["C:maj", "F:maj", "G:maj", "C:maj"]
    chords: List[Dict[str, object]] = []
    current = 0.0
    for label in chord_labels:
        end_time = current + segment_length
        chords.append(
            {
                "start": current,
                "end": end_time,
                "label": label,
                "conf": 0.6,
            }
        )
        current = end_time
        if duration and current >= duration:
            break

    payload["chords"] = chords
    write_partial(args.out, args.id, "chords", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
