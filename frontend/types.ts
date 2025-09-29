export interface Syllable {
    text: string;
    startTime: number;
    duration: number;
    chord?: string;
}

export interface Line {
    syllables: Syllable[];
}

export interface Section {
    name: string;
    lines: Line[];
}

export interface SongMap {
    title: string;
    artist: string;
    key: string;
    bpm: number;
    sections: Section[];
}

export type ChordDisplayMode = 'off' | 'names' | 'diagrams';

// Library Management Types
export interface LibrarySong {
    id: string;
    songMap: SongMap;
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
