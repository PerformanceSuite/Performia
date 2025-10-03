"""Structure detection algorithm for song analysis."""
import numpy as np
import librosa
from typing import List, Dict, Optional
from difflib import SequenceMatcher


def detect_structure(
    audio_path: str,
    duration: float = 0.0,
    downbeats: Optional[List[float]] = None,
    chords: Optional[List[Dict]] = None,
    lyrics: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Detect song structure (intro, verse, chorus, bridge, outro).

    Args:
        audio_path: Path to audio file
        duration: Duration in seconds (if known)
        downbeats: List of downbeat timestamps
        chords: List of chord segments
        lyrics: List of lyric segments

    Returns:
        List of sections with start, end, label, confidence
    """
    # Load audio for novelty detection (at lower sample rate for speed)
    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    if duration == 0.0:
        duration = librosa.get_duration(y=y, sr=sr)

    # Fast path: if we have chord data, use it primarily
    if chords and len(chords) > 4:
        boundaries = extract_chord_boundaries(chords)
        if downbeats:
            boundaries = align_to_downbeats(np.array(boundaries), downbeats)
    else:
        # Step 1: Find major transitions using novelty detection
        boundaries = detect_novelty_boundaries(y, sr, downbeats)

    # Step 2: Find repeated sections (likely choruses) using self-similarity
    repetition_map = find_repeated_sections(y, sr, boundaries)

    # Step 3: Use lyrics to identify choruses if available
    if lyrics:
        lyric_repetitions = find_lyric_repetitions(lyrics, boundaries)
    else:
        lyric_repetitions = []

    # Step 4: Classify sections based on position and repetition
    sections = classify_sections(
        boundaries,
        duration,
        repetition_map,
        lyric_repetitions
    )

    return sections


def extract_chord_boundaries(chords: List[Dict]) -> List[float]:
    """Extract potential section boundaries from chord changes."""
    boundaries = [0.0]

    # Group consecutive similar chords
    i = 0
    while i < len(chords):
        current_chord = chords[i]["label"]
        section_start = chords[i]["start"]

        # Find end of similar chord sequence
        j = i
        while j < len(chords) and is_chord_similar(chords[j]["label"], current_chord):
            j += 1

        if j < len(chords):
            boundaries.append(chords[j]["start"])

        i = j if j > i else i + 1

    return sorted(set(boundaries))


def is_chord_similar(chord1: str, chord2: str) -> bool:
    """Check if two chords are similar (same root)."""
    # Extract root note (before ':')
    root1 = chord1.split(':')[0]
    root2 = chord2.split(':')[0]
    return root1 == root2


def detect_novelty_boundaries(
    y: np.ndarray,
    sr: int,
    downbeats: Optional[List[float]] = None
) -> List[float]:
    """
    Detect major transitions using spectral novelty.

    Args:
        y: Audio time series
        sr: Sample rate
        downbeats: List of downbeat timestamps

    Returns:
        List of boundary timestamps
    """
    # Use larger hop for faster processing
    hop_length = 4096  # ~0.19s per frame at 22050 Hz

    # Compute chroma features for harmonic novelty
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)

    # Compute self-similarity matrix (optimized)
    rec = librosa.segment.recurrence_matrix(
        chroma,
        mode='affinity',
        metric='cosine',
        self=True
    )

    # Detect boundaries using Laplacian segmentation
    boundaries_frames = librosa.segment.agglomerative(
        rec,
        k=min(8, len(chroma[0]) // 10)  # Adaptive based on song length
    )

    # Convert frame indices to time
    boundaries = librosa.frames_to_time(boundaries_frames, sr=sr, hop_length=hop_length)

    # Align to downbeats if available
    if downbeats:
        boundaries = align_to_downbeats(boundaries, downbeats)

    return sorted(set(boundaries))


def align_to_downbeats(boundaries: np.ndarray, downbeats: List[float]) -> List[float]:
    """
    Snap boundaries to nearest downbeats for musical alignment.

    Args:
        boundaries: Detected boundary timestamps
        downbeats: Downbeat timestamps

    Returns:
        Aligned boundary timestamps
    """
    aligned = []
    downbeat_array = np.array(downbeats)

    for boundary in boundaries:
        # Find nearest downbeat within 2 seconds
        diffs = np.abs(downbeat_array - boundary)
        min_idx = np.argmin(diffs)

        if diffs[min_idx] < 2.0:  # Within 2 seconds
            aligned.append(float(downbeat_array[min_idx]))
        else:
            aligned.append(float(boundary))

    return sorted(set(aligned))


def find_repeated_sections(
    y: np.ndarray,
    sr: int,
    boundaries: List[float]
) -> Dict[int, List[int]]:
    """
    Find repeated sections using self-similarity matrix.

    Args:
        y: Audio time series
        sr: Sample rate
        boundaries: Section boundaries

    Returns:
        Map of section index to list of similar section indices
    """
    # Use larger hop for faster processing
    hop_length = 4096

    # Compute MFCC features for timbral similarity (fewer coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=8, hop_length=hop_length)

    # Aggregate similarity by sections (compare section means)
    repetition_map = {}
    n_sections = len(boundaries)

    # Compute section feature means
    section_features = []
    for i in range(n_sections - 1):
        start_frame = librosa.time_to_frames(boundaries[i], sr=sr, hop_length=hop_length)
        end_frame = librosa.time_to_frames(boundaries[i + 1], sr=sr, hop_length=hop_length)

        # Mean MFCC for this section
        if end_frame > start_frame:
            section_mean = np.mean(mfcc[:, start_frame:end_frame], axis=1)
        else:
            section_mean = mfcc[:, start_frame]

        section_features.append(section_mean)

    # Compare sections
    for i in range(n_sections - 1):
        similar_sections = []

        for j in range(i + 1, n_sections - 1):
            # Cosine similarity between section means
            sim_score = np.dot(section_features[i], section_features[j]) / (
                np.linalg.norm(section_features[i]) * np.linalg.norm(section_features[j]) + 1e-10
            )

            if sim_score > 0.7:  # Similarity threshold
                similar_sections.append(j)

        if similar_sections:
            repetition_map[i] = similar_sections

    return repetition_map


def find_lyric_repetitions(
    lyrics: List[Dict],
    boundaries: List[float]
) -> List[int]:
    """
    Find sections with repeated lyrics (likely choruses).

    Args:
        lyrics: List of lyric segments
        boundaries: Section boundaries

    Returns:
        List of section indices with repeated lyrics
    """
    # Group lyrics by section
    section_lyrics = []
    n_sections = len(boundaries)

    for i in range(n_sections - 1):
        start = boundaries[i]
        end = boundaries[i + 1]

        section_text = " ".join([
            phrase["text"]
            for phrase in lyrics
            if phrase["start"] >= start and phrase["end"] <= end
        ]).lower().strip()

        section_lyrics.append(section_text)

    # Find repeated sections using text similarity
    repeated_indices = []

    for i in range(len(section_lyrics)):
        for j in range(i + 1, len(section_lyrics)):
            if len(section_lyrics[i]) > 10 and len(section_lyrics[j]) > 10:
                similarity = SequenceMatcher(
                    None,
                    section_lyrics[i],
                    section_lyrics[j]
                ).ratio()

                if similarity > 0.7:  # High text similarity
                    repeated_indices.extend([i, j])

    return list(set(repeated_indices))




def classify_sections(
    boundaries: List[float],
    duration: float,
    repetition_map: Dict[int, List[int]],
    lyric_repetitions: List[int]
) -> List[Dict]:
    """
    Classify sections as intro, verse, chorus, bridge, outro.

    Args:
        boundaries: Section boundaries
        duration: Total duration
        repetition_map: Map of repeated sections
        lyric_repetitions: Sections with repeated lyrics

    Returns:
        List of sections with labels and confidence
    """
    n_sections = len(boundaries)
    sections = []

    # Identify repeated sections (likely choruses)
    chorus_candidates = set()

    # Merge repetition sources
    for section_idx in repetition_map:
        chorus_candidates.add(section_idx)
        chorus_candidates.update(repetition_map[section_idx])

    chorus_candidates.update(lyric_repetitions)

    for i in range(n_sections - 1):
        start = boundaries[i]
        end = boundaries[i + 1] if i + 1 < n_sections else duration

        # Calculate section position ratio
        position_ratio = start / duration if duration > 0 else 0
        section_duration = end - start

        # Classification heuristics
        label = "verse"  # Default
        confidence = 0.7

        # First section heuristics
        if i == 0:
            if section_duration < 8.0:
                label = "intro"
                confidence = 0.85
            else:
                label = "verse"
                confidence = 0.75

        # Last section heuristics
        elif i == n_sections - 2:
            if section_duration < 8.0 and position_ratio > 0.85:
                label = "outro"
                confidence = 0.85
            elif i in chorus_candidates:
                label = "chorus"
                confidence = 0.90
            else:
                label = "verse"
                confidence = 0.70

        # Repeated sections are likely choruses
        elif i in chorus_candidates:
            label = "chorus"
            confidence = 0.90

        # Middle unique section might be bridge
        elif position_ratio > 0.5 and position_ratio < 0.7:
            if i not in chorus_candidates and section_duration < 16.0:
                label = "bridge"
                confidence = 0.65

        sections.append({
            "start": round(start, 3),
            "end": round(end, 3),
            "label": label,
            "confidence": round(confidence, 2)
        })

    return sections
