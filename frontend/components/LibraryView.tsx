import React, { useState } from 'react';
import { LibrarySong, SongMap } from '../types';
import { useLibrary } from '../hooks/useLibrary';

interface LibraryViewProps {
    currentSong?: SongMap;
    onSongSelect: (songMap: SongMap) => void;
    onClose: () => void;
}

const LibraryView: React.FC<LibraryViewProps> = ({ currentSong, onSongSelect, onClose }) => {
    const {
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
        exportSong,
        importSong,
        exportLibrary,
        clearLibrary,
        count
    } = useLibrary();

    const [showImportDialog, setShowImportDialog] = useState(false);
    const [importData, setImportData] = useState('');
    const [editingSong, setEditingSong] = useState<LibrarySong | null>(null);
    const [editForm, setEditForm] = useState<{
        genre: string;
        difficulty: 'beginner' | 'intermediate' | 'advanced';
        tags: string;
    }>({ genre: '', difficulty: 'intermediate', tags: '' });

    const handleSaveCurrentSong = () => {
        if (currentSong) {
            addSong(currentSong);
        }
    };

    const handleDeleteSong = (id: string, event: React.MouseEvent) => {
        event.stopPropagation();
        if (confirm('Are you sure you want to delete this song?')) {
            deleteSong(id);
        }
    };

    const handleEditSong = (song: LibrarySong, event: React.MouseEvent) => {
        event.stopPropagation();
        setEditingSong(song);
        setEditForm({
            genre: song.genre || '',
            difficulty: song.difficulty || 'intermediate',
            tags: song.tags?.join(', ') || ''
        });
    };

    const handleSaveEdit = () => {
        if (editingSong) {
            const tags = editForm.tags
                .split(',')
                .map(tag => tag.trim())
                .filter(tag => tag.length > 0);
            
            updateSong(editingSong.id, {
                genre: editForm.genre || undefined,
                difficulty: editForm.difficulty,
                tags: tags.length > 0 ? tags : undefined
            });
            
            setEditingSong(null);
        }
    };

    const handleCancelEdit = () => {
        setEditingSong(null);
        setEditForm({ genre: '', difficulty: 'intermediate', tags: '' });
    };

    const handleExportSong = (id: string, event: React.MouseEvent) => {
        event.stopPropagation();
        const exported = exportSong(id);
        if (exported) {
            const blob = new Blob([exported], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `song_${id}.json`;
            a.click();
            URL.revokeObjectURL(url);
        }
    };

    const handleImportSong = () => {
        if (importData.trim()) {
            const imported = importSong(importData);
            if (imported) {
                setImportData('');
                setShowImportDialog(false);
            } else {
                alert('Failed to import song. Please check the format.');
            }
        }
    };

    const handleExportLibrary = () => {
        const exported = exportLibrary();
        const blob = new Blob([exported], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'performia_library.json';
        a.click();
        URL.revokeObjectURL(url);
    };

    const formatDate = (date: Date) => {
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    const getDifficultyColor = (difficulty?: string) => {
        switch (difficulty) {
            case 'beginner': return 'text-green-400';
            case 'intermediate': return 'text-yellow-400';
            case 'advanced': return 'text-red-400';
            default: return 'text-gray-400';
        }
    };

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
                <h2 className="text-xl font-bold text-performia-cyan">Song Library</h2>
                <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-400">{count} songs</span>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-white"
                    >
                        ✕
                    </button>
                </div>
            </div>

            {/* Controls */}
            <div className="p-4 space-y-3 border-b border-gray-700">
                {/* Search */}
                <div>
                    <input
                        type="text"
                        placeholder="Search songs, artists, tags..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-performia-cyan focus:outline-none"
                    />
                </div>

                {/* Sort Controls */}
                <div className="flex items-center space-x-4">
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value as any)}
                        className="px-3 py-1 bg-gray-800 border border-gray-600 rounded text-white focus:border-performia-cyan focus:outline-none"
                    >
                        <option value="updatedAt">Last Modified</option>
                        <option value="createdAt">Date Added</option>
                        <option value="title">Title</option>
                        <option value="artist">Artist</option>
                    </select>
                    <button
                        onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                        className="px-3 py-1 bg-gray-800 border border-gray-600 rounded text-white hover:bg-gray-700"
                    >
                        {sortOrder === 'asc' ? '↑' : '↓'}
                    </button>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-2">
                    {currentSong && (
                        <button
                            onClick={handleSaveCurrentSong}
                            className="px-3 py-1 bg-performia-cyan text-black rounded font-medium hover:bg-cyan-300"
                        >
                            Save Current Song
                        </button>
                    )}
                    <button
                        onClick={() => setShowImportDialog(true)}
                        className="px-3 py-1 bg-gray-700 text-white rounded hover:bg-gray-600"
                    >
                        Import Song
                    </button>
                    <button
                        onClick={handleExportLibrary}
                        className="px-3 py-1 bg-gray-700 text-white rounded hover:bg-gray-600"
                    >
                        Export Library
                    </button>
                    {count > 0 && (
                        <button
                            onClick={() => confirm('Clear entire library?') && clearLibrary()}
                            className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                        >
                            Clear All
                        </button>
                    )}
                </div>
            </div>

            {/* Song List */}
            <div className="flex-1 overflow-y-auto">
                {loading ? (
                    <div className="p-4 text-center text-gray-400">Loading...</div>
                ) : songs.length === 0 ? (
                    <div className="p-4 text-center text-gray-400">
                        {searchQuery ? 'No songs match your search.' : 'No songs in library yet.'}
                    </div>
                ) : (
                    <div className="space-y-2 p-4">
                        {songs.map((song) => (
                            <div
                                key={song.id}
                                onClick={() => onSongSelect(song.songMap)}
                                className="p-3 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-700 transition-colors"
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <h3 className="font-semibold text-white">{song.songMap.title}</h3>
                                        <p className="text-gray-400">{song.songMap.artist}</p>
                                        <div className="flex items-center space-x-4 mt-2 text-sm">
                                            <span className="text-gray-500">{song.songMap.key}</span>
                                            <span className="text-gray-500">{song.songMap.bpm} BPM</span>
                                            {song.difficulty && (
                                                <span className={getDifficultyColor(song.difficulty)}>
                                                    {song.difficulty}
                                                </span>
                                            )}
                                            {song.genre && (
                                                <span className="text-gray-500">{song.genre}</span>
                                            )}
                                        </div>
                                        <div className="text-xs text-gray-500 mt-1">
                                            Modified: {formatDate(song.updatedAt)}
                                        </div>
                                        {song.tags && song.tags.length > 0 && (
                                            <div className="flex flex-wrap gap-1 mt-2">
                                                {song.tags.map((tag, index) => (
                                                    <span
                                                        key={index}
                                                        className="px-2 py-1 bg-gray-700 text-xs rounded"
                                                    >
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                    <div className="flex space-x-1 ml-2">
                                        <button
                                            onClick={(e) => handleEditSong(song, e)}
                                            className="p-1 text-gray-400 hover:text-white"
                                            title="Edit Song"
                                        >
                                            ✏️
                                        </button>
                                        <button
                                            onClick={(e) => handleExportSong(song.id, e)}
                                            className="p-1 text-gray-400 hover:text-white"
                                            title="Export Song"
                                        >
                                            ↓
                                        </button>
                                        <button
                                            onClick={(e) => handleDeleteSong(song.id, e)}
                                            className="p-1 text-gray-400 hover:text-red-400"
                                            title="Delete Song"
                                        >
                                            🗑
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Import Dialog */}
            {showImportDialog && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-gray-800 rounded-lg p-6 w-96 max-w-full mx-4">
                        <h3 className="text-lg font-bold mb-4">Import Song</h3>
                        <textarea
                            value={importData}
                            onChange={(e) => setImportData(e.target.value)}
                            placeholder="Paste song JSON data here..."
                            className="w-full h-32 p-3 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-performia-cyan focus:outline-none"
                        />
                        <div className="flex justify-end space-x-2 mt-4">
                            <button
                                onClick={() => setShowImportDialog(false)}
                                className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleImportSong}
                                className="px-4 py-2 bg-performia-cyan text-black rounded font-medium hover:bg-cyan-300"
                            >
                                Import
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Edit Dialog */}
            {editingSong && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-gray-800 rounded-lg p-6 w-96 max-w-full mx-4">
                        <h3 className="text-lg font-bold mb-4">Edit Song Metadata</h3>
                        <div className="mb-4">
                            <h4 className="font-semibold text-performia-cyan mb-2">
                                {editingSong.songMap.title} - {editingSong.songMap.artist}
                            </h4>
                        </div>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">Genre</label>
                                <input
                                    type="text"
                                    value={editForm.genre}
                                    onChange={(e) => setEditForm({...editForm, genre: e.target.value})}
                                    placeholder="e.g., Rock, Pop, Jazz"
                                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-performia-cyan focus:outline-none"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Difficulty</label>
                                <select
                                    value={editForm.difficulty}
                                    onChange={(e) => setEditForm({...editForm, difficulty: e.target.value as any})}
                                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:border-performia-cyan focus:outline-none"
                                >
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">Tags (comma-separated)</label>
                                <input
                                    type="text"
                                    value={editForm.tags}
                                    onChange={(e) => setEditForm({...editForm, tags: e.target.value})}
                                    placeholder="e.g., classic, rock, easy"
                                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-performia-cyan focus:outline-none"
                                />
                            </div>
                        </div>
                        <div className="flex justify-end space-x-2 mt-6">
                            <button
                                onClick={handleCancelEdit}
                                className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSaveEdit}
                                className="px-4 py-2 bg-performia-cyan text-black rounded font-medium hover:bg-cyan-300"
                            >
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LibraryView;