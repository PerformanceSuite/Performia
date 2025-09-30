#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
import numpy as np
import librosa
from typing import Dict, List, Optional, Tuple

from services.common.audio import guess_duration_sec
from services.common.utils import write_partial


def hz_to_midi(frequency: float) -> int:
    """
    Convert frequency in Hz to MIDI note number.

    Args:
        frequency: Frequency in Hz

    Returns:
        MIDI note number (rounded to nearest integer)
    """
    if frequency <= 0:
        return 0
    midi_float = 69 + 12 * np.log2(frequency / 440.0)
    return int(np.round(midi_float))


def extract_pitch_track(audio_path: pathlib.Path, sr: int = 22050,
                       fmin: float = 65.0, fmax: float = 2093.0,
                       hop_length: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract pitch track from audio file using librosa's pyin algorithm.

    Args:
        audio_path: Path to audio file
        sr: Sample rate
        fmin: Minimum frequency to track (Hz)
        fmax: Maximum frequency to track (Hz)
        hop_length: Hop length for analysis (larger = faster but less precise)

    Returns:
        Tuple of (f0, voiced_probs) arrays
    """
    # Load audio at lower sample rate for faster processing
    y, _ = librosa.load(audio_path, sr=sr)

    # Use pyin for pitch tracking with optimized parameters
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        sr=sr,
        fmin=fmin,
        fmax=fmax,
        frame_length=2048,
        hop_length=hop_length,  # Larger hop = faster processing
        fill_na=0.0
    )

    return f0, voiced_probs


def segment_notes(f0: np.ndarray, voiced_probs: np.ndarray, hop_length: int = 512,
                 sr: int = 22050, min_duration: float = 0.1,
                 confidence_threshold: float = 0.5) -> List[Dict[str, float]]:
    """
    Segment continuous pitch track into discrete notes.

    Args:
        f0: Fundamental frequency array
        voiced_probs: Voice probability array
        hop_length: Hop length used in pyin
        sr: Sample rate
        min_duration: Minimum note duration in seconds
        confidence_threshold: Minimum confidence to consider a note

    Returns:
        List of note dictionaries with start, duration, midi, confidence
    """
    notes = []
    frame_duration = hop_length / sr

    # Find voiced regions with sufficient confidence
    voiced_mask = (voiced_probs >= confidence_threshold) & (f0 > 0)

    if not np.any(voiced_mask):
        return notes

    # Find contiguous voiced segments
    voiced_diff = np.diff(np.concatenate(([0], voiced_mask.astype(int), [0])))
    starts = np.where(voiced_diff == 1)[0]
    ends = np.where(voiced_diff == -1)[0]

    for start_idx, end_idx in zip(starts, ends):
        # Extract segment
        segment_f0 = f0[start_idx:end_idx]
        segment_probs = voiced_probs[start_idx:end_idx]

        # Calculate duration
        duration = (end_idx - start_idx) * frame_duration

        # Skip very short notes
        if duration < min_duration:
            continue

        # Get median frequency (more robust than mean)
        valid_f0 = segment_f0[segment_f0 > 0]
        if len(valid_f0) == 0:
            continue

        median_freq = np.median(valid_f0)
        midi_note = hz_to_midi(median_freq)

        # Average confidence
        avg_confidence = float(np.mean(segment_probs))

        # Calculate start time
        start_time = start_idx * frame_duration

        notes.append({
            "time": round(start_time, 3),
            "midi": midi_note,
            "velocity": int(80 + avg_confidence * 30),  # Scale velocity by confidence
            "duration": round(duration, 3),
            "confidence": round(avg_confidence, 3)
        })

    return notes


def smooth_and_merge_notes(notes: List[Dict[str, float]],
                           max_gap: float = 0.15,
                           semitone_threshold: int = 2) -> List[Dict[str, float]]:
    """
    Smooth note transitions and merge similar consecutive notes.

    Args:
        notes: List of note dictionaries
        max_gap: Maximum gap between notes to merge (seconds)
        semitone_threshold: Maximum semitone difference to merge notes

    Returns:
        Smoothed list of notes
    """
    if len(notes) <= 1:
        return notes

    smoothed = [notes[0].copy()]

    for note in notes[1:]:
        prev_note = smoothed[-1]
        prev_end = prev_note["time"] + prev_note.get("duration", 0)

        gap = note["time"] - prev_end
        midi_diff = abs(note["midi"] - prev_note["midi"])

        # Merge if notes are close in time and pitch
        if gap <= max_gap and midi_diff <= semitone_threshold:
            # Extend previous note
            new_duration = note["time"] + note.get("duration", 0) - prev_note["time"]
            prev_note["duration"] = round(new_duration, 3)

            # Average MIDI if different (quantize to semitone)
            if midi_diff > 0:
                avg_midi = (prev_note["midi"] + note["midi"]) / 2
                prev_note["midi"] = int(np.round(avg_midi))

            # Average confidence and velocity
            prev_conf = prev_note.get("confidence", 0.8)
            note_conf = note.get("confidence", 0.8)
            prev_note["confidence"] = round((prev_conf + note_conf) / 2, 3)
            prev_note["velocity"] = int(80 + prev_note["confidence"] * 30)
        else:
            smoothed.append(note.copy())

    return smoothed


def extract_melody_and_bass(audio_path: pathlib.Path,
                            stems_dir: Optional[pathlib.Path] = None) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract melody and bass tracks from audio file.

    Args:
        audio_path: Path to main audio file
        stems_dir: Optional directory containing separated stems

    Returns:
        Tuple of (melody_notes, bass_notes)
    """
    melody_notes = []
    bass_notes = []

    # Optimized parameters for speed
    sr = 16000  # Lower sample rate (was 22050)
    hop_length = 512  # ~32ms at 16000 Hz

    # Try to use stems if available
    vocal_stem = None
    bass_stem = None

    if stems_dir and stems_dir.exists():
        potential_vocal = stems_dir / "vocals.wav"
        potential_bass = stems_dir / "bass.wav"

        if potential_vocal.exists():
            vocal_stem = potential_vocal
        if potential_bass.exists():
            bass_stem = potential_bass

    # Extract melody from vocals or full mix
    if vocal_stem:
        print(f"Extracting melody from vocal stem: {vocal_stem}", file=sys.stderr)
        f0, voiced_probs = extract_pitch_track(
            vocal_stem,
            sr=sr,
            fmin=librosa.note_to_hz('C3'),  # C3 = 130.81 Hz
            fmax=librosa.note_to_hz('C6'),   # C6 = 1046.50 Hz
            hop_length=hop_length
        )
    else:
        print("Extracting melody from full mix (no vocal stem)", file=sys.stderr)
        f0, voiced_probs = extract_pitch_track(
            audio_path,
            sr=sr,
            fmin=librosa.note_to_hz('C3'),
            fmax=librosa.note_to_hz('C6'),
            hop_length=hop_length
        )

    melody_notes = segment_notes(f0, voiced_probs, hop_length=hop_length, sr=sr,
                                 min_duration=0.1, confidence_threshold=0.5)
    melody_notes = smooth_and_merge_notes(melody_notes, max_gap=0.2, semitone_threshold=2)

    # Extract bass from bass stem or full mix
    if bass_stem:
        print(f"Extracting bass from bass stem: {bass_stem}", file=sys.stderr)
        f0_bass, voiced_probs_bass = extract_pitch_track(
            bass_stem,
            sr=sr,
            fmin=librosa.note_to_hz('E1'),  # E1 = 41.20 Hz
            fmax=librosa.note_to_hz('E3'),   # E3 = 164.81 Hz
            hop_length=hop_length
        )
    else:
        print("Extracting bass from full mix (no bass stem)", file=sys.stderr)
        f0_bass, voiced_probs_bass = extract_pitch_track(
            audio_path,
            sr=sr,
            fmin=librosa.note_to_hz('E1'),
            fmax=librosa.note_to_hz('E3'),
            hop_length=hop_length
        )

    bass_notes = segment_notes(f0_bass, voiced_probs_bass, hop_length=hop_length, sr=sr,
                               min_duration=0.15, confidence_threshold=0.4)
    bass_notes = smooth_and_merge_notes(bass_notes, max_gap=0.25, semitone_threshold=1)

    return melody_notes, bass_notes


def main():
    parser = argparse.ArgumentParser(description="Melody & Bass Extraction Service")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", help="Input file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--partials", help="Partials folder (for reading separation stems)")
    args = parser.parse_args()

    payload: Dict[str, object] = {"id": args.id, "service": "melody_bass"}

    duration = 0.0
    melody: List[Dict[str, object]] = []
    bass: List[Dict[str, object]] = []

    if args.infile:
        src = pathlib.Path(args.infile).expanduser().resolve()
        payload["source_path"] = str(src)
        duration = guess_duration_sec(src)

        # Check for separation stems
        stems_dir = None
        if args.partials:
            partials_path = pathlib.Path(args.partials).expanduser().resolve()
            separation_file = partials_path / f"{args.id}.separation.json"

            if separation_file.exists():
                with open(separation_file, 'r') as f:
                    separation_data = json.load(f)
                    if "stems" in separation_data and "vocals" in separation_data["stems"]:
                        # Get stems directory from vocals path
                        vocals_path = pathlib.Path(separation_data["stems"]["vocals"])
                        stems_dir = vocals_path.parent
                        print(f"Found stems directory: {stems_dir}", file=sys.stderr)

        # Extract melody and bass
        print(f"Processing audio file: {src}", file=sys.stderr)
        import time
        start_time = time.time()

        melody, bass = extract_melody_and_bass(src, stems_dir)

        elapsed = time.time() - start_time
        print(f"Extraction completed in {elapsed:.2f} seconds", file=sys.stderr)
        print(f"Extracted {len(melody)} melody notes and {len(bass)} bass notes", file=sys.stderr)

    payload["performance"] = {"melody": melody, "bass": bass}
    payload["duration_sec"] = duration

    write_partial(args.out, args.id, "melody_bass", payload)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
