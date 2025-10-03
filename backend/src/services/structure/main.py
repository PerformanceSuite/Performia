#!/usr/bin/env python3
import argparse
import json
import pathlib
import logging
from typing import Dict, List

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial
from services.structure.structure_detection import detect_structure

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Structure")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "structure"}

    duration = 0.0
    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload["source_path"] = str(src)
        duration = guess_duration_sec(src)

        try:
            logging.info(f"Analyzing structure for {src}...")

            # Try to load partial data from other services if available
            partials_dir = pathlib.Path(args.out)
            beats_data = load_partial(partials_dir, args.id, "beats_key")
            chord_data = load_partial(partials_dir, args.id, "chords")
            asr_data = load_partial(partials_dir, args.id, "asr")

            sections = detect_structure(
                str(src),
                duration=duration,
                downbeats=beats_data.get("downbeats") if beats_data else None,
                chords=chord_data.get("chords") if chord_data else None,
                lyrics=asr_data.get("lyrics") if asr_data else None
            )

            logging.info(f"Detected {len(sections)} sections")
            payload["sections"] = sections

        except Exception as e:
            logging.error(f"Structure detection failed: {e}")
            # Fallback to simple stub data
            section_defs = [
                ("intro", 0.0, 4.0),
                ("verse", 4.0, 12.0),
                ("chorus", 12.0, 20.0),
            ]
            sections: List[Dict[str, object]] = []
            for label, start, end in section_defs:
                sections.append({
                    "start": start,
                    "end": end,
                    "label": label,
                    "confidence": 0.5
                })
                if duration and end >= duration:
                    break
            payload["sections"] = sections

    write_partial(args.out, args.id, "structure", payload)
    print(json.dumps(payload))

def load_partial(partials_dir: pathlib.Path, job_id: str, service_name: str) -> Dict:
    """Load partial data from another service if it exists."""
    partial_path = partials_dir / f"{job_id}.{service_name}.json"
    if partial_path.exists():
        try:
            with open(partial_path, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

if __name__ == "__main__":
    main()
