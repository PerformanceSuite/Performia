/**
 * Song Map Upload Examples
 *
 * This file contains various examples of how to use the Song Map API client
 * and React hook in different scenarios.
 */

import React, { useState, useEffect } from 'react';
import { useSongMapUpload } from '../hooks/useSongMapUpload';
import { songMapApi, SongMapApiError } from '../services/songMapApi';
import { libraryService } from '../services/libraryService';

// ============================================================================
// Example 1: Basic File Upload with Hook
// ============================================================================

export function BasicUploadExample() {
  const { uploadSong, isUploading, progress, songMap, error } = useSongMapUpload();

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    await uploadSong(file, {
      title: 'My Song',
      artist: 'My Artist',
    });
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={handleFileChange} disabled={isUploading} />

      {isUploading && (
        <div>
          <p>{progress.message}</p>
          <progress value={progress.progress} max={100} />
        </div>
      )}

      {songMap && (
        <div>
          <h3>Success!</h3>
          <p>Title: {songMap.title}</p>
          <p>Artist: {songMap.artist}</p>
          <p>BPM: {songMap.bpm}</p>
          <p>Key: {songMap.key}</p>
        </div>
      )}

      {error && <div className="error">{error}</div>}
    </div>
  );
}

// ============================================================================
// Example 2: Drag and Drop Upload
// ============================================================================

export function DragDropUploadExample() {
  const { uploadSong, isUploading, progress, songMap } = useSongMapUpload();
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('audio/')) {
      const title = file.name.replace(/\.[^/.]+$/, '');
      await uploadSong(file, { title });
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      style={{
        border: isDragging ? '2px dashed blue' : '2px dashed gray',
        padding: '2rem',
        textAlign: 'center',
      }}
    >
      {!isUploading && !songMap && <p>Drag and drop an audio file here</p>}
      {isUploading && <p>Uploading: {progress.progress}%</p>}
      {songMap && <p>Uploaded: {songMap.title}</p>}
    </div>
  );
}

// ============================================================================
// Example 3: Upload with Progress Bar and Cancel
// ============================================================================

