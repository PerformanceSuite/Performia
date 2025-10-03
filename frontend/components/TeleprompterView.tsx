import React, { useRef, useEffect, useMemo, useCallback, useState, useLayoutEffect } from 'react';
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
    // Only use demo mode (useSongPlayer) when there's no jobId
    const demoPlayer = useSongPlayer(songMap);
    const lyricsContainerRef = useRef<HTMLDivElement>(null);
    const lineRefs = useRef<(HTMLDivElement | null)[]>([]);
    const viewportRef = useRef<HTMLDivElement>(null);

    // Audio playback state
    const [audioCurrentTime, setAudioCurrentTime] = useState(0);
    const [audioUrl, setAudioUrl] = useState<string>('');
    const [isAudioPlaying, setIsAudioPlaying] = useState(false);
    const [showAudioControls, setShowAudioControls] = useState(false);
    const [audioError, setAudioError] = useState<string | null>(null);

    // Use demo player values only when no audio is available
    const activeLineIndex = jobId ? -1 : demoPlayer.activeLineIndex;
    const activeSyllableIndex = jobId ? -1 : demoPlayer.activeSyllableIndex;
    const elapsed = jobId ? audioCurrentTime : demoPlayer.elapsed;
    const isPlaying = jobId ? isAudioPlaying : demoPlayer.isPlaying;

    // Virtual scrolling state
    const [visibleRange, setVisibleRange] = useState({ start: 0, end: 50 });
    const BUFFER_SIZE = 10; // Lines to render above/below viewport

    // Initialize audio URL when jobId is available
    useEffect(() => {
        if (jobId) {
            // Validate jobId format (alphanumeric and hyphens only)
            if (!/^[a-zA-Z0-9-]+$/.test(jobId)) {
                console.error('Invalid jobId format:', jobId);
                setShowAudioControls(false);
                return;
            }

            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3002';
            setAudioUrl(`${apiUrl}/api/audio/${jobId}/original`);
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
        setAudioError(null);
    }, []);

    const handleAudioError = useCallback((error: string) => {
        setAudioError(error);
        console.error('Audio playback error:', error);
    }, []);

    // Auto-center active line using requestAnimationFrame for smooth 60fps
    useEffect(() => {
        let animationFrameId: number;

        const centerActiveLine = () => {
            if (activeLineIndex !== -1 && lyricsContainerRef.current && lineRefs.current[activeLineIndex]) {
                const container = lyricsContainerRef.current;
                const activeLineEl = lineRefs.current[activeLineIndex];

                if (container && activeLineEl && viewportRef.current) {
                    const viewportRect = viewportRef.current.getBoundingClientRect();
                    const activeLineRect = activeLineEl.getBoundingClientRect();

                    const scrollOffset = activeLineRect.top - viewportRect.top - (viewportRect.height / 2) + (activeLineRect.height / 2);

                    const currentTransform = new DOMMatrix(getComputedStyle(container).transform);
                    const currentTranslateY = currentTransform.m42;

                    container.style.transform = `translateY(${currentTranslateY - scrollOffset}px)`;
                }
            }
        };

        animationFrameId = requestAnimationFrame(centerActiveLine);

        return () => {
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
        };
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
        if (jobId && audioCurrentTime > 0) {
            return findActiveSyllable(audioCurrentTime);
        }
        return null;
    }, [jobId, audioCurrentTime, findActiveSyllable]);

    // Use audio time for highlighting when we have a jobId, otherwise use simulated demo time
    const currentTime = jobId ? audioCurrentTime : elapsed;
    const currentActiveLineIndex = jobId && activeSyllableFromAudio
        ? activeSyllableFromAudio.lineIdx
        : activeLineIndex;

    // Virtual scrolling: only render visible lines
    const visibleLines = useMemo(() =>
        allLines.slice(visibleRange.start, visibleRange.end),
        [allLines, visibleRange]
    );

    // Update visible range based on active line (virtual scrolling)
    useLayoutEffect(() => {
        if (currentActiveLineIndex !== -1) {
            const start = Math.max(0, currentActiveLineIndex - BUFFER_SIZE);
            const end = Math.min(allLines.length, currentActiveLineIndex + BUFFER_SIZE + 1);
            setVisibleRange({ start, end });
        }
    }, [currentActiveLineIndex, allLines.length, BUFFER_SIZE]);

    return (
        <div className="flex flex-col h-full">
            {/* Audio Controls - Fixed at top when available */}
            {jobId && audioUrl ? (
                <div className="p-4 bg-gray-900 border-b border-gray-700" role="region" aria-label="Audio controls">
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
                        onError={handleAudioError}
                    />
                </div>
            ) : (
                <div className="p-4 bg-gray-900 border-b border-gray-700" role="region" aria-label="Audio controls placeholder">
                    <div className="text-center text-gray-400 py-2">
                        <p className="text-sm">Audio playback available for uploaded songs</p>
                        <p className="text-xs mt-1">Upload a song to enable real-time audio synchronization</p>
                    </div>
                </div>
            )}

            {/* Teleprompter View */}
            <main
                ref={viewportRef}
                id="teleprompter-view"
                className="flex-grow flex items-center justify-center text-center overflow-hidden"
                role="main"
                aria-label={`Teleprompter for ${songMap.title} by ${songMap.artist}`}
                aria-live="polite"
            >
                <div
                    ref={lyricsContainerRef}
                    className="space-y-8 leading-tight transition-transform duration-500 ease-in-out"
                    style={{
                        // Add padding to account for hidden lines
                        paddingTop: `${visibleRange.start * 8}rem`,
                        paddingBottom: `${(allLines.length - visibleRange.end) * 8}rem`
                    }}
                >
                    {visibleLines.map((line, visibleIndex) => {
                        const lineIndex = visibleRange.start + visibleIndex;
                        return (
                            <div
                                key={lineIndex}
                                ref={setLineRef(lineIndex)}
                                className={`lyric-line ${currentActiveLineIndex === lineIndex ? 'active-line' : ''} ${lineIndex < currentActiveLineIndex ? 'opacity-30' : ''}`}
                                role="group"
                                aria-label={`Line ${lineIndex + 1}`}
                                aria-current={currentActiveLineIndex === lineIndex ? 'step' : undefined}
                            >
                                <div className="syllables-wrapper" role="list">
                                    {line.syllables.map((syllable, syllableIndex) => {
                                        const key = `${songMap.sections.findIndex(s => s.lines.includes(line))}-${lineIndex}-${syllableIndex}`;

                                        // Determine if this syllable is active based on audio or simulated time
                                        const isActive = jobId && activeSyllableFromAudio
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
                                                role="listitem"
                                                aria-label={syllable.chord ? `${syllable.text}, chord: ${displayedChord}` : syllable.text}
                                                aria-current={isActive ? 'step' : undefined}
                                                tabIndex={syllable.chord ? 0 : undefined}
                                                onKeyDown={(e) => {
                                                    if (syllable.chord && (e.key === 'Enter' || e.key === ' ')) {
                                                        e.preventDefault();
                                                        onToggleDiagram(key);
                                                    }
                                                }}
                                            >
                                                {/* Always render chord container for consistent layout */}
                                                {syllable.chord && displayedChord ? (
                                                    <div className="chord" role="note" aria-label={`Chord: ${displayedChord}`}>
                                                        <span className="chord-name" aria-hidden="true">{displayedChord}</span>
                                                        <div className="chord-diagram-wrapper" aria-hidden="true">
                                                           <ChordDiagram chordName={displayedChord} />
                                                        </div>
                                                    </div>
                                                ) : (
                                                    <div className="chord chord-spacer" aria-hidden="true">
                                                        {/* Empty spacer to maintain alignment */}
                                                    </div>
                                                )}
                                                <span className={`syllable ${isSung ? 'sung' : ''}`} aria-hidden="true">
                                                    {syllable.text}
                                                    <span className="syllable-wipe" style={{ width: `${progress * 100}%` }}>
                                                        {syllable.text}
                                                    </span>
                                                </span>
                                                <div className="syllable-progress-container" role="progressbar" aria-valuenow={Math.round(progress * 100)} aria-valuemin={0} aria-valuemax={100} aria-label="Syllable progress">
                                                    <div className="syllable-progress-fill" style={{ width: `${progress * 100}%` }}></div>
                                                </div>
                                            </span>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </main>
        </div>
    );
});

export default TeleprompterView;
