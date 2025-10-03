import { SongMap } from '../types';

/**
 * Backend Song Map API Types
 * These types match the backend's Song Map schema
 */

export interface Meter {
    numerator: number;
    denominator: number;
}

export interface Tempo {
    bpm_global: number;
    curve?: [number, number][];
    confidence?: number;
}

export interface KeySegment {
    start: number;
    end: number;
    tonic: string;
    mode: string;
    conf?: number;
}

export interface Chord {
    start: number;
    end: number;
    label: string;
    conf?: number;
}

export interface Section {
    start: number;
    end: number;
    label: string;
}

export interface Lyric {
    start: number;
    end: number;
    text: string;
    conf?: number;
}

export interface Performance {
    melody?: any[];
    bass?: any[];
}

/**
 * Backend Song Map format (from analysis pipeline)
 */
export interface BackendSongMap {
    id: string;
    duration_sec: number;
    tempo: Tempo;
    beats: number[];
    downbeats: number[];
    meter: Meter;
    chords: Chord[];
    lyrics: Lyric[];
    key?: KeySegment[];
    sections?: Section[];
    performance?: Performance;
    provenance?: any;
}

/**
 * API Response Types
 */

export interface AnalyzeResponse {
    job_id: string;
    status: 'pending' | 'processing' | 'complete' | 'error';
    message?: string;
}

export interface StatusResponse {
    job_id: string;
    status: 'pending' | 'processing' | 'complete' | 'error';
    progress: number; // 0.0 - 1.0
    elapsed: number;
    estimated_remaining?: number;
    error_message?: string | null;
}

export interface SongMapResponse {
    job_id: string;
    song_map: BackendSongMap;
    elapsed: number;
}

/**
 * API Error Class
 */
export class SongMapApiError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public details?: any
    ) {
        super(message);
        this.name = 'SongMapApiError';
    }
}

/**
 * Song Map API Client
 *
 * Handles communication with the backend Song Map generation API.
 * Provides methods for uploading audio files, polling job status,
 * and retrieving completed Song Maps.
 */