export function UploadWithCancelExample() {
  const {
    uploadSong,
    cancelUpload,
    reset,
    isUploading,
    progress,
    songMap,
    error,
  } = useSongMapUpload();

  const handleUpload = async (file: File) => {
    await uploadSong(file);
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        disabled={isUploading}
      />

      {isUploading && (
        <div>
          <p>{progress.message}</p>
          <div style={{ width: '100%', backgroundColor: '#ddd' }}>
            <div
              style={{
                width: `${progress.progress}%`,
                backgroundColor: 'blue',
                height: '20px',
              }}
            />
          </div>
          <p>
            {progress.progress}% complete • {Math.round(progress.elapsed)}s elapsed
            {progress.estimatedRemaining && ` • ~${Math.round(progress.estimatedRemaining)}s remaining`}
          </p>
          <button onClick={cancelUpload}>Cancel Upload</button>
        </div>
      )}

      {songMap && (
        <div>
          <h3>Upload Complete!</h3>
          <button onClick={reset}>Upload Another</button>
        </div>
      )}

      {error && (
        <div>
          <p>Error: {error}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Example 4: Upload and Auto-Add to Library
// ============================================================================

export function UploadToLibraryExample() {
  const { uploadSong, songMap, isUploading } = useSongMapUpload();
  const [addedToLibrary, setAddedToLibrary] = useState(false);

  useEffect(() => {
    if (songMap && !addedToLibrary) {
      // Automatically add to library when upload completes
      libraryService.addSong(songMap, {
        tags: ['uploaded', 'ai-generated'],
        difficulty: 'intermediate',
      });
      setAddedToLibrary(true);
    }
  }, [songMap, addedToLibrary]);

  const handleUpload = async (file: File) => {
    setAddedToLibrary(false);
    await uploadSong(file, {
      title: file.name.replace(/\.[^/.]+$/, ''),
      artist: 'Unknown',
    });
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        disabled={isUploading}
      />
      {addedToLibrary && <p>Song added to library!</p>}
    </div>
  );
}

// ============================================================================
// Example 5: Direct API Usage (Without Hook)
// ============================================================================

export function DirectApiExample() {
  const [status, setStatus] = useState<string>('idle');
  const [progress, setProgress] = useState<number>(0);

  const handleUpload = async (file: File) => {
    try {
      setStatus('uploading');

      // Upload file
      const response = await songMapApi.analyzeSong(file);
      const jobId = response.job_id;

      setStatus('processing');

      // Poll for completion
      while (true) {
        const statusResponse = await songMapApi.getStatus(jobId);
        setProgress(statusResponse.progress * 100);

        if (statusResponse.status === 'complete') {
          const result = await songMapApi.getSongMap(jobId);
          console.log('Song Map:', result.song_map);
          setStatus('complete');
          break;
        }

        if (statusResponse.status === 'error') {
          setStatus('error');
          break;
        }

        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('error');
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        disabled={status === 'uploading' || status === 'processing'}
      />
      <p>Status: {status}</p>
      {status === 'processing' && <p>Progress: {Math.round(progress)}%</p>}
    </div>
  );
}

// ============================================================================
// Example 6: Using waitForCompletion Helper
// ============================================================================

export function WaitForCompletionExample() {
  const [status, setStatus] = useState<string>('idle');
  const [progress, setProgress] = useState<number>(0);

  const handleUpload = async (file: File) => {
    try {
      setStatus('processing');

      const backendMap = await songMapApi.waitForCompletion(
        file,
        (statusUpdate) => {
          setProgress(statusUpdate.progress * 100);
          console.log(`${statusUpdate.progress * 100}% complete`);
        },
        1000
      );

      // Convert to frontend format
      const frontendMap = songMapApi.convertToFrontendFormat(
        backendMap,
        file.name.replace(/\.[^/.]+$/, ''),
        'Unknown Artist'
      );

      console.log('Song Map:', frontendMap);
      setStatus('complete');
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('error');
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])}
        disabled={status === 'processing'}
      />
      <p>Status: {status}</p>
      {status === 'processing' && <p>Progress: {Math.round(progress)}%</p>}
    </div>
  );
}

// ============================================================================
// Example 7: Batch Upload Multiple Files
// ============================================================================

export function BatchUploadExample() {
  const [uploads, setUploads] = useState<
    Array<{
      filename: string;
      status: string;
      progress: number;
      error?: string;
    }>
  >([]);

  const handleMultipleFiles = async (files: FileList) => {
    const fileArray = Array.from(files);

    // Initialize upload tracking
    setUploads(
      fileArray.map((file) => ({
        filename: file.name,
        status: 'pending',
        progress: 0,
      }))
    );

    // Upload all files (in parallel)
    await Promise.all(
      fileArray.map(async (file, index) => {
        try {
          await songMapApi.waitForCompletion(
            file,
            (status) => {
              setUploads((prev) => {
                const updated = [...prev];
                updated[index] = {
                  ...updated[index],
                  status: 'processing',
                  progress: status.progress * 100,
                };
                return updated;
              });
            },
            1000
          );

          setUploads((prev) => {
            const updated = [...prev];
            updated[index] = {
              ...updated[index],
              status: 'complete',
              progress: 100,
            };
            return updated;
          });
        } catch (error) {
          setUploads((prev) => {
            const updated = [...prev];
            updated[index] = {
              ...updated[index],
              status: 'error',
              error: error instanceof Error ? error.message : 'Unknown error',
            };
            return updated;
          });
        }
      })
    );
  };

  return (
    <div>
      <input
        type="file"
        accept="audio/*"
        multiple
        onChange={(e) => e.target.files && handleMultipleFiles(e.target.files)}
      />

      <div>
        {uploads.map((upload, index) => (
          <div key={index}>
            <strong>{upload.filename}</strong>: {upload.status} ({Math.round(upload.progress)}%)
            {upload.error && <span> - Error: {upload.error}</span>}
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// Example 8: Error Handling
// ============================================================================

export function ErrorHandlingExample() {
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    try {
      setError(null);
      await songMapApi.waitForCompletion(file);
    } catch (err) {
      if (err instanceof SongMapApiError) {
        // Handle API-specific errors
        setError(`API Error: ${err.message} (Status: ${err.statusCode})`);
        console.error('API Error Details:', err.details);
      } else if (err instanceof Error) {
        setError(`Error: ${err.message}`);
      } else {
        setError('Unknown error occurred');
      }
    }
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])} />
      {error && (
        <div style={{ color: 'red', padding: '1rem', border: '1px solid red' }}>
          {error}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Example 9: Custom Base URL
// ============================================================================

export function CustomBaseUrlExample() {
  const [baseUrl, setBaseUrl] = useState('http://localhost:8000');

  const handleUpload = async (file: File) => {
    // Create a custom API client with different base URL
    const customApi = new (songMapApi.constructor as any)(baseUrl);

    const backendMap = await customApi.waitForCompletion(file);
    console.log('Song Map from custom API:', backendMap);
  };

  return (
    <div>
      <input
        type="text"
        value={baseUrl}
        onChange={(e) => setBaseUrl(e.target.value)}
        placeholder="API Base URL"
      />
      <input type="file" accept="audio/*" onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])} />
    </div>
  );
}

// ============================================================================
// Example 10: Display Backend Song Map Details
// ============================================================================

export function BackendSongMapDetailsExample() {
  const { uploadSong, backendSongMap, songMap } = useSongMapUpload();

  const handleUpload = async (file: File) => {
    await uploadSong(file);
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])} />

      {backendSongMap && (
        <div>
          <h3>Backend Song Map Details</h3>
          <p>Duration: {backendSongMap.duration_sec}s</p>
          <p>BPM: {backendSongMap.tempo.bpm_global}</p>
          <p>Meter: {backendSongMap.meter.numerator}/{backendSongMap.meter.denominator}</p>
          <p>Beats: {backendSongMap.beats.length}</p>
          <p>Downbeats: {backendSongMap.downbeats.length}</p>
          <p>Chords: {backendSongMap.chords.length}</p>
          <p>Lyrics: {backendSongMap.lyrics.length} words</p>
          {backendSongMap.key && <p>Key Changes: {backendSongMap.key.length}</p>}
          {backendSongMap.sections && <p>Sections: {backendSongMap.sections.length}</p>}
        </div>
      )}

      {songMap && (
        <div>
          <h3>Frontend Song Map</h3>
          <p>Title: {songMap.title}</p>
          <p>Artist: {songMap.artist}</p>
          <p>BPM: {songMap.bpm}</p>
          <p>Key: {songMap.key}</p>
          <p>Sections: {songMap.sections.length}</p>
        </div>
      )}
    </div>
  );
}
