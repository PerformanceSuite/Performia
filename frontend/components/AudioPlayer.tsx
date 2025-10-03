import React, { useEffect, useRef, useState, useCallback } from 'react';

interface AudioPlayerProps {
  audioUrl: string;
  onTimeUpdate: (currentTime: number) => void;
  onDurationChange?: (duration: number) => void;
  onPlayStateChange?: (isPlaying: boolean) => void;
  onError?: (error: string) => void;
  className?: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({
  audioUrl,
  onTimeUpdate,
  onDurationChange,
  onPlayStateChange,
  onError,
  className = ''
}) => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const animationFrameRef = useRef<number>();

  // Throttled time update using requestAnimationFrame for smooth 60fps updates
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => {
      if (audio && !audio.paused) {
        const time = audio.currentTime;
        setCurrentTime(time);
        onTimeUpdate(time);
        animationFrameRef.current = requestAnimationFrame(updateTime);
      }
    };

    if (isPlaying) {
      animationFrameRef.current = requestAnimationFrame(updateTime);
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isPlaying, onTimeUpdate]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleDurationChange = () => {
      const dur = audio.duration;
      if (isFinite(dur)) {
        setDuration(dur);
        onDurationChange?.(dur);
      }
    };

    const handlePlay = () => {
      setIsPlaying(true);
      onPlayStateChange?.(true);
    };

    const handlePause = () => {
      setIsPlaying(false);
      onPlayStateChange?.(false);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      onPlayStateChange?.(false);
      setCurrentTime(0);
      onTimeUpdate(0);
    };

    const handleLoadedMetadata = () => {
      handleDurationChange();
      setIsLoading(false);
      setError(null);
    };

    const handleError = () => {
      const errorMessage = 'Failed to load audio. Please check your connection and try again.';
      setError(errorMessage);
      setIsLoading(false);
      setIsPlaying(false);
      onError?.(errorMessage);
      onPlayStateChange?.(false);
    };

    const handleLoadStart = () => {
      setIsLoading(true);
      setError(null);
    };

    audio.addEventListener('loadstart', handleLoadStart);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('durationchange', handleDurationChange);
    audio.addEventListener('play', handlePlay);
    audio.addEventListener('pause', handlePause);
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleError);

    return () => {
      audio.removeEventListener('loadstart', handleLoadStart);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('durationchange', handleDurationChange);
      audio.removeEventListener('play', handlePlay);
      audio.removeEventListener('pause', handlePause);
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleError);
    };
  }, [onDurationChange, onPlayStateChange, onTimeUpdate, onError]);

  // Reset when audio URL changes
  useEffect(() => {
    const audio = audioRef.current;
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
      setCurrentTime(0);
      setIsPlaying(false);
      setError(null);
      setIsLoading(true);
    }
  }, [audioUrl]);

  const retryLoad = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    setError(null);
    setIsLoading(true);
    audio.load();
  }, []);

  const togglePlay = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play().catch(err => {
        console.error('Error playing audio:', err);
      });
    }
  }, [isPlaying]);

  const seek = useCallback((time: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.currentTime = time;
    setCurrentTime(time);
    onTimeUpdate(time);
  }, [onTimeUpdate]);

  const handleVolumeChange = useCallback((newVolume: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.volume = newVolume;
    setVolume(newVolume);
    if (newVolume === 0) {
      setIsMuted(true);
    } else {
      setIsMuted(false);
    }
  }, []);

  const toggleMute = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isMuted) {
      audio.volume = volume > 0 ? volume : 1;
      setIsMuted(false);
    } else {
      audio.volume = 0;
      setIsMuted(true);
    }
  }, [isMuted, volume]);

  const formatTime = (seconds: number) => {
    if (!isFinite(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const progressPercentage = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className={`audio-player bg-gray-800 p-4 rounded-lg shadow-lg ${className}`}>
      <audio
        ref={audioRef}
        src={audioUrl}
        preload="metadata"
      />

      {/* Error Message */}
      {error && (
        <div className="mb-3 p-3 bg-red-900/50 border border-red-500 rounded-lg flex items-center justify-between">
          <div className="flex items-center gap-2 text-red-200">
            <span className="text-xl">⚠️</span>
            <span>{error}</span>
          </div>
          <button
            onClick={retryLoad}
            className="bg-red-700 hover:bg-red-600 text-white px-4 py-1 rounded transition-colors text-sm font-semibold"
          >
            Retry
          </button>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !error && (
        <div className="mb-3 p-3 bg-gray-700 rounded-lg flex items-center gap-2 text-gray-300">
          <div className="animate-spin h-4 w-4 border-2 border-performia-cyan border-t-transparent rounded-full"></div>
          <span>Loading audio...</span>
        </div>
      )}

      <div className="flex flex-col gap-3">
        {/* Progress Bar */}
        <div className="relative">
          <input
            type="range"
            min={0}
            max={duration || 0}
            value={currentTime}
            onChange={(e) => seek(parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #06b6d4 0%, #06b6d4 ${progressPercentage}%, #374151 ${progressPercentage}%, #374151 100%)`
            }}
          />
        </div>

        {/* Controls */}
        <div className="flex items-center gap-4">
          {/* Play/Pause Button */}
          <button
            onClick={togglePlay}
            disabled={!!error || isLoading}
            className="bg-performia-cyan hover:bg-cyan-400 text-black px-6 py-2 rounded-lg font-semibold transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isPlaying ? (
              <>
                <span>&#10074;&#10074;</span>
                <span>Pause</span>
              </>
            ) : (
              <>
                <span>&#9658;</span>
                <span>Play</span>
              </>
            )}
          </button>

          {/* Time Display */}
          <div className="text-white text-sm font-mono min-w-[100px]">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>

          {/* Spacer */}
          <div className="flex-1" />

          {/* Volume Controls */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggleMute}
              className="text-white hover:text-performia-cyan transition-colors"
              title={isMuted ? 'Unmute' : 'Mute'}
            >
              {isMuted || volume === 0 ? (
                <span className="text-xl">&#128263;</span>
              ) : volume < 0.5 ? (
                <span className="text-xl">&#128264;</span>
              ) : (
                <span className="text-xl">&#128266;</span>
              )}
            </button>
            <input
              type="range"
              min={0}
              max={1}
              step={0.01}
              value={isMuted ? 0 : volume}
              onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
              className="w-20 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>
      </div>

      <style>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 16px;
          height: 16px;
          background: #06b6d4;
          cursor: pointer;
          border-radius: 50%;
        }
        .slider::-moz-range-thumb {
          width: 16px;
          height: 16px;
          background: #06b6d4;
          cursor: pointer;
          border-radius: 50%;
          border: none;
        }
      `}</style>
    </div>
  );
};

export default AudioPlayer;
