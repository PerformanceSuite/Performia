#!/usr/bin/env python3
import argparse
import json
import pathlib
import logging
from typing import Dict, List

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial
from services.asr.whisper_service import get_whisper_service

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="ASR")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "asr"}

    duration = 0.0
    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload["source_path"] = str(src)
        duration = guess_duration_sec(src)

    phrases: List[Dict[str, object]] = []

    if args.infile:
        try:
            logging.info(f"Transcribing {src} with Whisper...")
            whisper_service = get_whisper_service(model_size="base")
            phrases = whisper_service.transcribe_to_phrases(str(src))
            logging.info(f"Transcribed {len(phrases)} phrases")
        except Exception as e:
            logging.error(f"ASR failed: {e}")
            # Fallback to stub data for testing
            words = ["la", "di", "da"]
            time_cursor = 0.0
            for word in words:
                end_time = time_cursor + 0.75
                phrases.append({"start": time_cursor, "end": end_time, "text": word})
                time_cursor = end_time + 0.25

    if duration and phrases:
        phrases[-1]["end"] = min(duration, phrases[-1]["end"])

    payload["lyrics"] = phrases
    write_partial(args.out, args.id, "asr", payload)
    print(json.dumps(payload))

if __name__ == "__main__":
    main()
