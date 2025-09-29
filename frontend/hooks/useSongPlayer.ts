import { useState, useEffect, useRef, useMemo } from 'react';
import { SongMap } from '../types';

export const useSongPlayer = (songMap: SongMap) => {
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
    }, [songMap, allSyllables, lastSyllable]);

    return { isPlaying, elapsed, activeLineIndex, activeSyllableIndex };
};
