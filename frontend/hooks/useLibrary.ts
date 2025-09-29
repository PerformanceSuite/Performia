import { useState, useEffect, useCallback } from 'react';
import { LibrarySong } from '../types';
import { libraryService } from '../services/libraryService';

export const useLibrary = () => {
    const [songs, setSongs] = useState<LibrarySong[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [sortBy, setSortBy] = useState<'title' | 'artist' | 'createdAt' | 'updatedAt'>('updatedAt');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

    const loadSongs = useCallback(() => {
        setLoading(true);
        try {
            const allSongs = searchQuery 
                ? libraryService.searchSongs(searchQuery)
                : libraryService.getAllSongs();
            
            const sortedSongs = libraryService.sortSongs(allSongs, sortBy, sortOrder);
            setSongs(sortedSongs);
        } catch (error) {
            console.error('Failed to load songs:', error);
        } finally {
            setLoading(false);
        }
    }, [searchQuery, sortBy, sortOrder]);

    // Subscribe to library changes
    useEffect(() => {
        const unsubscribe = libraryService.subscribe(() => {
            loadSongs();
        });

        loadSongs();

        return unsubscribe;
    }, [loadSongs]);

    // Update search and sort when they change
    useEffect(() => {
        loadSongs();
    }, [loadSongs]);

    const addSong = (songMap: any, metadata?: Partial<LibrarySong>) => {
        return libraryService.addSong(songMap, metadata);
    };

    const updateSong = (id: string, updates: Partial<LibrarySong>) => {
        return libraryService.updateSong(id, updates);
    };

    const deleteSong = (id: string) => {
        return libraryService.deleteSong(id);
    };

    const getSong = (id: string) => {
        return libraryService.getSong(id);
    };

    const exportSong = (id: string) => {
        return libraryService.exportSong(id);
    };

    const importSong = (jsonData: string) => {
        return libraryService.importSong(jsonData);
    };

    const exportLibrary = () => {
        return libraryService.exportLibrary();
    };

    const clearLibrary = () => {
        libraryService.clear();
    };

    return {
        songs,
        loading,
        searchQuery,
        setSearchQuery,
        sortBy,
        setSortBy,
        sortOrder,
        setSortOrder,
        addSong,
        updateSong,
        deleteSong,
        getSong,
        exportSong,
        importSong,
        exportLibrary,
        clearLibrary,
        count: songs.length,
        totalCount: libraryService.getCount(),
    };
};