/**
 * Song Map Adapter - Main transformation logic.
 *
 * Transforms backend Song Map (flat, time-indexed) to frontend format (hierarchical).
 *
 * Algorithm:
 * 1. Extract metadata (title, artist, key, BPM)
 * 2. Prepare section boundaries
 * 3. Group lyrics into lines within sections
 * 4. Map chords to syllables by time overlap
 * 5. Build hierarchical section structure
 */

import {
  BackendSongMap,
  FrontendSongMap,
  AdapterOptions,
  AdapterError,
  AdapterErrorCode,
  isValidBackendSongMap
} from './types';
import { extractMetadata } from './utils/metadata';
import { prepareSectionBoundaries, buildSections } from './utils/sectionBuilder';

/**
 * Default adapter options.
 */
const DEFAULT_OPTIONS: Required<AdapterOptions> = {
  title: '',
  artist: '',
  lineBreakThreshold: 1.0,
  chordOverlapThreshold: 0.1,
  simplifyChords: true
};

/**
 * Transform backend Song Map to frontend format.
 *
 * This is the main entry point for the adapter. It performs the complete
 * transformation from flat, time-indexed backend data to hierarchical
 * frontend structure.
 *
 * Performance target: < 50ms for typical songs (3-5 minutes, 200-400 lyrics)
 *
 * @param backendMap - Backend Song Map data
 * @param options - Optional transformation parameters
 * @returns Frontend-compatible Song Map
 * @throws {AdapterError} If transformation fails or input is invalid
 *
 * @example
 * ```typescript
 * const backendMap = await loadBackendSongMap('song.json');
 * const frontendMap = adaptBackendToFrontend(backendMap, {
 *   title: 'Yesterday',
 *   artist: 'The Beatles'
 * });
 * ```
 */
export function adaptBackendToFrontend(
  backendMap: BackendSongMap,
  options?: AdapterOptions
): FrontendSongMap {
  // Validate input
  if (!isValidBackendSongMap(backendMap)) {
    throw new AdapterError(
      'Invalid backend Song Map structure',
      AdapterErrorCode.INVALID_INPUT,
      { backendMap }
    );
  }

  // Merge options with defaults
  const opts: Required<AdapterOptions> = {
    ...DEFAULT_OPTIONS,
    ...options
  };

  try {
    // Step 1: Extract metadata
    const metadata = extractMetadata(backendMap);

    // Apply overrides from options
    const title = opts.title || metadata.title;
    const artist = opts.artist || metadata.artist;
    const key = metadata.key;
    const bpm = metadata.bpm;

    // Step 2: Prepare section boundaries
    const sectionBoundaries = prepareSectionBoundaries(backendMap);

    // Step 3-5: Build section hierarchy with lyrics and chords
    const sections = buildSections(
      sectionBoundaries,
      backendMap.lyrics,
      backendMap.chords,
      opts.lineBreakThreshold,
      opts.chordOverlapThreshold,
      opts.simplifyChords
    );

    // Return frontend format
    return {
      title,
      artist,
      key,
      bpm,
      sections
    };
  } catch (error) {
    // Re-throw AdapterError as-is
    if (error instanceof AdapterError) {
      throw error;
    }

    // Wrap other errors
    throw new AdapterError(
      `Transformation failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      AdapterErrorCode.TRANSFORMATION_FAILED,
      { originalError: error, backendMap }
    );
  }
}

/**
 * Batch transform multiple backend Song Maps.
 *
 * More efficient than calling adaptBackendToFrontend multiple times
 * when processing many songs.
 *
 * @param backendMaps - Array of backend Song Maps
 * @param options - Optional transformation parameters (applied to all)
 * @returns Array of frontend Song Maps
 * @throws {AdapterError} If any transformation fails (fails fast)
 */
export function adaptMultipleSongMaps(
  backendMaps: BackendSongMap[],
  options?: AdapterOptions
): FrontendSongMap[] {
  return backendMaps.map(backendMap =>
    adaptBackendToFrontend(backendMap, options)
  );
}

/**
 * Safe version of adaptBackendToFrontend that returns null on error.
 *
 * Useful for batch processing where you don't want one failed transformation
 * to stop the entire process.
 *
 * @param backendMap - Backend Song Map data
 * @param options - Optional transformation parameters
 * @returns Frontend Song Map or null if transformation fails
 */
export function adaptBackendToFrontendSafe(
  backendMap: BackendSongMap,
  options?: AdapterOptions
): FrontendSongMap | null {
  try {
    return adaptBackendToFrontend(backendMap, options);
  } catch (error) {
    console.error('Song Map transformation failed:', error);
    return null;
  }
}

/**
 * Get default/empty frontend Song Map.
 *
 * Useful for fallback when transformation fails or data is unavailable.
 *
 * @param title - Optional title
 * @param artist - Optional artist
 * @returns Empty frontend Song Map
 */
export function getEmptySongMap(
  title: string = 'Unknown Title',
  artist: string = 'Unknown Artist'
): FrontendSongMap {
  return {
    title,
    artist,
    key: 'Unknown',
    bpm: 0,
    sections: []
  };
}

/**
 * Validate that a frontend Song Map has valid structure.
 *
 * Performs deep validation of section/line/syllable hierarchy.
 *
 * @param frontendMap - Frontend Song Map to validate
 * @returns True if valid, false otherwise
 */
export function validateFrontendSongMap(frontendMap: FrontendSongMap): boolean {
  try {
    // Check required fields
    if (!frontendMap.title || !frontendMap.artist || !frontendMap.key) {
      return false;
    }

    if (typeof frontendMap.bpm !== 'number' || frontendMap.bpm < 0) {
      return false;
    }

    if (!Array.isArray(frontendMap.sections)) {
      return false;
    }

    // Validate each section
    for (const section of frontendMap.sections) {
      if (!section.name || !Array.isArray(section.lines)) {
        return false;
      }

      // Validate each line
      for (const line of section.lines) {
        if (!Array.isArray(line.syllables)) {
          return false;
        }

        // Validate each syllable
        for (const syllable of line.syllables) {
          if (
            !syllable.text ||
            typeof syllable.startTime !== 'number' ||
            typeof syllable.duration !== 'number' ||
            syllable.startTime < 0 ||
            syllable.duration < 0
          ) {
            return false;
          }
        }
      }
    }

    return true;
  } catch (error) {
    return false;
  }
}
