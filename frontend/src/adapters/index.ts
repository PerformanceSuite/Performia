/**
 * Song Map Adapter - Public API
 *
 * Export all public types and functions for external use.
 */

// Main adapter functions
export {
  adaptBackendToFrontend,
  adaptMultipleSongMaps,
  adaptBackendToFrontendSafe,
  getEmptySongMap,
  validateFrontendSongMap
} from './songMapAdapter';

// Type definitions
export type {
  BackendSongMap,
  BackendChord,
  BackendLyric,
  BackendSection,
  BackendKey,
  BackendNote,
  FrontendSongMap,
  Section,
  Line,
  Syllable,
  SongMap,
  AdapterOptions,
  SectionBoundary,
  ExtractedMetadata
} from './types';

// Error types
export {
  AdapterError,
  AdapterErrorCode
} from './types';

// Type guards
export {
  isValidBackendSongMap,
  isValidFrontendSongMap
} from './types';

// Utility functions (for advanced use cases)
export {
  extractMetadata,
  extractTitle,
  extractArtist,
  extractKey,
  extractBpm,
  formatKey,
  parseFilename,
  capitalizeWords
} from './utils/metadata';

export {
  simplifyChordLabel,
  simplifyChordLabels,
  isSimplified as isChordSimplified
} from './utils/chordSimplifier';

export {
  groupLyricsIntoLines,
  groupAllLyricsIntoLines,
  getLineGroupingStats,
  DEFAULT_LINE_BREAK_THRESHOLD
} from './utils/lyricGrouper';

export {
  findChordForSyllable,
  calculateTimeOverlap,
  mapChordsToSyllables,
  findOverlappingChords,
  getChordMappingStats,
  DEFAULT_CHORD_OVERLAP_THRESHOLD
} from './utils/chordMapper';

export {
  prepareSectionBoundaries,
  capitalizeLabel,
  buildSections,
  numberRepeatedSections,
  filterEmptySections,
  getSectionStats
} from './utils/sectionBuilder';
