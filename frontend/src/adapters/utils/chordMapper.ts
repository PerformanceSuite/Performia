/**
 * Chord mapping utilities for Song Map adapter.
 *
 * Maps chords to syllables based on time overlap.
 */

import { BackendChord, BackendLyric } from '../types';
import { simplifyChordLabel } from './chordSimplifier';

/**
 * Default minimum overlap percentage for chord attachment.
 */
export const DEFAULT_CHORD_OVERLAP_THRESHOLD = 0.1; // 10%

/**
 * Find the best matching chord for a syllable based on time overlap.
 *
 * Selects the chord with the greatest time overlap with the syllable.
 * Only attaches chord if overlap exceeds the threshold.
 *
 * @param syllable - Syllable/lyric to find chord for
 * @param chords - Array of all chords
 * @param overlapThreshold - Minimum overlap as fraction of syllable duration (default: 0.1)
 * @param simplify - Whether to simplify chord label (default: true)
 * @returns Chord label or undefined if no significant overlap
 */
export function findChordForSyllable(
  syllable: BackendLyric,
  chords: BackendChord[],
  overlapThreshold: number = DEFAULT_CHORD_OVERLAP_THRESHOLD,
  simplify: boolean = true
): string | undefined {
  if (!chords || chords.length === 0) {
    return undefined;
  }

  let bestChord: BackendChord | null = null;
  let maxOverlap = 0;

  // Find chord with greatest overlap
  for (const chord of chords) {
    const overlap = calculateTimeOverlap(syllable, chord);

    if (overlap > maxOverlap) {
      maxOverlap = overlap;
      bestChord = chord;
    }
  }

  // Check if overlap meets threshold
  const syllableDuration = syllable.end - syllable.start;
  const minOverlap = syllableDuration * overlapThreshold;

  if (bestChord && maxOverlap >= minOverlap) {
    const label = bestChord.label;
    return simplify ? simplifyChordLabel(label) : label;
  }

  return undefined;
}

/**
 * Calculate time overlap between a syllable and a chord.
 *
 * @param syllable - Syllable with start/end times
 * @param chord - Chord with start/end times
 * @returns Overlap duration in seconds
 */
export function calculateTimeOverlap(
  syllable: BackendLyric,
  chord: BackendChord
): number {
  const overlapStart = Math.max(syllable.start, chord.start);
  const overlapEnd = Math.min(syllable.end, chord.end);
  return Math.max(0, overlapEnd - overlapStart);
}

/**
 * Map chords to multiple syllables in batch.
 *
 * More efficient than calling findChordForSyllable repeatedly.
 *
 * @param syllables - Array of syllables
 * @param chords - Array of chords
 * @param overlapThreshold - Minimum overlap threshold
 * @param simplify - Whether to simplify chord labels
 * @returns Array of chord labels (undefined if no match)
 */
export function mapChordsToSyllables(
  syllables: BackendLyric[],
  chords: BackendChord[],
  overlapThreshold: number = DEFAULT_CHORD_OVERLAP_THRESHOLD,
  simplify: boolean = true
): (string | undefined)[] {
  return syllables.map(syllable =>
    findChordForSyllable(syllable, chords, overlapThreshold, simplify)
  );
}

/**
 * Find all chords that overlap with a time range.
 * Useful for debugging or advanced chord analysis.
 *
 * @param startTime - Start of time range
 * @param endTime - End of time range
 * @param chords - Array of all chords
 * @returns Array of overlapping chords
 */
export function findOverlappingChords(
  startTime: number,
  endTime: number,
  chords: BackendChord[]
): BackendChord[] {
  return chords.filter(chord => {
    const overlapStart = Math.max(startTime, chord.start);
    const overlapEnd = Math.min(endTime, chord.end);
    return overlapEnd > overlapStart;
  });
}

/**
 * Calculate statistics about chord mapping.
 *
 * @param syllables - Array of syllables
 * @param chords - Array of chords
 * @param overlapThreshold - Minimum overlap threshold
 * @returns Statistics object
 */
export function getChordMappingStats(
  syllables: BackendLyric[],
  chords: BackendChord[],
  overlapThreshold: number = DEFAULT_CHORD_OVERLAP_THRESHOLD
): {
  totalSyllables: number;
  syllablesWithChords: number;
  syllablesWithoutChords: number;
  coveragePercentage: number;
} {
  const totalSyllables = syllables.length;
  let syllablesWithChords = 0;

  for (const syllable of syllables) {
    const chord = findChordForSyllable(syllable, chords, overlapThreshold, false);
    if (chord !== undefined) {
      syllablesWithChords++;
    }
  }

  const syllablesWithoutChords = totalSyllables - syllablesWithChords;
  const coveragePercentage = totalSyllables > 0
    ? (syllablesWithChords / totalSyllables) * 100
    : 0;

  return {
    totalSyllables,
    syllablesWithChords,
    syllablesWithoutChords,
    coveragePercentage
  };
}
