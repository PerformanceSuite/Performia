import React, { useState, useEffect } from 'react';
import { BackendSongMap, FrontendSongMap, adaptBackendToFrontend } from '../types';
import TeleprompterView from './TeleprompterView';

interface DemoStats {
    transformTime: number;
    sectionsCount: number;
    linesCount: number;
    syllablesCount: number;
}

const SongMapDemo: React.FC = () => {
    const [backendMap, setBackendMap] = useState<BackendSongMap | null>(null);
    const [frontendMap, setFrontendMap] = useState<FrontendSongMap | null>(null);
    const [stats, setStats] = useState<DemoStats | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [view, setView] = useState<'before' | 'after' | 'teleprompter'>('before');
    const [diagramVisibility, setDiagramVisibility] = useState<{ [key: string]: boolean }>({});

    // Available backend Song Maps
    const availableMaps = [
        '/src/adapters/__tests__/fixtures/simpleBackendMap.json',
        '/src/adapters/__tests__/fixtures/32193cf0.song_map.json',
        '/src/adapters/__tests__/fixtures/b72e82dc.song_map.json',
        '/src/adapters/__tests__/fixtures/integration_test.song_map.json',
    ];

    const [selectedMap, setSelectedMap] = useState(availableMaps[0]);

    const loadSongMap = async (path: string) => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`Failed to load: ${response.statusText}`);
            }

            const data = await response.json() as BackendSongMap;
            setBackendMap(data);

            // Transform and measure performance
            const startTime = performance.now();
            const transformed = adaptBackendToFrontend(data, {
                title: 'Demo Song',
                artist: 'Test Artist'
            });
            const endTime = performance.now();

            setFrontendMap(transformed);

            // Calculate stats
            const linesCount = transformed.sections.reduce((sum, s) => sum + s.lines.length, 0);
            const syllablesCount = transformed.sections.reduce(
                (sum, s) => sum + s.lines.reduce((lineSum, l) => lineSum + l.syllables.length, 0),
                0
            );

            setStats({
                transformTime: endTime - startTime,
                sectionsCount: transformed.sections.length,
                linesCount,
                syllablesCount
            });

            setView('before');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load Song Map');
            console.error('Failed to load Song Map:', err);
        } finally {
            setLoading(false);
        }
    };

    // Load default map on mount
    useEffect(() => {
        loadSongMap(selectedMap);
    }, []);

    const handleMapChange = (path: string) => {
        setSelectedMap(path);
        loadSongMap(path);
    };

    const handleToggleDiagram = (key: string) => {
        setDiagramVisibility(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    return (
        <div className="h-full flex flex-col bg-gray-900 text-white">
            {/* Header */}
            <div className="border-b border-gray-700 bg-gray-800 p-4">
                <div className="flex items-center justify-between">
                    <h1 className="text-2xl font-bold text-performia-cyan">
                        Song Map Adapter Demo
                    </h1>
                    <div className="flex items-center gap-4">
                        {stats && (
                            <div className="text-sm text-gray-300 bg-gray-700 px-4 py-2 rounded">
                                <span className="font-semibold text-performia-cyan">
                                    Transform: {stats.transformTime.toFixed(2)}ms
                                </span>
                                <span className="ml-4">
                                    {stats.sectionsCount} sections, {stats.linesCount} lines, {stats.syllablesCount} syllables
                                </span>
                            </div>
                        )}
                    </div>
                </div>

                {/* Controls */}
                <div className="mt-4 flex items-center gap-4">
                    <select
                        value={selectedMap}
                        onChange={(e) => handleMapChange(e.target.value)}
                        className="px-4 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:border-performia-cyan focus:outline-none"
                        disabled={loading}
                    >
                        {availableMaps.map((path) => (
                            <option key={path} value={path}>
                                {path.split('/').pop()?.replace('.json', '')}
                            </option>
                        ))}
                    </select>

                    <div className="flex gap-2">
                        <button
                            onClick={() => setView('before')}
                            className={`px-4 py-2 rounded font-medium transition-colors ${
                                view === 'before'
                                    ? 'bg-performia-cyan text-black'
                                    : 'bg-gray-700 text-white hover:bg-gray-600'
                            }`}
                        >
                            Backend Format
                        </button>
                        <button
                            onClick={() => setView('after')}
                            className={`px-4 py-2 rounded font-medium transition-colors ${
                                view === 'after'
                                    ? 'bg-performia-cyan text-black'
                                    : 'bg-gray-700 text-white hover:bg-gray-600'
                            }`}
                        >
                            Frontend Format
                        </button>
                        <button
                            onClick={() => setView('teleprompter')}
                            className={`px-4 py-2 rounded font-medium transition-colors ${
                                view === 'teleprompter'
                                    ? 'bg-performia-cyan text-black'
                                    : 'bg-gray-700 text-white hover:bg-gray-600'
                            }`}
                            disabled={!frontendMap}
                        >
                            Live View
                        </button>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-auto p-6">
                {loading && (
                    <div className="text-center py-12">
                        <div className="text-xl text-gray-400">Loading Song Map...</div>
                    </div>
                )}

                {error && (
                    <div className="bg-red-900/20 border-2 border-red-500 rounded-lg p-6 max-w-2xl mx-auto">
                        <h3 className="text-xl font-bold text-red-400 mb-2">Error</h3>
                        <p className="text-red-300">{error}</p>
                    </div>
                )}

                {!loading && !error && view === 'before' && backendMap && (
                    <div className="max-w-4xl mx-auto">
                        <h2 className="text-xl font-bold mb-4 text-performia-cyan">
                            Backend Song Map (Flat, Time-Indexed)
                        </h2>
                        <pre className="bg-gray-800 p-6 rounded-lg overflow-auto text-sm border border-gray-700">
                            {JSON.stringify(backendMap, null, 2)}
                        </pre>
                    </div>
                )}

                {!loading && !error && view === 'after' && frontendMap && (
                    <div className="max-w-4xl mx-auto">
                        <h2 className="text-xl font-bold mb-4 text-performia-cyan">
                            Frontend Song Map (Hierarchical)
                        </h2>
                        <pre className="bg-gray-800 p-6 rounded-lg overflow-auto text-sm border border-gray-700">
                            {JSON.stringify(frontendMap, null, 2)}
                        </pre>
                    </div>
                )}

                {!loading && !error && view === 'teleprompter' && frontendMap && (
                    <div className="h-full flex flex-col">
                        <h2 className="text-xl font-bold mb-4 text-performia-cyan text-center">
                            TeleprompterView Rendering
                        </h2>
                        <div className="flex-1 relative">
                            <TeleprompterView
                                songMap={frontendMap}
                                transpose={0}
                                capo={0}
                                chordDisplay="names"
                                diagramVisibility={diagramVisibility}
                                onToggleDiagram={handleToggleDiagram}
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SongMapDemo;
