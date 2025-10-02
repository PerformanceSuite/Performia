import React, { useRef, useEffect, useMemo, useCallback, useState } from 'react';
import { SongMap, ChordDisplayMode } from '../types';
import { useSongPlayer } from '../hooks/useSongPlayer';
import { transposeChord } from '../utils/musicUtils';
import ChordDiagram from './ChordDiagram';
import AudioPlayer from './AudioPlayer';
import StemSelector, { StemType } from './StemSelector';

interface TeleprompterViewProps {
    songMap: SongMap;
    transpose: number;
    capo: number;
    chordDisplay: ChordDisplayMode;
    diagramVisibility: { [key: string]: boolean };
    onToggleDiagram: (key: string) => void;
    jobId?: string;  // Optional job ID for audio playback
}

const TeleprompterView: React.FC<TeleprompterViewProps> = React.memo(({ songMap, transpose, capo, diagramVisibility, onToggleDiagram, jobId }) => {
    const { activeLineIndex, activeSyllableIndex, elapsed, isPlaying } = useSongPlayer(songMap);
    const lyricsContainerRef = useRef<HTMLDivElement>(null);
    const lineRefs = useRef<(HTMLDivElement | null)[]>([]);

    // Audio playback state
    const [audioCurrentTime, setAudioCurrentTime] = useState(0);
    const [audioUrl, setAudioUrl] = useState<string>('');
    const [isAudioPlaying, setIsAudioPlaying] = useState(false);
    const [showAudioControls, setShowAudioControls] = useState(false);

    // Initialize audio URL when jobId is available
    useEffect(() => {
        if (jobId) {
            setAudioUrl(`http://localhost:8000/api/audio/${jobId}/original`);
            setShowAudioControls(true);
        } else {
            // For demo mode, still show controls but without audio URL
            setShowAudioControls(false);
        }
    }, [jobId]);

    // Find active syllable based on audio playback time
    const findActiveSyllable = useCallback((time: number): {
        sectionIdx: number;
        lineIdx: number;
        syllableIdx: number;
    } | null => {
        for (let sIdx = 0; sIdx < songMap.sections.length; sIdx++) {
            const section = songMap.sections[sIdx];
            for (let lIdx = 0; lIdx < section.lines.length; lIdx++) {
                const line = section.lines[lIdx];
                for (let sylIdx = 0; sylIdx < line.syllables.length; sylIdx++) {
                    const syllable = line.syllables[sylIdx];
                    if (time >= syllable.startTime &&
                        time < syllable.startTime + syllable.duration) {
                        return { sectionIdx: sIdx, lineIdx: lIdx, syllableIdx: sylIdx };
                    }
                }
            }
        }
        return null;
    }, [songMap]);

    // Handle audio time updates
    const handleAudioTimeUpdate = useCallback((time: number) => {
        setAudioCurrentTime(time);
        // The syllable highlighting will use this time in the render
    }, []);

    const handleStemChange = useCallback((url: string, stemType: StemType) => {
        setAudioUrl(url);
    }, []);

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

    // Optimization 2: Memoize allLines calculation
    const allLines = useMemo(() =>
        songMap.sections.flatMap(s => s.lines),
        [songMap]
    );

    // Optimization 4: Pre-calculate all transposed chords once
    const transposedChords = useMemo(() => {
        const chords: Record<string, string> = {};
        allLines.forEach(line =>
            line.syllables.forEach(syl => {
                if (syl.chord && !chords[syl.chord]) {
                    chords[syl.chord] = transposeChord(syl.chord, transpose - capo);
                }
            })
        );
        return chords;
    }, [allLines, transpose, capo]);

    // Optimization 3: Memoize ref callback creator
    const setLineRef = useCallback((index: number) => (el: HTMLDivElement | null) => {
        lineRefs.current[index] = el;
    }, []);

    // Calculate active syllable from audio time
    const activeSyllableFromAudio = useMemo(() => {
        if (isAudioPlaying && audioCurrentTime > 0) {
            return findActiveSyllable(audioCurrentTime);
        }
        return null;
    }, [isAudioPlaying, audioCurrentTime, findActiveSyllable]);

    // Use audio time for highlighting when audio is playing, otherwise use simulated time
    const currentTime = isAudioPlaying ? audioCurrentTime : elapsed;
    const currentActiveLineIndex = isAudioPlaying && activeSyllableFromAudio
        ? activeSyllableFromAudio.lineIdx
        : activeLineIndex;

    return (
        <div className="flex flex-col h-full">
            {/* Audio Controls - Fixed at top when available */}
            {jobId && audioUrl ? (
                <div className="p-4 bg-gray-900 border-b border-gray-700">
                    <div className="mb-3">
                        <StemSelector
                            jobId={jobId}
                            onStemChange={handleStemChange}
                        />
                    </div>
                    <AudioPlayer
                        audioUrl={audioUrl}
                        onTimeUpdate={handleAudioTimeUpdate}
                        onPlayStateChange={setIsAudioPlaying}
                    />
                </div>
            ) : (
                <div className="p-4 bg-gray-900 border-b border-gray-700">
                    <div className="text-center text-gray-400 py-2">
                        <p className="text-sm">Audio playback available for uploaded songs</p>
                        <p className="text-xs mt-1">Upload a song to enable real-time audio synchronization</p>
                    </div>
                </div>
            )}

            {/* Teleprompter View */}
            <main id="teleprompter-view" className="flex-grow flex items-center justify-center text-center overflow-hidden">
                <div
                    ref={lyricsContainerRef}
                    className="space-y-8 leading-tight transition-transform duration-500 ease-in-out"
                >
                    {allLines.map((line, lineIndex) => (
                        <div
                            key={lineIndex}
                            ref={setLineRef(lineIndex)}
                            className={`lyric-line ${currentActiveLineIndex === lineIndex ? 'active-line' : ''} ${lineIndex < currentActiveLineIndex ? 'opacity-30' : ''}`}
                        >
                            <div className="syllables-wrapper">
                                {line.syllables.map((syllable, syllableIndex) => {
                                    const key = `${songMap.sections.findIndex(s => s.lines.includes(line))}-${lineIndex}-${syllableIndex}`;

                                    // Determine if this syllable is active based on audio or simulated time
                                    const isActive = isAudioPlaying && activeSyllableFromAudio
                                        ? activeSyllableFromAudio.lineIdx === lineIndex && activeSyllableFromAudio.syllableIdx === syllableIndex
                                        : activeLineIndex === lineIndex && activeSyllableIndex === syllableIndex;

                                    const isSung = syllable.startTime < currentTime;
                                    const progress = isActive
                                        ? Math.min(1, (currentTime - syllable.startTime) / syllable.duration)
                                        : (isSung ? 1 : 0);

                                    const displayedChord = syllable.chord ? transposedChords[syllable.chord] : null;

                                    return (
                                        <span
                                            key={syllableIndex}
                                            className={`syllable-container ${isActive ? 'active-word' : ''} ${diagramVisibility[key] ? 'show-diagram' : ''}`}
                                            onClick={() => syllable.chord && onToggleDiagram(key)}
                                        >
                                            {/* Always render chord container for consistent layout */}
                                            {syllable.chord && displayedChord ? (
                                                <div className="chord">
                                                    <span className="chord-name">{displayedChord}</span>
                                                    <div className="chord-diagram-wrapper">
                                                       <ChordDiagram chordName={displayedChord} />
                                                    </div>
                                                </div>
                                            ) : (
                                                <div className="chord chord-spacer" aria-hidden="true">
                                                    {/* Empty spacer to maintain alignment */}
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
        </div>
    );
});

export default TeleprompterView;
