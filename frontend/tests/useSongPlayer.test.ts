import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useSongPlayer } from '../hooks/useSongPlayer';
import { SongMap } from '../types';

const mockSongMap: SongMap = {
    id: 'test-song',
    title: 'Test Song',
    artist: 'Test Artist',
    duration: 10,
    sections: [
        {
            name: 'Verse 1',
            startTime: 0,
            lines: [
                {
                    syllables: [
                        {
                            text: 'Test',
                            startTime: 1.0,
                            duration: 0.5,
                        },
                        {
                            text: 'song',
                            startTime: 1.5,
                            duration: 0.5,
                        },
                    ],
                },
            ],
        },
    ],
};

describe('useSongPlayer', () => {
    beforeEach(() => {
        vi.useFakeTimers();
    });

    afterEach(() => {
        vi.restoreAllMocks();
        vi.useRealTimers();
    });

    describe('Enabled Mode', () => {
        it('should initialize with default state', () => {
            const { result } = renderHook(() => useSongPlayer(mockSongMap, true));

            expect(result.current.isPlaying).toBe(false);
            expect(result.current.elapsed).toBe(0);
            expect(result.current.activeLineIndex).toBe(-1);
            expect(result.current.activeSyllableIndex).toBe(-1);
        });

        it('should start playing after 2 second delay when enabled=true', () => {
            const { result } = renderHook(() => useSongPlayer(mockSongMap, true));

            expect(result.current.isPlaying).toBe(false);

            // Fast-forward time by 2 seconds to trigger the timeout
            act(() => {
                vi.advanceTimersByTime(2000);
            });

            // Should now be playing (timeout fired)
            expect(result.current.isPlaying).toBe(true);
        });

        it('should default to enabled=true when parameter not provided', () => {
            const { result } = renderHook(() => useSongPlayer(mockSongMap));

            expect(result.current.isPlaying).toBe(false);

            act(() => {
                vi.advanceTimersByTime(2000);
            });

            expect(result.current.isPlaying).toBe(true);
        });
    });

    describe('Disabled Mode', () => {
        it('should not play when enabled=false', () => {
            const { result } = renderHook(() => useSongPlayer(mockSongMap, false));

            expect(result.current.isPlaying).toBe(false);
            expect(result.current.elapsed).toBe(0);
            expect(result.current.activeLineIndex).toBe(-1);
            expect(result.current.activeSyllableIndex).toBe(-1);

            // Advance time
            act(() => {
                vi.advanceTimersByTime(5000);
            });

            // Should still not be playing
            expect(result.current.isPlaying).toBe(false);
            expect(result.current.elapsed).toBe(0);
        });

        it('should reset state when switching from enabled to disabled', () => {
            const { result, rerender } = renderHook(
                ({ enabled }) => useSongPlayer(mockSongMap, enabled),
                { initialProps: { enabled: true } }
            );

            // Start playback
            act(() => {
                vi.advanceTimersByTime(2000);
            });

            expect(result.current.isPlaying).toBe(true);

            // Disable the hook
            rerender({ enabled: false });

            // Should reset state immediately
            expect(result.current.isPlaying).toBe(false);
            expect(result.current.elapsed).toBe(0);
            expect(result.current.activeLineIndex).toBe(-1);
            expect(result.current.activeSyllableIndex).toBe(-1);
        });

        it('should start playing when switching from disabled to enabled', () => {
            const { result, rerender } = renderHook(
                ({ enabled }) => useSongPlayer(mockSongMap, enabled),
                { initialProps: { enabled: false } }
            );

            expect(result.current.isPlaying).toBe(false);

            // Enable the hook
            rerender({ enabled: true });

            // Advance time to start playback
            act(() => {
                vi.advanceTimersByTime(2000);
            });

            expect(result.current.isPlaying).toBe(true);
        });
    });

    describe('Cleanup', () => {
        it('should cleanup animation frame on unmount during playback', () => {
            const cancelAnimationFrameSpy = vi.spyOn(window, 'cancelAnimationFrame');
            const { result, unmount } = renderHook(() => useSongPlayer(mockSongMap, true));

            // Start playback to ensure animation frame is created
            act(() => {
                vi.advanceTimersByTime(2000);
            });

            expect(result.current.isPlaying).toBe(true);

            unmount();

            // Should have called cancelAnimationFrame
            expect(cancelAnimationFrameSpy).toHaveBeenCalled();
        });

        it('should cleanup timeout on unmount', () => {
            const clearTimeoutSpy = vi.spyOn(window, 'clearTimeout');
            const { unmount } = renderHook(() => useSongPlayer(mockSongMap, true));

            unmount();

            // Should have called clearTimeout
            expect(clearTimeoutSpy).toHaveBeenCalled();
        });
    });
});
