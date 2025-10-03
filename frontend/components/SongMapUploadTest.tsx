import React, { useRef } from 'react';
import { useSongMapUpload } from '../hooks/useSongMapUpload';
import { libraryService } from '../services/libraryService';

/**
 * Test component for Song Map upload functionality
 *
 * This component demonstrates how to use the useSongMapUpload hook
 * to upload audio files and generate Song Maps.
 *
 * Features:
 * - File selection via button or drag-and-drop
 * - Real-time progress updates
 * - Error handling
 * - Automatic library integration
 */
export const SongMapUploadTest: React.FC = () => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const {
        uploadSong,
        cancelUpload,
        reset,
        isUploading,
        progress,
        songMap,
        backendSongMap,
        error,
        jobId,
    } = useSongMapUpload();

    const handleFileSelect = async (file: File) => {
        if (!file) return;

        // Extract title from filename (remove extension)
        const title = file.name.replace(/\.[^/.]+$/, '');

        await uploadSong(file, {
            title,
            artist: 'Unknown Artist',
        });
    };

    const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            handleFileSelect(file);
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    const handleAddToLibrary = () => {
        if (songMap) {
            libraryService.addSong(songMap, {
                tags: ['uploaded', 'generated'],
            });
            alert('Song added to library!');
            reset();
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('audio/')) {
            handleFileSelect(file);
        } else {
            alert('Please drop an audio file');
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-6 space-y-6">
            <h1 className="text-3xl font-bold">Song Map Upload Test</h1>

            {/* Upload Area */}
            <div
                className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="audio/*"
                    onChange={handleFileInputChange}
                    className="hidden"
                    disabled={isUploading}
                />

                {!isUploading && !songMap && (
                    <div className="space-y-4">
                        <div className="text-gray-600">
                            Drag and drop an audio file here, or
                        </div>
                        <button
                            onClick={handleButtonClick}
                            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                        >
                            Select Audio File
                        </button>
                        <div className="text-sm text-gray-500">
                            Supported formats: WAV, MP3, FLAC, etc.
                        </div>
                    </div>
                )}

                {isUploading && (
                    <div className="space-y-4">
                        <div className="text-lg font-semibold">{progress.message}</div>
                        <div className="w-full bg-gray-200 rounded-full h-4">
                            <div
                                className="bg-blue-600 h-4 rounded-full transition-all duration-300"
                                style={{ width: `${progress.progress}%` }}
                            />
                        </div>
                        <div className="text-sm text-gray-600">
                            {progress.progress}% complete
                            {progress.estimatedRemaining && (
                                <span> • ~{Math.round(progress.estimatedRemaining)}s remaining</span>
                            )}
                        </div>
                        <button
                            onClick={cancelUpload}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                        >
                            Cancel
                        </button>
                    </div>
                )}

                {songMap && (
                    <div className="space-y-4">
                        <div className="text-green-600 font-semibold text-xl">
                            ✓ Song Map Generated!
                        </div>
                        <div className="space-y-2">
                            <button
                                onClick={handleAddToLibrary}
                                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                            >
                                Add to Library
                            </button>
                            <button
                                onClick={reset}
                                className="ml-4 px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition"
                            >
                                Upload Another
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <div className="font-semibold text-red-800">Error</div>
                    <div className="text-red-700">{error}</div>
                    <button
                        onClick={reset}
                        className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
                    >
                        Try Again
                    </button>
                </div>
            )}

            {/* Job Info */}
            {jobId && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <div className="font-semibold">Job ID</div>
                    <div className="font-mono text-sm">{jobId}</div>
                </div>
            )}

            {/* Song Map Preview */}
            {songMap && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <h2 className="text-xl font-bold mb-4">Song Map Preview</h2>
                    <div className="space-y-2">
                        <div>
                            <span className="font-semibold">Title:</span> {songMap.title}
                        </div>
                        <div>
                            <span className="font-semibold">Artist:</span> {songMap.artist}
                        </div>
                        <div>
                            <span className="font-semibold">Key:</span> {songMap.key}
                        </div>
                        <div>
                            <span className="font-semibold">BPM:</span> {songMap.bpm}
                        </div>
                        <div>
                            <span className="font-semibold">Sections:</span> {songMap.sections.length}
                        </div>
                    </div>
                </div>
            )}

            {/* Backend Song Map Preview */}
            {backendSongMap && (
                <details className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <summary className="font-semibold cursor-pointer">
                        Backend Song Map (Raw)
                    </summary>
                    <pre className="mt-4 p-4 bg-gray-900 text-green-400 rounded overflow-x-auto text-xs">
                        {JSON.stringify(backendSongMap, null, 2)}
                    </pre>
                </details>
            )}

            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">Instructions</h3>
                <ol className="list-decimal list-inside space-y-1 text-blue-800 text-sm">
                    <li>Make sure the backend API is running at http://localhost:8000</li>
                    <li>Select or drag an audio file (test_music.wav recommended)</li>
                    <li>Wait for the Song Map to be generated</li>
                    <li>Add the song to your library or upload another file</li>
                </ol>
            </div>
        </div>
    );
};

export default SongMapUploadTest;
