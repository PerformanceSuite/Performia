import React, { useState, useEffect, useCallback } from 'react';
import { produce } from 'immer';
import { SongMap, ChordDisplayMode } from './types';
import { initialSongMap } from './data/mockSong';
import Header from './components/Header';
import TeleprompterView from './components/TeleprompterView';
import BlueprintView from './components/BlueprintView';
import SettingsPanel from './components/SettingsPanel';
import { SoundwaveIcon } from './components/icons/Icons';
import { libraryService } from './services/libraryService';

const App: React.FC = () => {
    const [songMap, setSongMap] = useState<SongMap>(initialSongMap);
    const [view, setView] = useState<'teleprompter' | 'blueprint'>('teleprompter');
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isLibraryInitialized, setIsLibraryInitialized] = useState(false);
    
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

    const getAppContainerClasses = () => {
        let classes = 'flex flex-col h-screen';
        if (chordDisplay === 'diagrams') classes += ' show-diagrams';
        if (chordDisplay === 'off') classes += ' hide-chords';
        return classes;
    }

    return (
        <div className={getAppContainerClasses()}>
            <Header 
                songTitle={songMap.title}
                artistName={songMap.artist}
                onSettingsClick={() => setIsSettingsOpen(true)}
                onTitleClick={() => setView('blueprint')}
                onPlayClick={() => setView('teleprompter')}
                currentView={view}
            />

            {view === 'teleprompter' ? (
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
