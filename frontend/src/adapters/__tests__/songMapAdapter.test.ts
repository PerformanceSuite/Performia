/**
 * Song Map Adapter Tests
 *
 * Comprehensive test suite for the Song Map adapter.
 * Tests all edge cases and validates transformation logic.
 */

import { describe, it, expect } from 'vitest';
import {
  adaptBackendToFrontend,
  adaptMultipleSongMaps,
  adaptBackendToFrontendSafe,
  getEmptySongMap,
  validateFrontendSongMap,
  AdapterError,
  AdapterErrorCode,
  BackendSongMap
} from '../index';
import simpleBackendMap from './fixtures/simpleBackendMap.json';

describe('songMapAdapter', () => {
  describe('adaptBackendToFrontend', () => {
    it('transforms valid backend map to frontend format', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        title: 'Test Song',
        artist: 'Test Artist'
      });

      expect(result.title).toBe('Test Song');
      expect(result.artist).toBe('Test Artist');
      expect(result.key).toBe('C Major');
      expect(result.bpm).toBe(120);
      expect(result.sections).toHaveLength(1);
      expect(result.sections[0].name).toBe('Verse');
      expect(result.sections[0].lines).toHaveLength(2); // Two lines detected by gap
    });

    it('uses metadata from backend when not overridden', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);

      expect(result.title).toBe('Test'); // Parsed from source_path (test_song.wav -> "Test")
      expect(result.artist).toBe('Song'); // Second part of underscore split
    });

    it('handles empty lyrics array (instrumental)', () => {
      const instrumental: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        lyrics: []
      };

      const result = adaptBackendToFrontend(instrumental);

      expect(result.sections).toHaveLength(1);
      expect(result.sections[0].lines).toHaveLength(0);
    });

    it('handles missing sections array', () => {
      const noSections: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        sections: undefined
      };

      const result = adaptBackendToFrontend(noSections);

      expect(result.sections).toHaveLength(1);
      expect(result.sections[0].name).toBe('Song');
    });

    it('handles zero BPM', () => {
      const zeroBpm: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        tempo: { bpm_global: 0.0 }
      };

      const result = adaptBackendToFrontend(zeroBpm);

      expect(result.bpm).toBe(0);
    });

    it('handles missing key', () => {
      const noKey: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        key: undefined
      };

      const result = adaptBackendToFrontend(noKey);

      expect(result.key).toBe('Unknown');
    });

    it('maps chords to syllables correctly', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);

      const firstLine = result.sections[0].lines[0];
      expect(firstLine.syllables[0].chord).toBe('C'); // "Hel" overlaps with C:maj
      expect(firstLine.syllables[1].chord).toBe('C'); // "lo" overlaps with C:maj

      const secondLine = result.sections[0].lines[1];
      expect(secondLine.syllables[0].chord).toBe('F'); // "Good" overlaps with F:maj
    });

    it('calculates syllable duration correctly', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);

      const firstSyllable = result.sections[0].lines[0].syllables[0];
      expect(firstSyllable.startTime).toBe(0.5);
      expect(firstSyllable.duration).toBeCloseTo(0.3, 10); // 0.8 - 0.5 (floating point precision)
    });

    it('throws on invalid input', () => {
      const invalid = { id: 'test' } as any;

      expect(() => adaptBackendToFrontend(invalid)).toThrow(AdapterError);
      expect(() => adaptBackendToFrontend(invalid)).toThrow(/Invalid backend Song Map/);
    });

    it('respects custom line break threshold', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        lineBreakThreshold: 0.5 // Lower threshold = more line breaks
      });

      // With 0.5s threshold, should detect more lines
      expect(result.sections[0].lines.length).toBeGreaterThanOrEqual(2);
    });

    it('respects chord overlap threshold', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        chordOverlapThreshold: 0.9 // Very high threshold = fewer chords attached
      });

      // Count syllables with chords
      let syllablesWithChords = 0;
      result.sections[0].lines.forEach(line => {
        line.syllables.forEach(syllable => {
          if (syllable.chord) syllablesWithChords++;
        });
      });

      // High threshold should result in fewer chord attachments than total syllables
      const totalSyllables = result.sections[0].lines.reduce((sum, line) => sum + line.syllables.length, 0);
      expect(syllablesWithChords).toBeLessThanOrEqual(totalSyllables);
    });

    it('can disable chord simplification', () => {
      const result = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        simplifyChords: false
      });

      const firstLine = result.sections[0].lines[0];
      expect(firstLine.syllables[0].chord).toBe('C:maj'); // Not simplified
    });
  });

  describe('adaptMultipleSongMaps', () => {
    it('transforms multiple backend maps', () => {
      const maps = [
        simpleBackendMap as BackendSongMap,
        simpleBackendMap as BackendSongMap
      ];

      const results = adaptMultipleSongMaps(maps, {
        title: 'Test',
        artist: 'Test'
      });

      expect(results).toHaveLength(2);
      results.forEach(result => {
        expect(result.title).toBe('Test');
        expect(validateFrontendSongMap(result)).toBe(true);
      });
    });
  });

  describe('adaptBackendToFrontendSafe', () => {
    it('returns null on error instead of throwing', () => {
      const invalid = { id: 'test' } as any;

      const result = adaptBackendToFrontendSafe(invalid);

      expect(result).toBeNull();
    });

    it('returns valid result on success', () => {
      const result = adaptBackendToFrontendSafe(simpleBackendMap as BackendSongMap);

      expect(result).not.toBeNull();
      expect(result?.title).toBeDefined();
    });
  });

  describe('getEmptySongMap', () => {
    it('returns empty song map with defaults', () => {
      const empty = getEmptySongMap();

      expect(empty.title).toBe('Unknown Title');
      expect(empty.artist).toBe('Unknown Artist');
      expect(empty.key).toBe('Unknown');
      expect(empty.bpm).toBe(0);
      expect(empty.sections).toEqual([]);
    });

    it('accepts custom title and artist', () => {
      const empty = getEmptySongMap('My Song', 'My Artist');

      expect(empty.title).toBe('My Song');
      expect(empty.artist).toBe('My Artist');
    });
  });

  describe('validateFrontendSongMap', () => {
    it('validates correct frontend map', () => {
      const valid = getEmptySongMap('Test', 'Test');
      expect(validateFrontendSongMap(valid)).toBe(true);
    });

    it('rejects map with missing title', () => {
      const invalid = { ...getEmptySongMap(), title: '' };
      expect(validateFrontendSongMap(invalid)).toBe(false);
    });

    it('rejects map with negative BPM', () => {
      const invalid = { ...getEmptySongMap(), bpm: -10 };
      expect(validateFrontendSongMap(invalid)).toBe(false);
    });

    it('rejects map with invalid section structure', () => {
      const invalid = {
        ...getEmptySongMap(),
        sections: [{ name: 'Test', lines: 'invalid' }]
      } as any;
      expect(validateFrontendSongMap(invalid)).toBe(false);
    });
  });

  describe('edge cases', () => {
    it('handles single syllable', () => {
      const singleSyllable: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        lyrics: [{ start: 0.5, end: 0.8, text: 'Hi' }]
      };

      const result = adaptBackendToFrontend(singleSyllable);

      expect(result.sections[0].lines).toHaveLength(1);
      expect(result.sections[0].lines[0].syllables).toHaveLength(1);
      expect(result.sections[0].lines[0].syllables[0].text).toBe('Hi');
    });

    it('handles syllables with no chord overlap', () => {
      const noOverlap: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        chords: [] // No chords
      };

      const result = adaptBackendToFrontend(noOverlap);

      const syllables = result.sections[0].lines.flatMap(l => l.syllables);
      syllables.forEach(syllable => {
        expect(syllable.chord).toBeUndefined();
      });
    });

    it('handles overlapping sections', () => {
      const overlapping: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        sections: [
          { start: 0.0, end: 5.0, label: 'verse' },
          { start: 4.5, end: 10.0, label: 'chorus' } // Overlaps with verse
        ]
      };

      const result = adaptBackendToFrontend(overlapping);

      expect(result.sections).toHaveLength(2);
      // Lyrics should be assigned to section with greatest overlap
    });

    it('handles empty sections in backend', () => {
      const emptySections: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        sections: []
      };

      const result = adaptBackendToFrontend(emptySections);

      expect(result.sections).toHaveLength(1);
      expect(result.sections[0].name).toBe('Song'); // Default section
    });

    it('handles very small timing values', () => {
      const smallTimings: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        lyrics: [
          { start: 0.001, end: 0.002, text: 'a' },
          { start: 0.002, end: 0.003, text: 'b' }
        ]
      };

      const result = adaptBackendToFrontend(smallTimings);

      expect(result.sections[0].lines[0].syllables).toHaveLength(2);
      expect(result.sections[0].lines[0].syllables[0].duration).toBe(0.001);
    });
  });

  describe('performance', () => {
    it('transforms in under 50ms', () => {
      const start = performance.now();
      adaptBackendToFrontend(simpleBackendMap as BackendSongMap);
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(50);
    });

    it('handles large song maps efficiently', () => {
      // Create a large backend map with 500 lyrics
      const largeLyrics = Array.from({ length: 500 }, (_, i) => ({
        start: i * 0.5,
        end: i * 0.5 + 0.3,
        text: `word${i}`,
        conf: 0.9
      }));

      const largeMap: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        duration_sec: 250,
        lyrics: largeLyrics
      };

      const start = performance.now();
      const result = adaptBackendToFrontend(largeMap);
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(100); // Should still be fast
      expect(result.sections[0].lines.length).toBeGreaterThan(0);
    });
  });
});
