import { LibrarySong, SongMap } from '../types';

class LibraryService {
    private songs: Map<string, LibrarySong> = new Map();
    private listeners: Set<() => void> = new Set();

    constructor() {
        this.loadFromStorage();
    }

    // Generate unique ID for songs
    private generateId(): string {
        return `song_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    // Add listener for changes
    subscribe(listener: () => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notify(): void {
        this.listeners.forEach(listener => listener());
        this.saveToStorage();
    }

    // CRUD Operations
    addSong(songMap: SongMap, metadata?: Partial<LibrarySong>): LibrarySong {
        const id = this.generateId();
        const now = new Date();
        
        const librarySong: LibrarySong = {
            id,
            songMap,
            createdAt: now,
            updatedAt: now,
            tags: metadata?.tags || [],
            genre: metadata?.genre,
            difficulty: metadata?.difficulty || 'intermediate',
        };

        this.songs.set(id, librarySong);
        this.notify();
        return librarySong;
    }

    getSong(id: string): LibrarySong | undefined {
        return this.songs.get(id);
    }

    getAllSongs(): LibrarySong[] {
        return Array.from(this.songs.values());
    }

    updateSong(id: string, updates: Partial<LibrarySong>): LibrarySong | null {
        const existing = this.songs.get(id);
        if (!existing) return null;

        const updated: LibrarySong = {
            ...existing,
            ...updates,
            id, // Ensure ID doesn't change
            updatedAt: new Date(),
        };

        this.songs.set(id, updated);
        this.notify();
        return updated;
    }

    deleteSong(id: string): boolean {
        const deleted = this.songs.delete(id);
        if (deleted) {
            this.notify();
        }
        return deleted;
    }

    // Search and filter
    searchSongs(query: string): LibrarySong[] {
        if (!query.trim()) return this.getAllSongs();

        const lowerQuery = query.toLowerCase();
        return this.getAllSongs().filter(song => 
            song.songMap.title.toLowerCase().includes(lowerQuery) ||
            song.songMap.artist.toLowerCase().includes(lowerQuery) ||
            song.tags?.some(tag => tag.toLowerCase().includes(lowerQuery)) ||
            song.genre?.toLowerCase().includes(lowerQuery)
        );
    }

    // Sort songs
    sortSongs(songs: LibrarySong[], sortBy: 'title' | 'artist' | 'createdAt' | 'updatedAt', order: 'asc' | 'desc' = 'asc'): LibrarySong[] {
        return [...songs].sort((a, b) => {
            let comparison = 0;
            
            switch (sortBy) {
                case 'title':
                    comparison = a.songMap.title.localeCompare(b.songMap.title);
                    break;
                case 'artist':
                    comparison = a.songMap.artist.localeCompare(b.songMap.artist);
                    break;
                case 'createdAt':
                    comparison = a.createdAt.getTime() - b.createdAt.getTime();
                    break;
                case 'updatedAt':
                    comparison = a.updatedAt.getTime() - b.updatedAt.getTime();
                    break;
            }
            
            return order === 'desc' ? -comparison : comparison;
        });
    }

    // Storage (localStorage for now, easily replaceable)
    private saveToStorage(): void {
        try {
            const data = Array.from(this.songs.entries()).map(([id, song]) => ({
                ...song,
                createdAt: song.createdAt.toISOString(),
                updatedAt: song.updatedAt.toISOString(),
            }));
            localStorage.setItem('performia_library', JSON.stringify(data));
        } catch (error) {
            console.error('Failed to save library to storage:', error);
        }
    }

    private loadFromStorage(): void {
        try {
            const stored = localStorage.getItem('performia_library');
            if (stored) {
                const data = JSON.parse(stored);
                data.forEach((item: any) => {
                    const song: LibrarySong = {
                        ...item,
                        createdAt: new Date(item.createdAt),
                        updatedAt: new Date(item.updatedAt),
                    };
                    this.songs.set(song.id, song);
                });
            }
        } catch (error) {
            console.error('Failed to load library from storage:', error);
        }
    }

    // Import/Export
    exportSong(id: string): string | null {
        const song = this.getSong(id);
        if (!song) return null;
        return JSON.stringify(song, null, 2);
    }

    exportLibrary(): string {
        const songs = this.getAllSongs();
        return JSON.stringify(songs, null, 2);
    }

    importSong(jsonData: string): LibrarySong | null {
        try {
            const data = JSON.parse(jsonData);
            // If it's a full LibrarySong
            if (data.songMap && data.id) {
                return this.addSong(data.songMap, {
                    tags: data.tags,
                    genre: data.genre,
                    difficulty: data.difficulty,
                });
            }
            // If it's just a SongMap
            if (data.title && data.artist && data.sections) {
                return this.addSong(data);
            }
            return null;
        } catch (error) {
            console.error('Failed to import song:', error);
            return null;
        }
    }

    // Get song count
    getCount(): number {
        return this.songs.size;
    }

    // Clear all songs (for testing/reset)
    clear(): void {
        this.songs.clear();
        this.notify();
    }
}

// Singleton instance
export const libraryService = new LibraryService();