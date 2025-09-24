import React from 'react';
import { ChordDisplayMode } from '../types';
import { CloseIcon } from './icons/Icons';

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
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({
    isOpen, onClose, chordDisplay, onChordDisplayChange,
    fontSize, onFontSizeChange, transpose, onTransposeChange,
    capo, onCapoChange
}) => {
    if (!isOpen) {
        return null;
    }

    return (
        <>
            <div 
                className="fixed inset-0 bg-black bg-opacity-50 z-20 opacity-100"
                onClick={onClose}
            ></div>
            <div id="settings-panel" className="fixed top-0 left-0 h-full w-96 bg-gray-900 border-r border-gray-800 z-30 transform translate-x-0 flex flex-col">
                <div className="flex justify-between items-center p-4 border-b border-gray-800 shrink-0">
                    <h2 className="text-xl font-bold">Performia Hub</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-white">
                        <CloseIcon />
                    </button>
                </div>
                
                <div className="p-6 space-y-6 overflow-y-auto flex-grow">
                    <h3 className="text-lg font-semibold text-gray-400">Display Options</h3>
                    <div className="flex items-center justify-between">
                        <span>Chord Display</span>
                        <div className="segmented-control flex p-1 bg-gray-800 rounded-lg">
                            {(['off', 'names', 'diagrams'] as ChordDisplayMode[]).map(mode => (
                                <button 
                                    key={mode} 
                                    onClick={() => onChordDisplayChange(mode)}
                                    className={`px-3 py-1 text-sm rounded-md ${chordDisplay === mode ? 'active' : ''}`}
                                >
                                    {mode.charAt(0).toUpperCase() + mode.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="space-y-2">
                        <label htmlFor="font-size-slider" className="flex items-center justify-between text-sm">
                            <span>Font Size</span>
                            <span>{fontSize}%</span>
                        </label>
                        <input 
                            type="range" id="font-size-slider" 
                            min="50" max="150" value={fontSize} 
                            onChange={(e) => onFontSizeChange(parseInt(e.target.value))}
                            className="w-full"
                        />
                    </div>

                    <hr className="border-gray-700 my-4" />
                    <h3 className="text-lg font-semibold text-gray-400">Musical Tools</h3>
                    <div className="flex items-center justify-between">
                        <span>Transpose</span>
                        <div className="flex items-center space-x-2">
                            <button onClick={() => onTransposeChange(transpose - 1)} className="px-2 py-0.5 bg-gray-800 hover:bg-gray-700 rounded">-</button>
                            <span className="text-sm w-12 text-center">{transpose > 0 ? `+${transpose}` : transpose}</span>
                            <button onClick={() => onTransposeChange(transpose + 1)} className="px-2 py-0.5 bg-gray-800 hover:bg-gray-700 rounded">+</button>
                        </div>
                    </div>
                    <div className="flex items-center justify-between">
                        <span>Capo</span>
                        <div className="flex items-center space-x-2">
                            <button onClick={() => onCapoChange(Math.max(0, capo - 1))} className="px-2 py-0.5 bg-gray-800 hover:bg-gray-700 rounded">-</button>
                            <span className="text-sm w-12 text-center">{capo > 0 ? `Fret ${capo}` : 'None'}</span>
                            <button onClick={() => onCapoChange(capo + 1)} className="px-2 py-0.5 bg-gray-800 hover:bg-gray-700 rounded">+</button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default SettingsPanel;
