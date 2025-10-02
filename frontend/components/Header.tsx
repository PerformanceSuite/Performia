import React from 'react';
import { SettingsIcon, PlayIcon, ListeningIcon } from './icons/Icons';

interface HeaderProps {
    songTitle: string;
    artistName: string;
    onSettingsClick: () => void;
    onTitleClick: () => void;
    onPlayClick: () => void;
    onUploadClick?: () => void;
    onDemoClick?: () => void;
    currentView: 'teleprompter' | 'blueprint' | 'demo';
}

const Header: React.FC<HeaderProps> = ({ songTitle, artistName, onSettingsClick, onTitleClick, onPlayClick, onUploadClick, onDemoClick, currentView }) => {
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
                {onUploadClick && (
                    <button
                        onClick={onUploadClick}
                        title="Upload Song"
                        className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-4 py-3 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        Upload Song
                    </button>
                )}
                {onDemoClick && (
                    <button
                        onClick={onDemoClick}
                        title="Adapter Demo"
                        className="bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white px-4 py-3 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                        </svg>
                        Demo
                    </button>
                )}
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
