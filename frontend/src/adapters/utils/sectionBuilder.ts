/**
 * Section building utilities for Song Map adapter.
 *
 * Prepares section boundaries and builds hierarchical section structure.
 */

import {
  BackendSongMap,
  BackendSection,
  SectionBoundary,
  Section,
  Line,
  Syllable,
  BackendLyric,
  BackendChord
} from '../types';
import { groupLyricsIntoLines } from './lyricGrouper';
import { findChordForSyllable } from './chordMapper';

/**
 * Prepare section boundaries from backend data.
 *
 * If sections exist, use them. Otherwise create a single default section
 * spanning the entire song duration.
 *
 * @param backendMap - Backend Song Map data
 * @returns Array of section boundaries
 */
export function prepareSectionBoundaries(backendMap: BackendSongMap): SectionBoundary[] {
  if (!backendMap.sections || backendMap.sections.length === 0) {
    // No sections detected, create default section
    return [{
      start: 0,
      end: backendMap.duration_sec,
      label: 'Song'
    }];
  }

  // Sort sections by start time (should already be sorted, but ensure)
  const sorted = [...backendMap.sections].sort((a, b) => a.start - b.start);

  // Map to SectionBoundary format with capitalized labels
  return sorted.map(section => ({
    start: section.start,
    end: section.end,
    label: capitalizeLabel(section.label)
  }));
}

/**
 * Capitalize and format section label.
 *
 * Examples:
 * - "intro" → "Intro"
 * - "verse" → "Verse"
 * - "verse_1" → "Verse 1"
 * - "chorus" → "Chorus"
 *
 * @param label - Raw section label from backend
 * @returns Formatted label
 */
export function capitalizeLabel(label: string): string {
  return label
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Build section hierarchy from section boundaries and lyrics.
 *
 * This is the main function that combines all utilities to create
 * the hierarchical section structure expected by the frontend.
 *
 * @param sectionBoundaries - Prepared section boundaries
 * @param lyrics - All lyrics from backend
 * @param chords - All chords from backend
 * @param lineBreakThreshold - Gap threshold for line detection
 * @param chordOverlapThreshold - Overlap threshold for chord mapping
 * @param simplifyChords - Whether to simplify chord labels
 * @returns Array of frontend Section objects
 */
export function buildSections(
  sectionBoundaries: SectionBoundary[],
  lyrics: BackendLyric[],
  chords: BackendChord[],
  lineBreakThreshold: number = 1.0,
  chordOverlapThreshold: number = 0.1,
  simplifyChords: boolean = true
): Section[] {
  const sections: Section[] = [];

  for (const boundary of sectionBoundaries) {
    // Group lyrics into lines for this section
    const lineGroups = groupLyricsIntoLines(
      lyrics,
      boundary.start,
      boundary.end,
      lineBreakThreshold
    );

    // Build Line objects with syllables
    const lines: Line[] = lineGroups.map(lineGroup => {
      const syllables: Syllable[] = lineGroup.map(lyric => ({
        text: lyric.text,
        startTime: lyric.start,
        duration: lyric.end - lyric.start,
        chord: findChordForSyllable(
          lyric,
          chords,
          chordOverlapThreshold,
          simplifyChords
        )
      }));

      return { syllables };
    });

    // Create section
    sections.push({
      name: boundary.label,
      lines: lines
    });
  }

  return sections;
}

/**
 * Add section numbering to repeated section names.
 *
 * Example: ["Verse", "Verse", "Chorus", "Verse"]
 *       → ["Verse 1", "Verse 2", "Chorus", "Verse 3"]
 *
 * @param sections - Array of sections
 * @returns Array of sections with numbered names
 */
export function numberRepeatedSections(sections: Section[]): Section[] {
  const counts: { [key: string]: number } = {};
  const totalCounts: { [key: string]: number } = {};

  // Count occurrences of each section name
  sections.forEach(section => {
    const baseName = section.name;
    totalCounts[baseName] = (totalCounts[baseName] || 0) + 1;
  });

  // Add numbers to sections that appear multiple times
  return sections.map(section => {
    const baseName = section.name;

    // Only number if section appears more than once
    if (totalCounts[baseName] > 1) {
      counts[baseName] = (counts[baseName] || 0) + 1;
      return {
        ...section,
        name: `${baseName} ${counts[baseName]}`
      };
    }

    return section;
  });
}

/**
 * Filter out empty sections (sections with no lines).
 *
 * @param sections - Array of sections
 * @returns Array of sections with at least one line
 */
export function filterEmptySections(sections: Section[]): Section[] {
  return sections.filter(section => section.lines.length > 0);
}

/**
 * Calculate statistics about section structure.
 *
 * @param sections - Array of sections
 * @returns Statistics object
 */
export function getSectionStats(sections: Section[]): {
  totalSections: number;
  totalLines: number;
  totalSyllables: number;
  avgLinesPerSection: number;
  avgSyllablesPerLine: number;
  emptySections: number;
} {
  const totalSections = sections.length;
  let totalLines = 0;
  let totalSyllables = 0;
  let emptySections = 0;

  sections.forEach(section => {
    if (section.lines.length === 0) {
      emptySections++;
    }
    totalLines += section.lines.length;
    section.lines.forEach(line => {
      totalSyllables += line.syllables.length;
    });
  });

  const avgLinesPerSection = totalSections > 0 ? totalLines / totalSections : 0;
  const avgSyllablesPerLine = totalLines > 0 ? totalSyllables / totalLines : 0;

  return {
    totalSections,
    totalLines,
    totalSyllables,
    avgLinesPerSection,
    avgSyllablesPerLine,
    emptySections
  };
}
