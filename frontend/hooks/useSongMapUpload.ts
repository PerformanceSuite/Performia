import { useState, useCallback, useRef } from 'react';
import { SongMap } from '../types';
import {
    songMapApi,
    BackendSongMap,
    StatusResponse,
    SongMapApiError,
} from '../services/songMapApi';

export interface UploadProgress {
    status: 'idle' | 'uploading' | 'processing' | 'complete' | 'error';
    progress: number; // 0-100
    elapsed: number;
    estimatedRemaining?: number;
    message?: string;
}

export interface UseSongMapUploadResult {
    uploadSong: (file: File, metadata?: { title?: string; artist?: string }) => Promise<void>;
    cancelUpload: () => void;
    reset: () => void;
    isUploading: boolean;
    progress: UploadProgress;
    songMap: SongMap | null;
    backendSongMap: BackendSongMap | null;
    error: string | null;
    jobId: string | null;
}

/**
 * React hook for uploading audio files and generating Song Maps
 *
 * Usage:
 * ```tsx
 * const { uploadSong, isUploading, progress, songMap, error } = useSongMapUpload();
 *
 * const handleFileSelect = async (file: File) => {
 *   await uploadSong(file, { title: 'My Song', artist: 'Artist Name' });
 * };
 * ```
 */
export const useSongMapUpload = (): UseSongMapUploadResult => {
    const [isUploading, setIsUploading] = useState(false);
    const [progress, setProgress] = useState<UploadProgress>({
        status: 'idle',
        progress: 0,
        elapsed: 0,
    });
    const [songMap, setSongMap] = useState<SongMap | null>(null);
    const [backendSongMap, setBackendSongMap] = useState<BackendSongMap | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [jobId, setJobId] = useState<string | null>(null);

    // Use ref to track if upload should be cancelled
    const cancelledRef = useRef(false);

    /**
     * Upload and process an audio file
     */
    const uploadSong = useCallback(
        async (file: File, metadata?: { title?: string; artist?: string }) => {
            // Reset state
            setIsUploading(true);
            setError(null);
            setSongMap(null);
            setBackendSongMap(null);
            setJobId(null);
            cancelledRef.current = false;

            setProgress({
                status: 'uploading',
                progress: 0,
                elapsed: 0,
                message: 'Uploading audio file...',
            });

            try {
                // Start analysis
                const analyzeResponse = await songMapApi.analyzeSong(file);
                setJobId(analyzeResponse.job_id);

                if (cancelledRef.current) {
                    setProgress({ status: 'idle', progress: 0, elapsed: 0 });
                    setIsUploading(false);
                    return;
                }

                setProgress({
                    status: 'processing',
                    progress: 5,
                    elapsed: 0,
                    message: 'Processing audio...',
                });

                // Poll for completion
                const onProgress = (status: StatusResponse) => {
                    if (cancelledRef.current) {
                        throw new Error('Upload cancelled');
                    }

                    setProgress({
                        status: 'processing',
                        progress: Math.round(status.progress * 100),
                        elapsed: status.elapsed,
                        estimatedRemaining: status.estimated_remaining,
                        message: getStatusMessage(status.status, status.progress),
                    });
                };

                const backendMap = await songMapApi.waitForCompletion(
                    file,
                    onProgress,
                    1000
                );

                if (cancelledRef.current) {
                    setProgress({ status: 'idle', progress: 0, elapsed: 0 });
                    setIsUploading(false);
                    return;
                }

                // Convert to frontend format
                const frontendMap = songMapApi.convertToFrontendFormat(
                    backendMap,
                    metadata?.title || file.name.replace(/\.[^/.]+$/, ''),
                    metadata?.artist
                );

                setBackendSongMap(backendMap);
                setSongMap(frontendMap);

                setProgress({
                    status: 'complete',
                    progress: 100,
                    elapsed: backendMap.duration_sec || 0,
                    message: 'Song Map generated successfully!',
                });
            } catch (err) {
                if (cancelledRef.current) {
                    setProgress({ status: 'idle', progress: 0, elapsed: 0 });
                    return;
                }

                const errorMessage =
                    err instanceof SongMapApiError
                        ? err.message
                        : err instanceof Error
                        ? err.message
                        : 'Unknown error occurred';

                setError(errorMessage);
                setProgress({
                    status: 'error',
                    progress: 0,
                    elapsed: 0,
                    message: errorMessage,
                });
            } finally {
                setIsUploading(false);
            }
        },
        []
    );

    /**
     * Cancel the current upload
     */
    const cancelUpload = useCallback(() => {
        cancelledRef.current = true;
        setIsUploading(false);
        setProgress({
            status: 'idle',
            progress: 0,
            elapsed: 0,
            message: 'Upload cancelled',
        });
    }, []);

    /**
     * Reset all state
     */
    const reset = useCallback(() => {
        cancelledRef.current = false;
        setIsUploading(false);
        setProgress({ status: 'idle', progress: 0, elapsed: 0 });
        setSongMap(null);
        setBackendSongMap(null);
        setError(null);
        setJobId(null);
    }, []);

    return {
        uploadSong,
        cancelUpload,
        reset,
        isUploading,
        progress,
        songMap,
        backendSongMap,
        error,
        jobId,
    };
};

/**
 * Get a user-friendly message for the current status
 */
function getStatusMessage(status: string, progress: number): string {
    const percentage = Math.round(progress * 100);

    switch (status) {
        case 'pending':
            return 'Waiting to start...';
        case 'processing':
            if (percentage < 20) return 'Analyzing audio...';
            if (percentage < 40) return 'Detecting beats and tempo...';
            if (percentage < 60) return 'Recognizing chords...';
            if (percentage < 80) return 'Transcribing lyrics...';
            if (percentage < 95) return 'Finalizing Song Map...';
            return 'Almost done...';
        case 'complete':
            return 'Song Map generated successfully!';
        case 'error':
            return 'An error occurred';
        default:
            return 'Processing...';
    }
}
