import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { produce } from 'immer';
import { SongMap, ChordDisplayMode } from './types';
import { initialSongMap } from './data/mockSong';
import Header from './components/Header';
import TeleprompterView from './components/TeleprompterView';
import BlueprintView from './components/BlueprintView';
import SettingsPanel from './components/SettingsPanel';
import { SoundwaveIcon } from './components/icons/Icons';
import { libraryService } from './services/libraryService';
import { useSongMapUpload } from './hooks/useSongMapUpload';

const App: React.FC = () => {
    const [songMap, setSongMap] = useState<SongMap>(initialSongMap);
    const [view, setView] = useState<'teleprompter' | 'blueprint'>('teleprompter');
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isLibraryInitialized, setIsLibraryInitialized] = useState(false);
    const [showUploadUI, setShowUploadUI] = useState(false);

    // Song Map upload hook
    const { uploadSong, isUploading, progress, songMap: uploadedSongMap, error, reset } = useSongMapUpload();
    
    // Settings State
    const [chordDisplay, setChordDisplay] = useState<ChordDisplayMode>('names');
    const [fontSize, setFontSize] = useState(100); // Percentage
    const [transpose, setTranspose] = useState(0);
    const [capo, setCapo] = useState(0);
    const [diagramVisibility, setDiagramVisibility] = useState<{ [key: string]: boolean }>({});

    useEffect(() => {
        document.documentElement.style.setProperty('--base-font-size', `${3.0 * (fontSize / 100)}rem`);
    }, [fontSize]);

    // Initialize library with demo song on first load
    useEffect(() => {
        if (!isLibraryInitialized && libraryService.getCount() === 0) {
            libraryService.addSong(initialSongMap, {
                tags: ['demo', 'classic', 'beatles'],
                genre: 'Rock',
                difficulty: 'intermediate'
            });
            setIsLibraryInitialized(true);
        }
    }, [isLibraryInitialized]);

    // Handle uploaded Song Map
    useEffect(() => {
        if (uploadedSongMap && progress.status === 'complete') {
            setSongMap(uploadedSongMap);
            setShowUploadUI(false);
            setView('teleprompter');

            // Add to library
            libraryService.addSong(uploadedSongMap, {
                tags: ['uploaded'],
                genre: 'Unknown',
                difficulty: 'intermediate'
            });
        }
    }, [uploadedSongMap, progress.status]);
    
    const handleSongMapChange = useCallback((newSongMap: SongMap) => {
        setSongMap(newSongMap);
    }, []);
    
    const handleSongSelect = useCallback((newSongMap: SongMap) => {
        setSongMap(newSongMap);
        setIsSettingsOpen(false);
        setView('teleprompter');
    }, []);

    const handleToggleDiagram = (key: string) => {
        setDiagramVisibility(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const fileName = file.name.replace(/\.[^/.]+$/, '');
            await uploadSong(file, {
                title: fileName,
                artist: 'Unknown Artist'
            });
        }
    };

    const handleUploadClick = () => {
        setShowUploadUI(true);
    };

    // Optimization 5: Memoize class name calculation
    const appContainerClasses = useMemo(() => {
        let classes = 'flex flex-col h-screen';
        if (chordDisplay === 'diagrams') classes += ' show-diagrams';
        if (chordDisplay === 'off') classes += ' hide-chords';
        return classes;
    }, [chordDisplay]);

    return (
        <div className={appContainerClasses}>
            <Header
                songTitle={songMap.title}
                artistName={songMap.artist}
                onSettingsClick={() => setIsSettingsOpen(true)}
                onTitleClick={() => setView('blueprint')}
                onPlayClick={() => setView('teleprompter')}
                onUploadClick={handleUploadClick}
                currentView={view}
            />

            {showUploadUI && !isUploading ? (
                <main className="flex-grow flex items-center justify-center">
                    <div className="text-center space-y-6">
                        <h2 className="text-3xl font-bold text-white">Upload a Song</h2>
                        <p className="text-gray-400">Choose an audio file to generate a Song Map</p>
                        <div className="flex flex-col items-center gap-4">
                            <label className="cursor-pointer bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-8 py-4 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl">
                                Choose Audio File
                                <input
                                    type="file"
                                    accept="audio/*,.wav,.mp3,.m4a,.flac"
                                    onChange={handleFileUpload}
                                    className="hidden"
                                />
                            </label>
                            <button
                                onClick={() => setShowUploadUI(false)}
                                className="text-gray-400 hover:text-white transition-colors"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </main>
            ) : isUploading ? (
                <main className="flex-grow flex items-center justify-center">
                    <div className="text-center space-y-6 max-w-md w-full px-4">
                        <h2 className="text-3xl font-bold text-white">
                            {progress.message || 'Processing...'}
                        </h2>

                        <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
                            <div
                                className="bg-gradient-to-r from-blue-500 to-purple-500 h-full transition-all duration-300 ease-out"
                                style={{ width: `${progress.progress}%` }}
                            />
                        </div>

                        <div className="flex justify-between text-sm text-gray-400">
                            <span>{progress.progress}%</span>
                            {progress.estimatedRemaining && (
                                <span>~{Math.round(progress.estimatedRemaining)}s remaining</span>
                            )}
                        </div>

                        {error && (
                            <div className="mt-4 p-4 bg-red-900/20 border border-red-500 rounded-lg">
                                <p className="text-red-400">{error}</p>
                                <button
                                    onClick={() => {
                                        reset();
                                        setShowUploadUI(true);
                                    }}
                                    className="mt-2 text-white hover:text-gray-300 transition-colors"
                                >
                                    Try Again
                                </button>
                            </div>
                        )}
                    </div>
                </main>
            ) : view === 'teleprompter' ? (
                <TeleprompterView
                    songMap={songMap}
                    transpose={transpose}
                    capo={capo}
                    chordDisplay={chordDisplay}
                    diagramVisibility={diagramVisibility}
                    onToggleDiagram={handleToggleDiagram}
                />
            ) : (
                <BlueprintView
                    songMap={songMap}
                    onSongMapChange={handleSongMapChange}
                />
            )}
            
            <footer className="w-full px-6 py-4 footer-container shrink-0 z-10">
                <div className="relative flex justify-center items-center h-8">
                    <SoundwaveIcon />
                </div>
            </footer>

            <SettingsPanel 
                isOpen={isSettingsOpen}
                onClose={() => setIsSettingsOpen(false)}
                chordDisplay={chordDisplay}
                onChordDisplayChange={setChordDisplay}
                fontSize={fontSize}
                onFontSizeChange={setFontSize}
                transpose={transpose}
                onTransposeChange={setTranspose}
                capo={capo}
                onCapoChange={setCapo}
                currentSong={songMap}
                onSongSelect={handleSongSelect}
            />
        </div>
    );
};

export default App;
