import os, pathlib, json
from typing import Optional

def gcs_url(bucket: str, *parts: str) -> str:
    path = "/".join(parts)
    return f"gs://{bucket}/{path}"

def ensure_dir(path: str):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def save_text(path: str, text: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
