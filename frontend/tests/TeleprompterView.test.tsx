import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import TeleprompterView from '../components/TeleprompterView';
import { SongMap } from '../types';

// Mock the useSongPlayer hook
vi.mock('../hooks/useSongPlayer', () => ({
    useSongPlayer: vi.fn((songMap: SongMap, enabled: boolean = true) => ({
        isPlaying: enabled,
        elapsed: 0,
        activeLineIndex: enabled ? 0 : -1,
        activeSyllableIndex: enabled ? 0 : -1,
    })),
}));

// Mock AudioPlayer component
vi.mock('../components/AudioPlayer', () => ({
    default: vi.fn(({ audioUrl, onError }) => (
        <div data-testid="audio-player">
            <div data-testid="audio-url">{audioUrl}</div>
            {onError && <button onClick={() => onError('Test error')}>Trigger Error</button>}
        </div>
    )),
}));

// Mock StemSelector component
vi.mock('../components/StemSelector', () => ({
    default: vi.fn(() => <div data-testid="stem-selector">Stem Selector</div>),
}));

// Mock ChordDiagram component
vi.mock('../components/ChordDiagram', () => ({
    default: vi.fn(() => <div>Chord Diagram</div>),
}));

// Mock musicUtils to prevent errors
vi.mock('../utils/musicUtils', () => ({
    transposeChord: vi.fn((chord: string) => chord),
}));

const mockSongMap: SongMap = {
    id: 'test-song',
    title: 'Test Song',
    artist: 'Test Artist',
    duration: 180,
    sections: [
        {
            name: 'Verse 1',
            startTime: 0,
            lines: [
                {
                    syllables: [
                        {
                            text: 'Hello',
                            startTime: 0.5,
                            duration: 0.3,
                            chord: 'C',
                        },
                        {
                            text: 'world',
                            startTime: 0.8,
                            duration: 0.4,
                            chord: 'G',
                        },
                    ],
                },
            ],
        },
    ],
};

describe('TeleprompterView', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('Demo Mode (No JobId)', () => {
        it('should use demo mode when no jobId is provided', async () => {
            const useSongPlayerModule = await import('../hooks/useSongPlayer');
            const useSongPlayerMock = useSongPlayerModule.useSongPlayer as ReturnType<typeof vi.fn>;

            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                />
            );

            // Verify useSongPlayer was called with enabled=true
            expect(useSongPlayerMock).toHaveBeenCalledWith(mockSongMap, true);
        });

        it('should not show audio controls in demo mode', () => {
            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                />
            );

            expect(screen.queryByTestId('audio-player')).not.toBeInTheDocument();
            expect(screen.getByText(/Audio playback available for uploaded songs/i)).toBeInTheDocument();
        });
    });

    describe('Audio Mode (With JobId)', () => {
        it('should disable demo mode when jobId is present', async () => {
            const useSongPlayerModule = await import('../hooks/useSongPlayer');
            const useSongPlayerMock = useSongPlayerModule.useSongPlayer as ReturnType<typeof vi.fn>;

            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="test-job-123"
                />
            );

            // Verify useSongPlayer was called with enabled=false
            expect(useSongPlayerMock).toHaveBeenCalledWith(mockSongMap, false);
        });

        it('should show audio controls when jobId is provided', async () => {
            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="test-job-123"
                />
            );

            await waitFor(() => {
                expect(screen.getByTestId('audio-player')).toBeInTheDocument();
            });
        });

        it('should construct correct audio URL with jobId', async () => {
            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="abc123"
                />
            );

            await waitFor(() => {
                const audioUrl = screen.getByTestId('audio-url').textContent;
                expect(audioUrl).toContain('/api/audio/abc123/original');
            });
        });

        it('should reject invalid jobId format', () => {
            const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="../../../etc/passwd"
                />
            );

            expect(consoleSpy).toHaveBeenCalledWith('Invalid jobId format:', '../../../etc/passwd');
            expect(screen.queryByTestId('audio-player')).not.toBeInTheDocument();

            consoleSpy.mockRestore();
        });
    });

    describe('Error Handling', () => {
        it('should handle audio errors gracefully', async () => {
            const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="test-job-123"
                />
            );

            await waitFor(() => {
                const errorButton = screen.getByText('Trigger Error');
                errorButton.click();
            });

            expect(consoleSpy).toHaveBeenCalledWith('Audio playback error:', 'Test error');

            consoleSpy.mockRestore();
        });
    });

    describe('Mode Switching', () => {
        it('should switch from demo to audio mode when jobId is added', async () => {
            const useSongPlayerModule = await import('../hooks/useSongPlayer');
            const useSongPlayerMock = useSongPlayerModule.useSongPlayer as ReturnType<typeof vi.fn>;

            const { rerender } = render(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                />
            );

            // Initially in demo mode
            expect(useSongPlayerMock).toHaveBeenCalledWith(mockSongMap, true);

            // Rerender with jobId
            rerender(
                <TeleprompterView
                    songMap={mockSongMap}
                    transpose={0}
                    capo={0}
                    chordDisplay="names"
                    diagramVisibility={{}}
                    onToggleDiagram={vi.fn()}
                    jobId="new-job-456"
                />
            );

            // Should now be in audio mode
            expect(useSongPlayerMock).toHaveBeenLastCalledWith(mockSongMap, false);
        });
    });
});
