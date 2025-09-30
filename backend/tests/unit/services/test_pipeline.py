import json
import os
import subprocess
import sys
import wave
from io import BytesIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PIPE_ROOT = REPO_ROOT / "ingest-analyze-pipe"


def _create_demo_wav(dest: Path) -> None:
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
    dest.write_bytes(buf.getvalue())


def test_run_pipeline_generates_song_map(tmp_path: Path) -> None:
    raw_path = tmp_path / "raw.wav"
    partials_dir = tmp_path / "partials"
    final_dir = tmp_path / "final"
    stems_dir = tmp_path / "stems"

    _create_demo_wav(raw_path)

    cmd = [
        sys.executable,
        str(PIPE_ROOT / "scripts/run_pipeline.py"),
        "--id",
        "unit",
        "--raw",
        str(raw_path),
        "--partials",
        str(partials_dir),
        "--final",
        str(final_dir),
        "--stems",
        str(stems_dir),
        "--clean",
    ]
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(PIPE_ROOT), existing)))

    subprocess.run(cmd, check=True, env=env)

    output_path = final_dir / "unit.song_map.json"
    assert output_path.exists(), "pipeline should produce final song map"

    with output_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    assert payload["beats"], "beats should be populated"
    assert payload["chords"], "chords should be populated"
    assert payload["sections"], "sections should be populated"
    assert payload["lyrics"], "lyrics should be populated"
    assert payload["performance"]["melody"], "melody events should be populated"
    assert payload["performance"]["bass"], "bass events should be populated"
