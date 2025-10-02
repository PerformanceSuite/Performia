import React, { useState } from 'react';

export type StemType = 'original' | 'vocals' | 'bass' | 'drums' | 'other';

interface StemOption {
  id: StemType;
  label: string;
  description: string;
}

interface StemSelectorProps {
  jobId: string;
  baseUrl?: string;
  onStemChange: (stemUrl: string, stemType: StemType) => void;
  className?: string;
}

const STEM_OPTIONS: StemOption[] = [
  {
    id: 'original',
    label: 'Full Mix',
    description: 'Original audio with all instruments'
  },
  {
    id: 'vocals',
    label: 'Vocals',
    description: 'Isolated vocal track'
  },
  {
    id: 'bass',
    label: 'Bass',
    description: 'Bass and low-end instruments'
  },
  {
    id: 'drums',
    label: 'Drums',
    description: 'Percussion and drums'
  },
  {
    id: 'other',
    label: 'Other',
    description: 'Remaining instruments'
  }
];

export const StemSelector: React.FC<StemSelectorProps> = ({
  jobId,
  baseUrl = 'http://localhost:8000',
  onStemChange,
  className = ''
}) => {
  const [selectedStem, setSelectedStem] = useState<StemType>('original');
  const [loadingStems, setLoadingStems] = useState<Set<StemType>>(new Set());
  const [availableStems, setAvailableStems] = useState<Set<StemType>>(new Set(['original']));

  const buildStemUrl = (stemType: StemType): string => {
    if (stemType === 'original') {
      return `${baseUrl}/api/audio/${jobId}/original`;
    } else {
      return `${baseUrl}/api/audio/${jobId}/stem/${stemType}`;
    }
  };

  const handleStemSelect = async (stemType: StemType) => {
    const url = buildStemUrl(stemType);

    // For non-original stems, check if they exist first
    if (stemType !== 'original' && !availableStems.has(stemType)) {
      setLoadingStems(prev => new Set(prev).add(stemType));

      try {
        const response = await fetch(url, { method: 'HEAD' });
        if (response.ok) {
          setAvailableStems(prev => new Set(prev).add(stemType));
          setSelectedStem(stemType);
          onStemChange(url, stemType);
        } else {
          console.warn(`Stem ${stemType} not available for job ${jobId}`);
          alert(`The ${stemType} stem is not available for this song. It may not have been processed yet.`);
        }
      } catch (error) {
        console.error(`Error checking stem ${stemType}:`, error);
        alert(`Unable to load ${stemType} stem. Please try again.`);
      } finally {
        setLoadingStems(prev => {
          const next = new Set(prev);
          next.delete(stemType);
          return next;
        });
      }
    } else {
      setSelectedStem(stemType);
      onStemChange(url, stemType);
    }
  };

  return (
    <div className={`stem-selector ${className}`}>
      <div className="mb-2">
        <h3 className="text-sm font-semibold text-gray-300">Audio Track</h3>
        <p className="text-xs text-gray-500">Select which audio track to play</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {STEM_OPTIONS.map(stem => {
          const isSelected = selectedStem === stem.id;
          const isLoading = loadingStems.has(stem.id);
          const isAvailable = availableStems.has(stem.id);

          return (
            <button
              key={stem.id}
              onClick={() => handleStemSelect(stem.id)}
              disabled={isLoading}
              className={`
                px-4 py-2 rounded-lg font-medium transition-all
                ${isSelected
                  ? 'bg-performia-cyan text-black shadow-lg scale-105'
                  : 'bg-gray-700 text-white hover:bg-gray-600'
                }
                ${isLoading ? 'opacity-50 cursor-wait' : 'cursor-pointer'}
                ${!isAvailable && stem.id !== 'original' ? 'opacity-60' : ''}
              `}
              title={stem.description}
            >
              <div className="flex items-center gap-2">
                {isLoading ? (
                  <span className="inline-block animate-spin">&#8987;</span>
                ) : isSelected ? (
                  <span>&#9658;</span>
                ) : (
                  <span className="opacity-0">&#9658;</span>
                )}
                <span>{stem.label}</span>
              </div>
            </button>
          );
        })}
      </div>

      {selectedStem !== 'original' && (
        <div className="mt-2 p-2 bg-gray-800 rounded text-xs text-gray-400">
          <span className="text-performia-cyan font-semibold">Note:</span>
          {' '}Playing isolated {selectedStem} track.
          Switch to "Full Mix" to hear the complete song.
        </div>
      )}
    </div>
  );
};

export default StemSelector;
