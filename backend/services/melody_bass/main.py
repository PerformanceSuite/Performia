#!/usr/bin/env python3
import argparse
import json
import pathlib
from typing import Dict, List

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial

def main():
    parser = argparse.ArgumentParser(description="Melody & Bass")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "melody_bass"}

    duration = 0.0
    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload["source_path"] = str(src)
        duration = guess_duration_sec(src)

    melody: List[Dict[str, object]] = []
    bass: List[Dict[str, object]] = []
    for idx, midi_note in enumerate((60, 62, 64, 65)):
        melody.append({"time": idx * 0.5, "midi": midi_note, "velocity": 90})
    for idx, midi_note in enumerate((36, 36, 38, 40)):
        bass.append({"time": idx * 1.0, "midi": midi_note, "velocity": 80})

    payload["performance"] = {"melody": melody, "bass": bass}
    payload["duration_sec"] = duration

    write_partial(args.out, args.id, "melody_bass", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
