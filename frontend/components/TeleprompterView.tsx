import React, { useRef, useEffect } from 'react';
import { SongMap, ChordDisplayMode } from '../types';
import { useSongPlayer } from '../hooks/useSongPlayer';
import { transposeChord } from '../utils/musicUtils';
import ChordDiagram from './ChordDiagram';

interface TeleprompterViewProps {
    songMap: SongMap;
    transpose: number;
    capo: number;
    chordDisplay: ChordDisplayMode;
    diagramVisibility: { [key: string]: boolean };
    onToggleDiagram: (key: string) => void;
}

const TeleprompterView: React.FC<TeleprompterViewProps> = ({ songMap, transpose, capo, diagramVisibility, onToggleDiagram }) => {
    const { activeLineIndex, activeSyllableIndex, elapsed, isPlaying } = useSongPlayer(songMap);
    const lyricsContainerRef = useRef<HTMLDivElement>(null);
    const lineRefs = useRef<(HTMLDivElement | null)[]>([]);

    useEffect(() => {
        if (activeLineIndex !== -1 && lyricsContainerRef.current && lineRefs.current[activeLineIndex]) {
            const container = lyricsContainerRef.current;
            const activeLineEl = lineRefs.current[activeLineIndex];
            
            if (container && activeLineEl) {
                const containerRect = container.parentElement!.getBoundingClientRect();
                const activeLineRect = activeLineEl.getBoundingClientRect();
                
                const scrollOffset = activeLineRect.top - containerRect.top - (containerRect.height / 2) + (activeLineRect.height / 2);
                
                const currentTransform = new DOMMatrix(getComputedStyle(container).transform);
                const currentTranslateY = currentTransform.m42;
                
                container.style.transform = `translateY(${currentTranslateY - scrollOffset}px)`;
            }
        }
    }, [activeLineIndex]);

    const allLines = songMap.sections.flatMap(s => s.lines);

    return (
        <main id="teleprompter-view" className="flex-grow flex items-center justify-center text-center overflow-hidden">
            <div 
                ref={lyricsContainerRef} 
                className="space-y-8 leading-tight transition-transform duration-500 ease-in-out"
            >
                {allLines.map((line, lineIndex) => (
                    <div
                        key={lineIndex}
                        ref={el => lineRefs.current[lineIndex] = el}
                        className={`lyric-line ${activeLineIndex === lineIndex ? 'active-line' : ''} ${lineIndex < activeLineIndex ? 'opacity-30' : ''}`}
                    >
                        <div className="syllables-wrapper">
                            {line.syllables.map((syllable, syllableIndex) => {
                                const key = `${songMap.sections.findIndex(s => s.lines.includes(line))}-${lineIndex}-${syllableIndex}`;
                                const isActive = activeLineIndex === lineIndex && activeSyllableIndex === syllableIndex;
                                const isSung = syllable.startTime < elapsed;
                                const progress = isActive ? Math.min(1, (elapsed - syllable.startTime) / syllable.duration) : (isSung ? 1 : 0);
                                const displayedChord = transposeChord(syllable.chord, transpose - capo);

                                return (
                                    <span
                                        key={syllableIndex}
                                        className={`syllable-container ${isActive ? 'active-word' : ''} ${diagramVisibility[key] ? 'show-diagram' : ''}`}
                                        onClick={() => syllable.chord && onToggleDiagram(key)}
                                    >
                                        {syllable.chord && displayedChord && (
                                            <div className="chord">
                                                <span className="chord-name">{displayedChord}</span>
                                                <div className="chord-diagram-wrapper">
                                                   <ChordDiagram chordName={displayedChord} />
                                                </div>
                                            </div>
                                        )}
                                        <span className={`syllable ${isSung ? 'sung' : ''}`}>
                                            {syllable.text}
                                            <span className="syllable-wipe" style={{ width: `${progress * 100}%` }}>
                                                {syllable.text}
                                            </span>
                                        </span>
                                        <div className="syllable-progress-container">
                                            <div className="syllable-progress-fill" style={{ width: `${progress * 100}%` }}></div>
                                        </div>
                                    </span>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>
        </main>
    );
};

export default TeleprompterView;
