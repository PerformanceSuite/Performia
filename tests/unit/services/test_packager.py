import json
import os
import subprocess
import sys
import wave
from io import BytesIO
from pathlib import Path

import pytest

PIPE_ROOT = Path(__file__).resolve().parents[3] / "ingest-analyze-pipe"
if str(PIPE_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPE_ROOT))

from services.packager.main import build_minimal_song_map  # noqa: E402


def _make_demo_wav(tmp_path: Path) -> Path:
    sample_rate = 44100
    duration_sec = 1
    frames = int(sample_rate * duration_sec)
    buf = BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for _ in range(frames):
            wav.writeframesraw((0).to_bytes(2, "little", signed=True))
        wav.writeframes(b"")
    wav_path = tmp_path / "demo.wav"
    wav_path.write_bytes(buf.getvalue())
    return wav_path


def test_build_minimal_song_map_returns_expected_keys(tmp_path: Path):
    wav_path = _make_demo_wav(tmp_path)
    song_map = build_minimal_song_map("unit_test", str(wav_path))

    assert song_map["id"] == "unit_test"
    assert song_map["meter"] == {"numerator": 4, "denominator": 4}
    assert "tempo" in song_map and "bpm_global" in song_map["tempo"]
    assert "provenance" in song_map and song_map["provenance"]["separation"] == "pending"


def test_packager_cli_emits_schema_compliant_json(tmp_path: Path):
    wav_path = _make_demo_wav(tmp_path)
    out_dir = tmp_path / "final"
    partials_dir = tmp_path / "partials"
    partials_dir.mkdir()

    partial_payload = {
        "chords": [
            {"start": 0.0, "end": 1.0, "label": "C:maj", "conf": 0.8}
        ]
    }
    (partials_dir / "cli_test.chords.json").write_text(json.dumps(partial_payload))

    cmd = [
        sys.executable,
        "-m",
        "services.packager.main",
        "--id",
        "cli_test",
        "--raw",
        str(wav_path),
        "--out",
        str(out_dir),
        "--partials",
        str(partials_dir),
    ]
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(PIPE_ROOT), existing]))

    subprocess.run(cmd, check=True, env=env)

    output_path = out_dir / "cli_test.song_map.json"
    assert output_path.exists()

    payload = json.loads(output_path.read_text())

    try:
        import jsonschema  # type: ignore

        schema = json.loads((PIPE_ROOT / "schemas/song_map.schema.json").read_text())
        jsonschema.validate(payload, schema)
    except ModuleNotFoundError:
        pytest.skip("jsonschema not installed: run scripts/bootstrap_env.sh first")

    assert payload["chords"], "expected chords partial to be merged"
