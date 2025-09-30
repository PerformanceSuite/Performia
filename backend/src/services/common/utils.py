"""Common utility functions for services."""
import json
from pathlib import Path
from typing import Dict


def write_partial(output_dir: str, job_id: str, service_name: str, payload: Dict) -> None:
    """
    Write service output to partial file.

    Args:
        output_dir: Output directory path
        job_id: Job identifier
        service_name: Name of service
        payload: Data to write
    """
    out_path = Path(output_dir) / f"{job_id}_{service_name}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, 'w') as f:
        json.dump(payload, f, indent=2)
