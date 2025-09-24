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
