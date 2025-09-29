#!/usr/bin/env python3
import argparse
import json
import pathlib
from typing import Dict, List

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial

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

    section_defs = [
        ("intro", 0.0, 4.0),
        ("verse", 4.0, 12.0),
        ("chorus", 12.0, 20.0),
    ]
    sections: List[Dict[str, object]] = []
    for label, start, end in section_defs:
        sections.append({"start": start, "end": end, "label": label})
        if duration and end >= duration:
            break

    payload["sections"] = sections
    write_partial(args.out, args.id, "structure", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
