import { useEffect, useCallback } from 'react';

export interface KeyboardShortcut {
    key: string;
    ctrlKey?: boolean;
    shiftKey?: boolean;
    altKey?: boolean;
    metaKey?: boolean;
    action: () => void;
    description: string;
}

/**
 * Hook for managing keyboard shortcuts
 *
 * Keyboard shortcuts:
 * - Space: Play/Pause
 * - ArrowUp/Down: Adjust font size
 * - ArrowLeft/Right: Transpose
 * - F: Toggle fullscreen
 * - H: Toggle help
 * - S: Open settings
 * - L: Open library
 * - Escape: Close modals
 */
export const useKeyboardShortcuts = (shortcuts: KeyboardShortcut[], enabled = true) => {
    const handleKeyDown = useCallback((event: KeyboardEvent) => {
        // Don't trigger shortcuts when typing in inputs
        const target = event.target as HTMLElement;
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
            return;
        }

        for (const shortcut of shortcuts) {
            const keyMatches = event.key === shortcut.key;
            const ctrlMatches = shortcut.ctrlKey ? event.ctrlKey : !event.ctrlKey;
            const shiftMatches = shortcut.shiftKey ? event.shiftKey : !event.shiftKey;
            const altMatches = shortcut.altKey ? event.altKey : !event.altKey;
            const metaMatches = shortcut.metaKey ? event.metaKey : !event.metaKey;

            if (keyMatches && ctrlMatches && shiftMatches && altMatches && metaMatches) {
                event.preventDefault();
                shortcut.action();
                break;
            }
        }
    }, [shortcuts]);

    useEffect(() => {
        if (!enabled) return;

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [handleKeyDown, enabled]);
};

/**
 * Predefined keyboard shortcuts for the app
 */
export const createDefaultShortcuts = (handlers: {
    onPlayPause?: () => void;
    onFontIncrease?: () => void;
    onFontDecrease?: () => void;
    onTransposeUp?: () => void;
    onTransposeDown?: () => void;
    onToggleFullscreen?: () => void;
    onToggleHelp?: () => void;
    onOpenSettings?: () => void;
    onOpenLibrary?: () => void;
    onEscape?: () => void;
}): KeyboardShortcut[] => {
    const shortcuts: KeyboardShortcut[] = [];

    if (handlers.onPlayPause) {
        shortcuts.push({
            key: ' ',
            action: handlers.onPlayPause,
            description: 'Play/Pause'
        });
    }

    if (handlers.onFontIncrease) {
        shortcuts.push({
            key: 'ArrowUp',
            action: handlers.onFontIncrease,
            description: 'Increase font size'
        });
    }

    if (handlers.onFontDecrease) {
        shortcuts.push({
            key: 'ArrowDown',
            action: handlers.onFontDecrease,
            description: 'Decrease font size'
        });
    }

    if (handlers.onTransposeUp) {
        shortcuts.push({
            key: 'ArrowRight',
            action: handlers.onTransposeUp,
            description: 'Transpose up'
        });
    }

    if (handlers.onTransposeDown) {
        shortcuts.push({
            key: 'ArrowLeft',
            action: handlers.onTransposeDown,
            description: 'Transpose down'
        });
    }

    if (handlers.onToggleFullscreen) {
        shortcuts.push({
            key: 'f',
            action: handlers.onToggleFullscreen,
            description: 'Toggle fullscreen'
        });
    }

    if (handlers.onToggleHelp) {
        shortcuts.push({
            key: 'h',
            action: handlers.onToggleHelp,
            description: 'Toggle help'
        });
    }

    if (handlers.onOpenSettings) {
        shortcuts.push({
            key: 's',
            action: handlers.onOpenSettings,
            description: 'Open settings'
        });
    }

    if (handlers.onOpenLibrary) {
        shortcuts.push({
            key: 'l',
            action: handlers.onOpenLibrary,
            description: 'Open library'
        });
    }

    if (handlers.onEscape) {
        shortcuts.push({
            key: 'Escape',
            action: handlers.onEscape,
            description: 'Close modal/Cancel'
        });
    }

    return shortcuts;
};
