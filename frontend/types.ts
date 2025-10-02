/**
 * Frontend Types - Now powered by Song Map Adapter
 *
 * This file re-exports types from the adapter to maintain backward compatibility
 * while making the adapter types the single source of truth.
 */

// Re-export core Song Map types from adapter
export type {
    FrontendSongMap,
    Section,
    Line,
    Syllable,
    SongMap,
    BackendSongMap,
    AdapterOptions
} from './src/adapters';

// Re-export adapter functions for convenience
export {
    adaptBackendToFrontend,
    adaptBackendToFrontendSafe,
    adaptMultipleSongMaps,
    getEmptySongMap,
    validateFrontendSongMap,
    isValidBackendSongMap,
    isValidFrontendSongMap,
    AdapterError,
    AdapterErrorCode
} from './src/adapters';

// UI-specific types (not part of adapter)
export type ChordDisplayMode = 'off' | 'names' | 'diagrams';

// Import SongMap type for use in interfaces below
import type { SongMap } from './src/adapters';

// Library Management Types
export interface LibrarySong {
    id: string;
    songMap: SongMap;
    jobId?: string;  // Optional job ID for audio playback
    createdAt: Date;
    updatedAt: Date;
    tags?: string[];
    genre?: string;
    difficulty?: 'beginner' | 'intermediate' | 'advanced';
}

export interface LibraryState {
    songs: LibrarySong[];
    currentSongId?: string;
    searchQuery: string;
    sortBy: 'title' | 'artist' | 'createdAt' | 'updatedAt';
    sortOrder: 'asc' | 'desc';
}
