/**
 * Chord Mapper Tests
 */

import { describe, it, expect } from 'vitest';
import {
  findChordForSyllable,
  calculateTimeOverlap,
  mapChordsToSyllables,
  findOverlappingChords,
  getChordMappingStats,
  BackendChord,
  BackendLyric
} from '../index';

describe('chord mapper utilities', () => {
  const chords: BackendChord[] = [
    { start: 0.0, end: 2.0, label: 'C:maj' },
    { start: 2.0, end: 4.0, label: 'F:maj' },
    { start: 4.0, end: 6.0, label: 'G:maj' }
  ];

  const syllables: BackendLyric[] = [
    { start: 0.5, end: 0.8, text: 'Hel' },
    { start: 0.8, end: 1.1, text: 'lo' },
    { start: 2.1, end: 2.4, text: 'world' }
  ];

  describe('findChordForSyllable', () => {
    it('finds chord with greatest overlap', () => {
      const syllable = { start: 0.5, end: 0.8, text: 'Hel' };
      const chord = findChordForSyllable(syllable, chords);
      expect(chord).toBe('C'); // Simplified from C:maj
    });

    it('returns undefined when no overlap', () => {
      const syllable = { start: 6.5, end: 6.8, text: 'test' };
      const chord = findChordForSyllable(syllable, chords);
      expect(chord).toBeUndefined();
    });

    it('returns undefined when overlap below threshold', () => {
      // Syllable at boundary with very small duration and high threshold
      const syllable = { start: 1.99, end: 2.0, text: 'test' }; // Duration: 0.01s
      const chord = findChordForSyllable(syllable, chords, 0.5); // Threshold: 50% of 0.01s = 0.005s
      // Overlap with C:maj is 0.01s which meets threshold, but F:maj starts at 2.0 (no overlap)
      // So it should find C:maj. Let's test with even higher threshold
      const result = findChordForSyllable(syllable, chords, 2.0); // Needs overlap > 0.02s (impossible)
      expect(result).toBeUndefined();
    });

    it('respects simplify parameter', () => {
      const syllable = { start: 0.5, end: 0.8, text: 'Hel' };
      const simplified = findChordForSyllable(syllable, chords, 0.1, true);
      const notSimplified = findChordForSyllable(syllable, chords, 0.1, false);

      expect(simplified).toBe('C');
      expect(notSimplified).toBe('C:maj');
    });

    it('handles empty chords array', () => {
      const syllable = { start: 0.5, end: 0.8, text: 'Hel' };
      const chord = findChordForSyllable(syllable, []);
      expect(chord).toBeUndefined();
    });

    it('chooses chord with greatest overlap when multiple', () => {
      const multiChords: BackendChord[] = [
        { start: 0.0, end: 0.6, label: 'C:maj' }, // 0.1s overlap
        { start: 0.5, end: 2.0, label: 'G:maj' }  // 0.3s overlap
      ];
      const syllable = { start: 0.5, end: 0.8, text: 'test' };
      const chord = findChordForSyllable(syllable, multiChords);
      expect(chord).toBe('G'); // Greater overlap
    });
  });

  describe('calculateTimeOverlap', () => {
    it('calculates overlap correctly', () => {
      const syllable = { start: 0.5, end: 0.8, text: 'test' };
      const chord = { start: 0.0, end: 2.0, label: 'C:maj' };
      const overlap = calculateTimeOverlap(syllable, chord);
      expect(overlap).toBeCloseTo(0.3, 10); // 0.8 - 0.5 (use toBeCloseTo for floating point)
    });

    it('returns 0 for no overlap', () => {
      const syllable = { start: 3.0, end: 3.5, text: 'test' };
      const chord = { start: 0.0, end: 2.0, label: 'C:maj' };
      const overlap = calculateTimeOverlap(syllable, chord);
      expect(overlap).toBe(0);
    });

    it('handles partial overlap', () => {
      const syllable = { start: 1.5, end: 2.5, text: 'test' };
      const chord = { start: 0.0, end: 2.0, label: 'C:maj' };
      const overlap = calculateTimeOverlap(syllable, chord);
      expect(overlap).toBe(0.5); // 2.0 - 1.5
    });

    it('handles complete syllable inside chord', () => {
      const syllable = { start: 0.5, end: 0.8, text: 'test' };
      const chord = { start: 0.0, end: 2.0, label: 'C:maj' };
      const overlap = calculateTimeOverlap(syllable, chord);
      expect(overlap).toBeCloseTo(0.3, 10); // Full syllable duration
    });

    it('handles complete chord inside syllable', () => {
      const syllable = { start: 0.0, end: 5.0, text: 'test' };
      const chord = { start: 1.0, end: 2.0, label: 'C:maj' };
      const overlap = calculateTimeOverlap(syllable, chord);
      expect(overlap).toBe(1.0); // Full chord duration
    });
  });

  describe('mapChordsToSyllables', () => {
    it('maps chords to all syllables', () => {
      const mapped = mapChordsToSyllables(syllables, chords);
      expect(mapped).toHaveLength(3);
      expect(mapped[0]).toBe('C'); // First syllable
      expect(mapped[1]).toBe('C'); // Second syllable
      expect(mapped[2]).toBe('F'); // Third syllable
    });

    it('handles syllables without chords', () => {
      const noChordSyllables = [
        { start: 10.0, end: 10.3, text: 'test' }
      ];
      const mapped = mapChordsToSyllables(noChordSyllables, chords);
      expect(mapped[0]).toBeUndefined();
    });
  });

  describe('findOverlappingChords', () => {
    it('finds all overlapping chords', () => {
      const overlapping = findOverlappingChords(1.0, 3.0, chords);
      expect(overlapping).toHaveLength(2); // C:maj and F:maj
    });

    it('returns empty array when no overlap', () => {
      const overlapping = findOverlappingChords(10.0, 11.0, chords);
      expect(overlapping).toHaveLength(0);
    });

    it('handles edge boundaries', () => {
      const overlapping = findOverlappingChords(2.0, 2.0, chords);
      expect(overlapping).toHaveLength(0); // Zero-width range
    });
  });

  describe('getChordMappingStats', () => {
    it('calculates mapping statistics', () => {
      const stats = getChordMappingStats(syllables, chords);

      expect(stats.totalSyllables).toBe(3);
      expect(stats.syllablesWithChords).toBe(3); // All have chords
      expect(stats.syllablesWithoutChords).toBe(0);
      expect(stats.coveragePercentage).toBe(100);
    });

    it('handles syllables without chords', () => {
      const mixedSyllables = [
        ...syllables,
        { start: 10.0, end: 10.3, text: 'nochor' }
      ];
      const stats = getChordMappingStats(mixedSyllables, chords);

      expect(stats.totalSyllables).toBe(4);
      expect(stats.syllablesWithChords).toBe(3);
      expect(stats.syllablesWithoutChords).toBe(1);
      expect(stats.coveragePercentage).toBe(75);
    });

    it('handles empty syllables array', () => {
      const stats = getChordMappingStats([], chords);
      expect(stats.coveragePercentage).toBe(0);
    });
  });
});
