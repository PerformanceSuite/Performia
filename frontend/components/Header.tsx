import React from 'react';
import { SettingsIcon, PlayIcon, ListeningIcon } from './icons/Icons';

interface HeaderProps {
    songTitle: string;
    artistName: string;
    onSettingsClick: () => void;
    onTitleClick: () => void;
    onPlayClick: () => void;
    currentView: 'teleprompter' | 'blueprint';
}

const Header: React.FC<HeaderProps> = ({ songTitle, artistName, onSettingsClick, onTitleClick, onPlayClick, currentView }) => {
    return (
        <header className="w-full px-6 py-3 border-b border-gray-800 shrink-0 z-10 flex justify-between items-center">
            <div className="flex items-center gap-4">
                <button 
                    onClick={onSettingsClick} 
                    title="Settings"
                    className="bg-cyan-600 text-white hover:bg-cyan-500 hover:text-black transition-all duration-200 p-3 rounded-lg border border-cyan-400 hover:border-cyan-300 shadow-lg shadow-cyan-600/20"
                    style={{ minWidth: '52px', minHeight: '52px' }}
                >
                    <SettingsIcon />
                </button>
            </div>
            <div className="w-1/3 text-center flex items-center justify-center">
                <div className="flex flex-col items-center">
                    <button onClick={onTitleClick} className="text-lg font-semibold hover:text-cyan-400 transition">
                        {songTitle}
                    </button>
                    <p className="text-sm text-gray-400">{artistName}</p>
                </div>
                {currentView === 'blueprint' && (
                    <button onClick={onPlayClick} className="ml-4 text-cyan-400 hover:text-white">
                        <PlayIcon />
                    </button>
                )}
            </div>
            <div className="w-1/3 flex justify-end">
                <ListeningIcon />
            </div>
        </header>
    );
};

export default Header;
