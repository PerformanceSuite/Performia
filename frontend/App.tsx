import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { produce } from 'immer';
import { SongMap, ChordDisplayMode } from './types';
import { initialSongMap } from './data/mockSong';
import Header from './components/Header';
import TeleprompterView from './components/TeleprompterView';
import FullChart from './components/FullChart';
import SettingsPanel from './components/SettingsPanel';
import SongMapDemo from './components/SongMapDemo';
import { SoundwaveIcon } from './components/icons/Icons';
import { libraryService } from './services/libraryService';
import { useSongMapUpload } from './hooks/useSongMapUpload';

const App: React.FC = () => {
    const [songMap, setSongMap] = useState<SongMap>(initialSongMap);
    const [currentJobId, setCurrentJobId] = useState<string | undefined>(undefined);
    const [view, setView] = useState<'teleprompter' | 'fullchart' | 'demo'>('teleprompter');
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isLibraryInitialized, setIsLibraryInitialized] = useState(false);
    const [showUploadUI, setShowUploadUI] = useState(false);

    // Song Map upload hook
    const { uploadSong, isUploading, progress, songMap: uploadedSongMap, error, reset, jobId: uploadJobId } = useSongMapUpload();
    
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
            setCurrentJobId(uploadJobId || undefined);
            setShowUploadUI(false);
            setView('teleprompter');

            // Add to library with jobId for audio playback
            libraryService.addSong(uploadedSongMap, {
                tags: ['uploaded'],
                genre: 'Unknown',
                difficulty: 'intermediate',
                jobId: uploadJobId || undefined
            });
        }
    }, [uploadedSongMap, progress.status, uploadJobId]);
    
    const handleSongMapChange = useCallback((newSongMap: SongMap) => {
        setSongMap(newSongMap);
    }, []);
    
    const handleSongSelect = useCallback((newSongMap: SongMap, jobId?: string) => {
        setSongMap(newSongMap);
        setCurrentJobId(jobId);
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
                onTitleClick={() => setView('fullchart')}
                onPlayClick={() => setView('teleprompter')}
                onUploadClick={handleUploadClick}
                onDemoClick={() => setView('demo')}
                currentView={view}
            />

            {showUploadUI && !isUploading ? (
                <main className="flex-grow flex items-center justify-center px-8 py-12" role="main" aria-label="Upload interface">
                    <div className="text-center max-w-2xl w-full">
                        <div className="space-y-8">
                            <div className="space-y-4">
                                <h2 className="text-5xl font-bold text-white tracking-tight">
                                    Upload a Song
                                </h2>
                                <p className="text-lg text-gray-300 leading-relaxed">
                                    Choose an audio file to generate an interactive Song Map with real-time analysis
                                </p>
                            </div>

                            <div className="flex flex-col items-center gap-6 mt-12">
                                <label
                                    className="cursor-pointer bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-12 py-5 rounded-xl font-semibold text-lg transition-all duration-200 shadow-2xl hover:shadow-3xl hover:scale-105 focus-within:ring-4 focus-within:ring-blue-400 focus-within:ring-opacity-50"
                                    style={{ minHeight: '44px', minWidth: '44px' }}
                                    aria-label="Choose audio file for upload"
                                >
                                    <span className="flex items-center gap-3">
                                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>
                                        Choose Audio File
                                    </span>
                                    <input
                                        type="file"
                                        accept="audio/*,.wav,.mp3,.m4a,.flac"
                                        onChange={handleFileUpload}
                                        className="hidden"
                                        aria-label="Audio file input"
                                    />
                                </label>

                                <div className="text-sm text-gray-400 space-y-2">
                                    <p className="font-medium">Supported formats:</p>
                                    <p>WAV, MP3, M4A, FLAC</p>
                                </div>

                                <button
                                    onClick={() => setShowUploadUI(false)}
                                    className="mt-4 px-8 py-3 text-gray-300 hover:text-white transition-colors duration-200 rounded-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-400"
                                    style={{ minHeight: '44px', minWidth: '44px' }}
                                    aria-label="Cancel upload"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </main>
            ) : isUploading ? (
                <main className="flex-grow flex items-center justify-center px-8 py-12" role="main" aria-label="Upload progress">
                    <div className="text-center max-w-2xl w-full">
                        <div className="space-y-8">
                            <h2 className="text-4xl font-bold text-white tracking-tight" aria-live="polite">
                                {progress.message || 'Processing...'}
                            </h2>

                            <div
                                className="w-full bg-gray-800 rounded-xl h-6 overflow-hidden shadow-inner"
                                role="progressbar"
                                aria-valuenow={progress.progress}
                                aria-valuemin={0}
                                aria-valuemax={100}
                                aria-label={`Upload progress: ${progress.progress}%`}
                            >
                                <div
                                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-full transition-all duration-300 ease-out"
                                    style={{ width: `${progress.progress}%` }}
                                />
                            </div>

                            <div className="flex justify-between text-base text-gray-300 px-2" aria-live="polite">
                                <span className="font-medium">{progress.progress}%</span>
                                {progress.estimatedRemaining && (
                                    <span>~{Math.round(progress.estimatedRemaining)}s remaining</span>
                                )}
                            </div>

                            {error && (
                                <div
                                    className="mt-8 p-6 bg-red-900/20 border-2 border-red-500 rounded-xl"
                                    role="alert"
                                    aria-live="assertive"
                                >
                                    <p className="text-red-300 text-lg mb-4">{error}</p>
                                    <button
                                        onClick={() => {
                                            reset();
                                            setShowUploadUI(true);
                                        }}
                                        className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 font-semibold focus:outline-none focus:ring-2 focus:ring-red-400"
                                        style={{ minHeight: '44px', minWidth: '44px' }}
                                        aria-label="Try uploading again"
                                    >
                                        Try Again
                                    </button>
                                </div>
                            )}
                        </div>
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
                    jobId={currentJobId}
                />
            ) : view === 'demo' ? (
                <SongMapDemo />
            ) : (
                <FullChart
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
