import os, json, pathlib
from typing import Any, Dict

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)

def write_json(path: str, obj: Dict[str, Any]):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def partial_filename(job_id: str, stage: str) -> str:
    return f"{job_id}.{stage}.json"


def partial_path(out_dir: str, job_id: str, stage: str) -> pathlib.Path:
    return pathlib.Path(out_dir) / partial_filename(job_id, stage)


def write_partial(out_dir: str, job_id: str, stage: str, payload: Dict[str, Any]) -> pathlib.Path:
    path = partial_path(out_dir, job_id, stage)
    write_json(str(path), payload)
    return path


def read_partial(out_dir: str, job_id: str, stage: str) -> Dict[str, Any]:
    return read_json(str(partial_path(out_dir, job_id, stage)))
