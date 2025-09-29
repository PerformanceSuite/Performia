#!/usr/bin/env python3
import argparse
import json
import pathlib
import shutil
from typing import Dict

from services.common.utils import write_partial

def main():
    parser = argparse.ArgumentParser(description="Separation")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--stems-dir", default="tmp/stems", help="Destination for separated stems")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "separation"}
    stems_root = pathlib.Path(args.stems_dir).expanduser().resolve()
    stems_dir = stems_root / args.id
    stems_dir.mkdir(parents=True, exist_ok=True)

    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        stems = {}
        for stem in ("mix", "vocals", "drums", "bass", "other"):
            stem_path = stems_dir / f"{stem}.wav"
            shutil.copyfile(src, stem_path)
            stems[stem] = str(stem_path)
        payload["stems"] = stems
        payload["source_path"] = str(src)
    write_partial(args.out, args.id, "separation", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
