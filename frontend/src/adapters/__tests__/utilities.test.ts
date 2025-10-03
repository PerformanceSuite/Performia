/**
 * Additional utility tests to improve coverage
 */

import { describe, it, expect } from 'vitest';
import {
  simplifyChordLabel,
  simplifyChordLabels,
  isChordSimplified,
  groupAllLyricsIntoLines,
  getLineGroupingStats,
  numberRepeatedSections,
  filterEmptySections,
  getSectionStats,
  BackendLyric,
  Section
} from '../index';

describe('chordSimplifier utilities', () => {
  describe('simplifyChordLabel', () => {
    it('simplifies major chords', () => {
      expect(simplifyChordLabel('C:maj')).toBe('C');
      expect(simplifyChordLabel('F:maj')).toBe('F');
      expect(simplifyChordLabel('G:maj')).toBe('G');
    });

    it('simplifies minor chords', () => {
      expect(simplifyChordLabel('A:min')).toBe('Am');
      expect(simplifyChordLabel('D:min')).toBe('Dm');
      expect(simplifyChordLabel('E:min')).toBe('Em');
    });

    it('handles extended chords', () => {
      expect(simplifyChordLabel('D:min7')).toBe('Dm7');
      expect(simplifyChordLabel('F:maj7')).toBe('Fmaj7');
      expect(simplifyChordLabel('C:maj9')).toBe('Cmaj9');
    });

    it('handles sus, dim, aug chords', () => {
      expect(simplifyChordLabel('G:sus4')).toBe('Gsus4');
      expect(simplifyChordLabel('B:dim')).toBe('Bdim');
      expect(simplifyChordLabel('E:aug')).toBe('Eaug');
    });

    it('handles already simplified chords', () => {
      expect(simplifyChordLabel('C')).toBe('C');
      expect(simplifyChordLabel('Dm7')).toBe('Dm7');
    });

    it('handles empty or invalid input', () => {
      expect(simplifyChordLabel('')).toBe('');
      expect(simplifyChordLabel(null as any)).toBe('');
    });
  });

  describe('simplifyChordLabels', () => {
    it('simplifies multiple chord labels', () => {
      const labels = ['C:maj', 'F:maj', 'G:maj', 'D:min'];
      const simplified = simplifyChordLabels(labels);
      expect(simplified).toEqual(['C', 'F', 'G', 'Dm']);
    });
  });

  describe('isChordSimplified', () => {
    it('detects simplified chords', () => {
      expect(isChordSimplified('C')).toBe(true);
      expect(isChordSimplified('Dm7')).toBe(true);
      expect(isChordSimplified('Fmaj7')).toBe(true);
    });

    it('detects unsimplified chords', () => {
      expect(isChordSimplified('C:maj')).toBe(false);
      expect(isChordSimplified('D:min7')).toBe(false);
    });
  });
});

describe('lyricGrouper utilities', () => {
  const lyrics: BackendLyric[] = [
    { start: 0.5, end: 0.8, text: 'Hello' },
    { start: 0.9, end: 1.2, text: 'world' },
    { start: 2.5, end: 2.8, text: 'Goodbye' },
    { start: 2.9, end: 3.2, text: 'now' }
  ];

  describe('groupAllLyricsIntoLines', () => {
    it('groups all lyrics into lines', () => {
      const lines = groupAllLyricsIntoLines(lyrics, 1.0);
      expect(lines).toHaveLength(2); // Two lines with 1.0s gap
      expect(lines[0]).toHaveLength(2); // "Hello world"
      expect(lines[1]).toHaveLength(2); // "Goodbye now"
    });

    it('handles empty lyrics array', () => {
      const lines = groupAllLyricsIntoLines([]);
      expect(lines).toEqual([]);
    });

    it('respects line break threshold', () => {
      const lines = groupAllLyricsIntoLines(lyrics, 0.5);
      expect(lines).toHaveLength(2);
    });
  });

  describe('getLineGroupingStats', () => {
    it('calculates line grouping statistics', () => {
      const lines = [
        [{ start: 0, end: 1, text: 'a' }, { start: 1, end: 2, text: 'b' }],
        [{ start: 3, end: 4, text: 'c' }]
      ];
      const stats = getLineGroupingStats(lines);

      expect(stats.totalLines).toBe(2);
      expect(stats.totalLyrics).toBe(3);
      expect(stats.avgLyricsPerLine).toBe(1.5);
      expect(stats.minLyricsPerLine).toBe(1);
      expect(stats.maxLyricsPerLine).toBe(2);
    });

    it('handles empty lines array', () => {
      const stats = getLineGroupingStats([]);
      expect(stats.totalLines).toBe(0);
      expect(stats.totalLyrics).toBe(0);
    });
  });
});

describe('sectionBuilder utilities', () => {
  const sections: Section[] = [
    {
      name: 'Verse',
      lines: [
        { syllables: [{ text: 'Hello', startTime: 0, duration: 0.5 }] }
      ]
    },
    {
      name: 'Verse',
      lines: [
        { syllables: [{ text: 'World', startTime: 2, duration: 0.5 }] }
      ]
    },
    {
      name: 'Chorus',
      lines: []
    }
  ];

  describe('numberRepeatedSections', () => {
    it('numbers repeated section names', () => {
      const numbered = numberRepeatedSections(sections);
      expect(numbered[0].name).toBe('Verse 1');
      expect(numbered[1].name).toBe('Verse 2');
      expect(numbered[2].name).toBe('Chorus'); // Not repeated
    });

    it('handles non-repeated sections', () => {
      const singleSections: Section[] = [
        { name: 'Intro', lines: [] },
        { name: 'Verse', lines: [] },
        { name: 'Outro', lines: [] }
      ];
      const numbered = numberRepeatedSections(singleSections);
      expect(numbered[0].name).toBe('Intro');
      expect(numbered[1].name).toBe('Verse');
      expect(numbered[2].name).toBe('Outro');
    });
  });

  describe('filterEmptySections', () => {
    it('filters out empty sections', () => {
      const filtered = filterEmptySections(sections);
      expect(filtered).toHaveLength(2); // Chorus removed
      expect(filtered[0].name).toBe('Verse');
      expect(filtered[1].name).toBe('Verse');
    });

    it('keeps all sections if none are empty', () => {
      const nonEmpty: Section[] = [
        {
          name: 'Verse',
          lines: [{ syllables: [{ text: 'test', startTime: 0, duration: 1 }] }]
        }
      ];
      const filtered = filterEmptySections(nonEmpty);
      expect(filtered).toHaveLength(1);
    });
  });

  describe('getSectionStats', () => {
    it('calculates section statistics', () => {
      const stats = getSectionStats(sections);
      expect(stats.totalSections).toBe(3);
      expect(stats.totalLines).toBe(2);
      expect(stats.totalSyllables).toBe(2);
      expect(stats.avgLinesPerSection).toBeCloseTo(0.666, 2);
      expect(stats.emptySections).toBe(1);
    });

    it('handles empty sections array', () => {
      const stats = getSectionStats([]);
      expect(stats.totalSections).toBe(0);
      expect(stats.totalLines).toBe(0);
      expect(stats.avgLinesPerSection).toBe(0);
    });
  });
});
