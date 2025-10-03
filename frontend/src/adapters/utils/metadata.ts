/**
 * Metadata extraction utilities for Song Map adapter.
 *
 * Handles extraction of title, artist, key, and BPM from backend Song Map data.
 */

import { BackendSongMap, ExtractedMetadata } from '../types';

/**
 * Extract metadata from backend Song Map.
 *
 * @param backendMap - Backend Song Map data
 * @returns Extracted metadata
 */
export function extractMetadata(backendMap: BackendSongMap): ExtractedMetadata {
  const title = extractTitle(backendMap);
  const artist = extractArtist(backendMap);
  const key = extractKey(backendMap);
  const bpm = extractBpm(backendMap);

  return { title, artist, key, bpm };
}

/**
 * Extract title from backend data.
 * Attempts to parse from provenance.source_path, falls back to "Unknown Title".
 *
 * @param backendMap - Backend Song Map data
 * @returns Title string
 */
export function extractTitle(backendMap: BackendSongMap): string {
  if (backendMap.provenance?.source_path) {
    const parsed = parseFilename(backendMap.provenance.source_path);
    if (parsed.title) {
      return parsed.title;
    }
  }
  return 'Unknown Title';
}

/**
 * Extract artist from backend data.
 * Attempts to parse from provenance.source_path, falls back to "Unknown Artist".
 *
 * @param backendMap - Backend Song Map data
 * @returns Artist string
 */
export function extractArtist(backendMap: BackendSongMap): string {
  if (backendMap.provenance?.source_path) {
    const parsed = parseFilename(backendMap.provenance.source_path);
    if (parsed.artist) {
      return parsed.artist;
    }
  }
  return 'Unknown Artist';
}

/**
 * Extract primary key from backend data.
 * Uses first key in array, formats as "F Major" or "D# Minor".
 *
 * @param backendMap - Backend Song Map data
 * @returns Formatted key string
 */
export function extractKey(backendMap: BackendSongMap): string {
  if (!backendMap.key || backendMap.key.length === 0) {
    return 'Unknown';
  }

  // Use first key (most songs have single key throughout)
  const primaryKey = backendMap.key[0];
  return formatKey(primaryKey.tonic, primaryKey.mode);
}

/**
 * Extract BPM from backend data.
 * Rounds to nearest integer. Returns 0 if tempo detection failed.
 *
 * @param backendMap - Backend Song Map data
 * @returns BPM as integer
 */
export function extractBpm(backendMap: BackendSongMap): number {
  const bpm = backendMap.tempo.bpm_global;
  return bpm > 0 ? Math.round(bpm) : 0;
}

/**
 * Format key from tonic and mode.
 * Examples: "F" + "major" → "F Major", "D#" + "minor" → "D# Minor"
 *
 * @param tonic - Root note (e.g., "D#", "F", "C")
 * @param mode - Mode (e.g., "major", "minor")
 * @returns Formatted key string
 */
export function formatKey(tonic: string, mode: string): string {
  const capitalizedMode = mode.charAt(0).toUpperCase() + mode.slice(1);
  return `${tonic} ${capitalizedMode}`;
}

/**
 * Parse filename to extract title and artist.
 * Supports formats like:
 * - "yesterday_beatles.wav" → { title: "Yesterday", artist: "Beatles" }
 * - "song_title.mp3" → { title: "Song Title" }
 * - "/path/to/file.wav" → { title: "File" }
 *
 * @param filepath - File path string
 * @returns Parsed title and artist (if available)
 */
export function parseFilename(filepath: string): { title?: string; artist?: string } {
  // Extract filename from path
  const filename = filepath.split('/').pop() || filepath;

  // Remove extension
  const nameWithoutExt = filename.replace(/\.(wav|mp3|flac|m4a|ogg)$/i, '');

  // Try to split on underscore (title_artist format)
  const parts = nameWithoutExt.split('_');

  if (parts.length >= 2) {
    // Assume first part is title, second is artist
    return {
      title: capitalizeWords(parts[0]),
      artist: capitalizeWords(parts[1])
    };
  } else if (parts.length === 1) {
    // Single part, use as title
    return {
      title: capitalizeWords(parts[0])
    };
  }

  return {};
}

/**
 * Capitalize words in a string.
 * Examples: "hello world" → "Hello World", "the_beatles" → "The Beatles"
 *
 * @param str - Input string
 * @returns Capitalized string
 */
export function capitalizeWords(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}
