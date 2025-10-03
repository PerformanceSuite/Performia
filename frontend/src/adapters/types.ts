/**
 * TypeScript type definitions for Song Map adapter.
 *
 * This file contains:
 * - Backend Song Map interfaces (matching backend/schemas/song_map.schema.json)
 * - Frontend Song Map interfaces (hierarchical format)
 * - Adapter configuration options
 * - Error types
 * - Type guards
 */

/**
 * Backend Song Map structure (flat, time-indexed).
 * All fields use snake_case as per Python backend conventions.
 */
export interface BackendSongMap {
  // Required fields
  id: string;
  duration_sec: number;
  tempo: {
    bpm_global: number;
    curve?: [number, number][];
    confidence?: number;
  };
  beats: number[];
  downbeats: number[];
  meter: {
    numerator: number;
    denominator: number;
  };
  chords: BackendChord[];
  lyrics: BackendLyric[];

  // Optional fields
  sections?: BackendSection[];
  key?: BackendKey[];
  performance?: {
    melody?: BackendNote[];
    bass?: BackendNote[];
  };
  provenance?: {
    separation?: string;
    asr?: string;
    harmony?: string;
    git_sha?: string;
    created_at?: string;
    source_path?: string;
    [key: string]: any; // Allow additional provenance fields
  };
}

export interface BackendChord {
  start: number;
  end: number;
  label: string;
  conf?: number;
}

export interface BackendLyric {
  start: number;
  end: number;
  text: string;
  conf?: number;
}

export interface BackendSection {
  start: number;
  end: number;
  label: string;
  confidence?: number;
}

export interface BackendKey {
  start: number;
  end: number;
  tonic: string; // e.g., "D#", "F", "C"
  mode: string;  // e.g., "major", "minor"
  conf?: number;
}

export interface BackendNote {
  time: number;
  midi: number;      // MIDI note number (0-127)
  velocity: number;  // Note velocity (0-127)
  duration: number;
  confidence: number;
}

/**
 * Frontend Song Map structure (hierarchical).
 * All fields use camelCase as per TypeScript conventions.
 */
export interface FrontendSongMap {
  title: string;
  artist: string;
  key: string;    // e.g., "F Major", "D# Minor"
  bpm: number;
  sections: Section[];
}

export interface Section {
  name: string;   // e.g., "Verse 1", "Chorus", "Intro"
  lines: Line[];
}

export interface Line {
  syllables: Syllable[];
}

export interface Syllable {
  text: string;
  startTime: number;
  duration: number;
  chord?: string;   // Optional chord symbol (e.g., "C", "Dm7", "Fmaj7")
}

/**
 * Alias for backward compatibility with existing frontend code
 */
export type SongMap = FrontendSongMap;

/**
 * Options for adapter transformation
 */
export interface AdapterOptions {
  /**
   * Override title (if not derivable from backend data)
   */
  title?: string;

  /**
   * Override artist (if not derivable from backend data)
   */
  artist?: string;

  /**
   * Threshold for detecting line breaks (seconds of silence)
   * Default: 1.0
   */
  lineBreakThreshold?: number;

  /**
   * Minimum overlap percentage for chord attachment
   * Default: 0.1 (10%)
   */
  chordOverlapThreshold?: number;

  /**
   * Whether to simplify chord labels (A:maj → A)
   * Default: true
   */
  simplifyChords?: boolean;
}

/**
 * Error codes for adapter errors
 */
export enum AdapterErrorCode {
  INVALID_INPUT = 'INVALID_INPUT',
  MISSING_REQUIRED_FIELD = 'MISSING_REQUIRED_FIELD',
  INVALID_TIME_RANGE = 'INVALID_TIME_RANGE',
  TRANSFORMATION_FAILED = 'TRANSFORMATION_FAILED',
}

/**
 * Error thrown during adapter transformation
 */
export class AdapterError extends Error {
  constructor(
    message: string,
    public readonly code: AdapterErrorCode,
    public readonly details?: any
  ) {
    super(message);
    this.name = 'AdapterError';
  }
}

/**
 * Internal type for section boundaries during transformation
 */
export interface SectionBoundary {
  start: number;
  end: number;
  label: string;
}

/**
 * Internal type for extracted metadata
 */
export interface ExtractedMetadata {
  title: string;
  artist: string;
  key: string;
  bpm: number;
}

/**
 * Type guard to check if backend data is valid
 */
export function isValidBackendSongMap(data: any): data is BackendSongMap {
  return (
    typeof data === 'object' &&
    data !== null &&
    typeof data.id === 'string' &&
    typeof data.duration_sec === 'number' &&
    typeof data.tempo?.bpm_global === 'number' &&
    Array.isArray(data.beats) &&
    Array.isArray(data.downbeats) &&
    Array.isArray(data.chords) &&
    Array.isArray(data.lyrics) &&
    typeof data.meter?.numerator === 'number' &&
    typeof data.meter?.denominator === 'number'
  );
}

/**
 * Type guard to check if frontend data is valid
 */
export function isValidFrontendSongMap(data: any): data is FrontendSongMap {
  return (
    typeof data === 'object' &&
    data !== null &&
    typeof data.title === 'string' &&
    typeof data.artist === 'string' &&
    typeof data.key === 'string' &&
    typeof data.bpm === 'number' &&
    Array.isArray(data.sections)
  );
}
