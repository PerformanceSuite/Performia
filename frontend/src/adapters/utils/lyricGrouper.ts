/**
 * Lyric grouping utilities for Song Map adapter.
 *
 * Groups flat time-indexed lyrics into lines based on timing gaps.
 */

import { BackendLyric } from '../types';

/**
 * Default threshold for detecting line breaks (seconds of silence).
 */
export const DEFAULT_LINE_BREAK_THRESHOLD = 1.0;

/**
 * Group lyrics into lines based on timing gaps.
 *
 * Detects line breaks when the gap between consecutive lyrics exceeds
 * the threshold. Only processes lyrics within the specified time range.
 *
 * @param lyrics - Array of all lyrics (sorted by start time)
 * @param sectionStart - Start time of section
 * @param sectionEnd - End time of section
 * @param lineBreakThreshold - Gap threshold in seconds (default: 1.0s)
 * @returns Array of line groups (each line is an array of lyrics)
 */
export function groupLyricsIntoLines(
  lyrics: BackendLyric[],
  sectionStart: number,
  sectionEnd: number,
  lineBreakThreshold: number = DEFAULT_LINE_BREAK_THRESHOLD
): BackendLyric[][] {
  // Filter lyrics within section boundaries
  const sectionLyrics = lyrics.filter(
    lyric => lyric.start >= sectionStart && lyric.start < sectionEnd
  );

  if (sectionLyrics.length === 0) {
    return []; // No lyrics in this section
  }

  // Single lyric forms a single line
  if (sectionLyrics.length === 1) {
    return [sectionLyrics];
  }

  // Group lyrics into lines based on timing gaps
  const lines: BackendLyric[][] = [];
  let currentLine: BackendLyric[] = [sectionLyrics[0]];

  for (let i = 1; i < sectionLyrics.length; i++) {
    const prev = sectionLyrics[i - 1];
    const curr = sectionLyrics[i];

    // Calculate gap between end of previous lyric and start of current
    const gap = curr.start - prev.end;

    if (gap > lineBreakThreshold) {
      // Gap detected, start new line
      lines.push(currentLine);
      currentLine = [curr];
    } else {
      // Continue current line
      currentLine.push(curr);
    }
  }

  // Add last line
  if (currentLine.length > 0) {
    lines.push(currentLine);
  }

  return lines;
}

/**
 * Group all lyrics into lines without section boundaries.
 * Useful when no sections are defined in backend data.
 *
 * @param lyrics - Array of all lyrics
 * @param lineBreakThreshold - Gap threshold in seconds (default: 1.0s)
 * @returns Array of line groups
 */
export function groupAllLyricsIntoLines(
  lyrics: BackendLyric[],
  lineBreakThreshold: number = DEFAULT_LINE_BREAK_THRESHOLD
): BackendLyric[][] {
  if (lyrics.length === 0) {
    return [];
  }

  // Find time range of all lyrics
  const startTime = lyrics[0].start;
  const endTime = Math.max(...lyrics.map(l => l.end));

  // Use groupLyricsIntoLines with full time range
  return groupLyricsIntoLines(lyrics, startTime, endTime + 1, lineBreakThreshold);
}

/**
 * Calculate statistics about lyric line grouping.
 * Useful for debugging and validation.
 *
 * @param lines - Array of line groups
 * @returns Statistics object
 */
export function getLineGroupingStats(lines: BackendLyric[][]): {
  totalLines: number;
  totalLyrics: number;
  avgLyricsPerLine: number;
  minLyricsPerLine: number;
  maxLyricsPerLine: number;
} {
  const totalLines = lines.length;
  const totalLyrics = lines.reduce((sum, line) => sum + line.length, 0);
  const avgLyricsPerLine = totalLines > 0 ? totalLyrics / totalLines : 0;

  const lineLengths = lines.map(line => line.length);
  const minLyricsPerLine = totalLines > 0 ? Math.min(...lineLengths) : 0;
  const maxLyricsPerLine = totalLines > 0 ? Math.max(...lineLengths) : 0;

  return {
    totalLines,
    totalLyrics,
    avgLyricsPerLine,
    minLyricsPerLine,
    maxLyricsPerLine
  };
}
