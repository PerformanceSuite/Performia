import React, { useState } from 'react';
import { ChordDisplayMode, SongMap } from '../types';
import { CloseIcon } from './icons/Icons';
import LibraryView from './LibraryView';

interface SettingsPanelProps {
    isOpen: boolean;
    onClose: () => void;
    chordDisplay: ChordDisplayMode;
    onChordDisplayChange: (mode: ChordDisplayMode) => void;
    fontSize: number;
    onFontSizeChange: (size: number) => void;
    transpose: number;
    onTransposeChange: (value: number) => void;
    capo: number;
    onCapoChange: (value: number) => void;
    currentSong?: SongMap;
    onSongSelect: (songMap: SongMap, jobId?: string) => void;
    highContrastMode: boolean;
    onHighContrastModeChange: (enabled: boolean) => void;
    reducedMotion: boolean;
    onReducedMotionChange: (enabled: boolean) => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({
    isOpen, onClose, chordDisplay, onChordDisplayChange,
    fontSize, onFontSizeChange, transpose, onTransposeChange,
    capo, onCapoChange, currentSong, onSongSelect,
    highContrastMode, onHighContrastModeChange,
    reducedMotion, onReducedMotionChange
}) => {
    const [activeTab, setActiveTab] = useState<'now-playing' | 'library' | 'ai-band'>('now-playing');
    if (!isOpen) {
        return null;
    }

    return (
        <>
            <div 
                className="fixed inset-0 bg-black bg-opacity-50 z-20 opacity-100"
                onClick={onClose}
            ></div>
            <div id="settings-panel" className="fixed top-0 left-0 h-full w-96 bg-gray-900 border-r border-gray-700 z-30 transform translate-x-0 flex flex-col">
                <div className="flex justify-between items-center px-6 py-5 border-b border-gray-700 shrink-0">
                    <h2 className="text-xl font-semibold text-white">
                        Settings
                    </h2>
                    <button 
                        onClick={onClose} 
                        className="bg-gray-700 text-white hover:bg-cyan-600 hover:text-black transition-all duration-200 p-3 rounded-lg border border-gray-500 hover:border-cyan-400"
                        style={{ minWidth: '48px', minHeight: '48px' }}
                        title="Close Settings"
                    >
                        <CloseIcon />
                    </button>
                </div>
                
                {/* Tab Navigation */}
                <div className="flex border-b border-gray-800 shrink-0">
                    {[
                        { id: 'now-playing', label: 'Now Playing' },
                        { id: 'library', label: 'Library' },
                        { id: 'ai-band', label: 'AI Band' }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id as any)}
                            className={`settings-tab ${
                                activeTab === tab.id ? 'active' : 'text-gray-400'
                            }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
                
                {/* Tab Content */}
                <div className="flex-grow overflow-hidden">
                    {activeTab === 'now-playing' && (
                        <div className="p-6 overflow-y-auto h-full">
                            {/* PRIMARY PERFORMANCE CONTROLS - Most Important */}
                            <div className="settings-section">
                                <h3 className="settings-section-title primary">⚡ Live Controls</h3>
                                
                                <div className="settings-row">
                                    <span className="settings-label primary">Chord Display</span>
                                    <div className="segmented-control flex">
                                        {(['off', 'names', 'diagrams'] as ChordDisplayMode[]).map(mode => (
                                            <button 
                                                key={mode} 
                                                onClick={() => onChordDisplayChange(mode)}
                                                className={`${chordDisplay === mode ? 'active' : ''}`}
                                            >
                                                {mode.charAt(0).toUpperCase() + mode.slice(1)}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                                
                                <div className="settings-row">
                                    <span className="settings-label primary">Font Size</span>
                                    <span className={`settings-value-display ${fontSize !== 100 ? 'primary' : ''}`}>
                                        {fontSize}%
                                    </span>
                                </div>
                                
                                <div className="mt-4">
                                    <input 
                                        type="range" id="font-size-slider" 
                                        min="50" max="150" value={fontSize} 
                                        onChange={(e) => onFontSizeChange(parseInt(e.target.value))}
                                        className="w-full"
                                    />
                                </div>
                            </div>

                            {/* MUSICAL TOOLS - Performance Critical */}
                            <div className="settings-section">
                                <h3 className="settings-section-title primary">🎵 Musical Tools</h3>
                                
                                <div className="settings-row">
                                    <span className="settings-label primary">Transpose</span>
                                    <div className="flex items-center space-x-3">
                                        <button 
                                            onClick={() => onTransposeChange(transpose - 1)} 
                                            className="settings-button"
                                        >
                                            −
                                        </button>
                                        <span className={`settings-value-display ${transpose !== 0 ? 'primary' : ''}`}>
                                            {transpose > 0 ? `+${transpose}` : transpose}
                                        </span>
                                        <button 
                                            onClick={() => onTransposeChange(transpose + 1)} 
                                            className="settings-button"
                                        >
                                            +
                                        </button>
                                    </div>
                                </div>
                                
                                <div className="settings-row">
                                    <span className="settings-label primary">Capo</span>
                                    <div className="flex items-center space-x-3">
                                        <button 
                                            onClick={() => onCapoChange(Math.max(0, capo - 1))} 
                                            className="settings-button"
                                        >
                                            −
                                        </button>
                                        <span className={`settings-value-display ${capo !== 0 ? 'primary' : ''}`}>
                                            {capo > 0 ? `Fret ${capo}` : 'None'}
                                        </span>
                                        <button 
                                            onClick={() => onCapoChange(capo + 1)} 
                                            className="settings-button"
                                        >
                                            +
                                        </button>
                                    </div>
                                </div>
                            </div>

                            {/* ACCESSIBILITY CONTROLS */}
                            <div className="settings-section">
                                <h3 className="settings-section-title">♿ Accessibility</h3>

                                <div className="settings-row">
                                    <span className="settings-label">High Contrast Mode</span>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={highContrastMode}
                                            onChange={(e) => onHighContrastModeChange(e.target.checked)}
                                            aria-label="Toggle high contrast mode"
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>

                                <div className="settings-row">
                                    <span className="settings-label">Reduced Motion</span>
                                    <label className="toggle-switch">
                                        <input
                                            type="checkbox"
                                            checked={reducedMotion}
                                            onChange={(e) => onReducedMotionChange(e.target.checked)}
                                            aria-label="Toggle reduced motion mode"
                                        />
                                        <span className="toggle-slider"></span>
                                    </label>
                                </div>

                                <div className="mt-2 text-xs text-gray-400">
                                    <p>High contrast improves readability in bright conditions.</p>
                                    <p className="mt-1">Reduced motion minimizes animations for comfort.</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'library' && (
                        <LibraryView 
                            currentSong={currentSong}
                            onSongSelect={onSongSelect}
                            onClose={onClose}
                        />
                    )}
                    
                    {activeTab === 'ai-band' && (
                        <div className="p-6 space-y-6 overflow-y-auto h-full">
                            <h3 className="text-lg font-semibold text-gray-400">AI Band</h3>
                            <div className="text-center text-gray-500 mt-8">
                                <div className="mb-4 text-4xl">🎸</div>
                                <p className="text-lg font-medium text-gray-300">Coming Soon!</p>
                                <p className="text-sm mt-2">AI Band features will be available in Performia Studio.</p>
                                <div className="mt-6 p-4 bg-gray-800 rounded-lg border border-gray-700">
                                    <h4 className="font-semibold text-performia-cyan mb-2">Upgrade to Performia Studio</h4>
                                    <ul className="text-sm text-left space-y-1">
                                        <li>• AI band members that learn your style</li>
                                        <li>• Conversational song creation</li>
                                        <li>• Real-time accompaniment</li>
                                        <li>• Advanced musical AI</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
};

export default SettingsPanel;
