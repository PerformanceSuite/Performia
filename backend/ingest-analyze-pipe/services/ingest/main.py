#!/usr/bin/env python3
import argparse
import json
import pathlib
from typing import Optional

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial

def main():
    parser = argparse.ArgumentParser(description="Ingest")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    payload = {"id": args.id, "service": "ingest"}
    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload.update(
            {
                "source_path": str(src),
                "raw_path": str(src),
                "duration_sec": guess_duration_sec(src),
            }
        )
    write_partial(args.out, args.id, "ingest", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
