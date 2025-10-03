import { useState, useEffect, useRef, useMemo } from 'react';
import { SongMap } from '../types';

/**
 * Hook for demo mode auto-playback simulation
 *
 * @param songMap - The song map to play
 * @param enabled - Whether the demo player should run (default: true)
 * @returns Player state including active line/syllable and elapsed time
 */
export const useSongPlayer = (songMap: SongMap, enabled: boolean = true) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [elapsed, setElapsed] = useState(0);
    const [activeLineIndex, setActiveLineIndex] = useState(-1);
    const [activeSyllableIndex, setActiveSyllableIndex] = useState(-1);

    const animationFrameId = useRef<number>();
    const startTimeRef = useRef<number>(0);

    const allSyllables = useMemo(() =>
        songMap.sections.flatMap((section, sectionIndex) =>
            section.lines.flatMap((line, lineIndex) =>
                line.syllables.map((syllable, syllableIndex) => ({
                    ...syllable,
                    sectionIndex,
                    lineIndex,
                    syllableIndex
                }))
            )
        ), [songMap]);

    const lastSyllable = allSyllables[allSyllables.length - 1];

    useEffect(() => {
        // Exit early if disabled
        if (!enabled) {
            setIsPlaying(false);
            setElapsed(0);
            setActiveLineIndex(-1);
            setActiveSyllableIndex(-1);
            return;
        }
        const startPerformance = () => {
            startTimeRef.current = performance.now();
            setIsPlaying(true);
            animate(startTimeRef.current);
        };
        
        const animate = (time: number) => {
            const elapsedTime = (time - startTimeRef.current) / 1000;
            setElapsed(elapsedTime);
            
            const activeSyllable = allSyllables.find(s => 
                elapsedTime >= s.startTime && elapsedTime < s.startTime + s.duration
            );

            if (activeSyllable) {
                setActiveLineIndex(activeSyllable.lineIndex);
                setActiveSyllableIndex(activeSyllable.syllableIndex);
            } else {
                // Find last sung syllable to keep highlighting
                const lastSung = [...allSyllables].reverse().find(s => elapsedTime >= s.startTime);
                if (lastSung) {
                    setActiveLineIndex(lastSung.lineIndex);
                    setActiveSyllableIndex(lastSung.syllableIndex);
                }
            }

            if (lastSyllable && elapsedTime > lastSyllable.startTime + lastSyllable.duration + 2) {
                startPerformance(); // Restart
                return;
            }

            animationFrameId.current = requestAnimationFrame(animate);
        };

        const timeoutId = setTimeout(startPerformance, 2000);

        return () => {
            clearTimeout(timeoutId);
            if (animationFrameId.current) {
                cancelAnimationFrame(animationFrameId.current);
            }
            setIsPlaying(false);
        };
    }, [songMap, allSyllables, lastSyllable, enabled]);

    return { isPlaying, elapsed, activeLineIndex, activeSyllableIndex };
};