export class SongMapApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:3002') {
        this.baseUrl = baseUrl;
    }

    /**
     * Upload an audio file for analysis
     *
     * @param audioFile - The audio file to analyze (WAV, MP3, etc.)
     * @returns Job information including job_id for status polling
     */
    async analyzeSong(audioFile: File): Promise<AnalyzeResponse> {
        const formData = new FormData();
        formData.append('file', audioFile);

        try {
            const response = await fetch(`${this.baseUrl}/api/analyze`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new SongMapApiError(
                    errorData.detail || `Upload failed: ${response.statusText}`,
                    response.status,
                    errorData
                );
            }

            return await response.json();
        } catch (error) {
            if (error instanceof SongMapApiError) {
                throw error;
            }
            throw new SongMapApiError(
                `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
            );
        }
    }

    /**
     * Get the current status of a Song Map generation job
     *
     * @param jobId - The job ID returned from analyzeSong()
     * @returns Current job status and progress information
     */
    async getStatus(jobId: string): Promise<StatusResponse> {
        try {
            const response = await fetch(`${this.baseUrl}/api/status/${jobId}`);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new SongMapApiError(
                    errorData.detail || `Status check failed: ${response.statusText}`,
                    response.status,
                    errorData
                );
            }

            return await response.json();
        } catch (error) {
            if (error instanceof SongMapApiError) {
                throw error;
            }
            throw new SongMapApiError(
                `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
            );
        }
    }

    /**
     * Retrieve the completed Song Map
     *
     * @param jobId - The job ID of a completed job
     * @returns The generated Song Map and metadata
     */
    async getSongMap(jobId: string): Promise<SongMapResponse> {
        try {
            const response = await fetch(`${this.baseUrl}/api/songmap/${jobId}`);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new SongMapApiError(
                    errorData.detail || `Song Map retrieval failed: ${response.statusText}`,
                    response.status,
                    errorData
                );
            }

            return await response.json();
        } catch (error) {
            if (error instanceof SongMapApiError) {
                throw error;
            }
            throw new SongMapApiError(
                `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
            );
        }
    }

    /**
     * Upload a file and wait for completion, polling status periodically
     *
     * @param audioFile - The audio file to analyze
     * @param onProgress - Optional callback for progress updates
     * @param pollInterval - Polling interval in milliseconds (default: 1000)
     * @returns The completed Song Map in backend format
     */
    async waitForCompletion(
        audioFile: File,
        onProgress?: (status: StatusResponse) => void,
        pollInterval: number = 1000
    ): Promise<BackendSongMap> {
        // Start the analysis
        const analyzeResponse = await this.analyzeSong(audioFile);
        const jobId = analyzeResponse.job_id;

        // Poll until complete
        while (true) {
            const status = await this.getStatus(jobId);

            // Call progress callback if provided
            if (onProgress) {
                onProgress(status);
            }

            // Check if complete
            if (status.status === 'complete') {
                const result = await this.getSongMap(jobId);
                return result.song_map;
            }

            // Check if error
            if (status.status === 'error') {
                throw new SongMapApiError(
                    status.error_message || 'Song Map generation failed',
                    undefined,
                    status
                );
            }

            // Wait before next poll
            await new Promise(resolve => setTimeout(resolve, pollInterval));
        }
    }

    /**
     * Convert backend Song Map format to frontend format
     *
     * This is a basic converter - you may need to enhance it based on your needs.
     * The backend format is more detailed, so some simplification is needed.
     */
    convertToFrontendFormat(backendMap: BackendSongMap, title?: string, artist?: string): SongMap {
        // Extract key (use first key segment if available)
        const key = backendMap.key?.[0]
            ? `${backendMap.key[0].tonic} ${backendMap.key[0].mode}`
            : 'Unknown';

        // Get BPM
        const bpm = Math.round(backendMap.tempo.bpm_global);

        // Convert lyrics to sections
        // This is a simplified conversion - you may want to enhance this
        // to use the backend's sections array if available
        const sections = this.convertLyricsToSections(backendMap.lyrics, backendMap.chords);

        return {
            title: title || 'Unknown Title',
            artist: artist || 'Unknown Artist',
            key,
            bpm,
            sections,
        };
    }

    /**
     * Convert backend lyrics array to frontend sections/lines/syllables
     * This is a simplified conversion that groups lyrics into sections
     */
    private convertLyricsToSections(lyrics: Lyric[], chords: Chord[]): any[] {
        if (!lyrics || lyrics.length === 0) {
            return [];
        }

        // Group lyrics into lines (by detecting pauses > 1 second)
        const lines: Lyric[][] = [];
        let currentLine: Lyric[] = [];

        for (let i = 0; i < lyrics.length; i++) {
            const lyric = lyrics[i];
            currentLine.push(lyric);

            // If next lyric has a gap > 1 second or this is the last lyric, start new line
            const nextLyric = lyrics[i + 1];
            if (!nextLyric || (nextLyric.start - lyric.end) > 1.0) {
                lines.push([...currentLine]);
                currentLine = [];
            }
        }

        // Convert to frontend format
        // For now, put everything in one "Verse" section
        // You can enhance this to detect actual sections
        return [{
            name: 'Verse 1',
            lines: lines.map(line => ({
                syllables: line.map(lyric => {
                    // Find chord at this time
                    const chord = chords.find(c =>
                        lyric.start >= c.start && lyric.start < c.end
                    );

                    return {
                        text: lyric.text,
                        startTime: lyric.start,
                        duration: lyric.end - lyric.start,
                        chord: chord?.label,
                    };
                }),
            })),
        }];
    }
}

/**
 * Singleton instance
 * Use this for all API calls throughout your application
 */
export const songMapApi = new SongMapApiClient();
