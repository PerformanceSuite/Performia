# Song Map API Client - Usage Guide

## Overview

The Song Map API client provides a TypeScript interface for uploading audio files to the backend analysis pipeline and retrieving generated Song Maps.

## Files Created

1. **`/services/songMapApi.ts`** - Core API client and type definitions
2. **`/hooks/useSongMapUpload.ts`** - React hook for easy integration
3. **`/components/SongMapUploadTest.tsx`** - Test component demonstrating usage

## Quick Start

### Basic Usage with React Hook

```tsx
import { useSongMapUpload } from '../hooks/useSongMapUpload';

function MyComponent() {
  const { uploadSong, isUploading, progress, songMap, error } = useSongMapUpload();

  const handleFileSelect = async (file: File) => {
    await uploadSong(file, {
      title: 'My Song',
      artist: 'My Artist'
    });
  };

  return (
    <div>
      {isUploading && <div>Progress: {progress.progress}%</div>}
      {songMap && <div>Success! Song Map generated.</div>}
      {error && <div>Error: {error}</div>}
    </div>
  );
}
```

### Direct API Usage (Without Hook)

```tsx
import { songMapApi } from '../services/songMapApi';

async function uploadAndProcess(file: File) {
  try {
    // Option 1: Manual polling
    const response = await songMapApi.analyzeSong(file);
    const jobId = response.job_id;

    // Poll for status
    let status = await songMapApi.getStatus(jobId);
    while (status.status === 'processing') {
      await new Promise(resolve => setTimeout(resolve, 1000));
      status = await songMapApi.getStatus(jobId);
    }

    // Get result
    const result = await songMapApi.getSongMap(jobId);
    console.log('Song Map:', result.song_map);

    // Option 2: Use helper method
    const backendMap = await songMapApi.waitForCompletion(
      file,
      (status) => console.log(`Progress: ${status.progress * 100}%`)
    );

    // Convert to frontend format
    const frontendMap = songMapApi.convertToFrontendFormat(
      backendMap,
      'Song Title',
      'Artist Name'
    );

  } catch (error) {
    console.error('Upload failed:', error);
  }
}
```

## API Reference

### SongMapApiClient

The main client class for interacting with the backend API.

#### Methods

##### `analyzeSong(audioFile: File): Promise<AnalyzeResponse>`

Upload an audio file for analysis.

**Parameters:**
- `audioFile` - The audio file to analyze (WAV, MP3, FLAC, etc.)

**Returns:**
- `job_id` - Unique identifier for tracking the job
- `status` - Initial status ('pending' or 'processing')
- `message` - Optional status message

**Example:**
```tsx
const response = await songMapApi.analyzeSong(file);
console.log('Job ID:', response.job_id);
```

##### `getStatus(jobId: string): Promise<StatusResponse>`

Check the status of a running job.

**Parameters:**
- `jobId` - The job ID from `analyzeSong()`

**Returns:**
- `job_id` - The job identifier
- `status` - Current status ('pending', 'processing', 'complete', 'error')
- `progress` - Progress value (0.0 - 1.0)
- `elapsed` - Seconds elapsed since job start
- `estimated_remaining` - Estimated seconds remaining (optional)
- `error_message` - Error details if status is 'error'

**Example:**
```tsx
const status = await songMapApi.getStatus(jobId);
console.log(`Progress: ${status.progress * 100}%`);
```

##### `getSongMap(jobId: string): Promise<SongMapResponse>`

Retrieve the completed Song Map.

**Parameters:**
- `jobId` - The job ID of a completed job

**Returns:**
- `job_id` - The job identifier
- `song_map` - The generated Song Map (backend format)
- `elapsed` - Total processing time in seconds

**Example:**
```tsx
const result = await songMapApi.getSongMap(jobId);
console.log('Song Map:', result.song_map);
```

##### `waitForCompletion(audioFile, onProgress?, pollInterval?): Promise<BackendSongMap>`

Upload a file and wait for completion with automatic polling.

**Parameters:**
- `audioFile` - The audio file to analyze
- `onProgress` - Optional callback for progress updates
- `pollInterval` - Polling interval in milliseconds (default: 1000)

**Returns:**
- Complete Song Map in backend format

**Example:**
```tsx
const songMap = await songMapApi.waitForCompletion(
  file,
  (status) => {
    console.log(`${status.progress * 100}% - ${status.elapsed}s elapsed`);
  },
  1000
);
```

##### `convertToFrontendFormat(backendMap, title?, artist?): SongMap`

Convert backend Song Map format to frontend format.

**Parameters:**
- `backendMap` - Song Map from backend
- `title` - Optional song title
- `artist` - Optional artist name

**Returns:**
- Song Map in frontend format (simplified)

**Example:**
```tsx
const frontendMap = songMapApi.convertToFrontendFormat(
  backendMap,
  'Song Title',
  'Artist Name'
);
```

### useSongMapUpload Hook

React hook that manages the upload process with built-in state management.

#### Return Value

```tsx
interface UseSongMapUploadResult {
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
```

#### Usage Example

```tsx
const {
  uploadSong,
  cancelUpload,
  reset,
  isUploading,
  progress,
  songMap,
  backendSongMap,
  error,
  jobId,
} = useSongMapUpload();

// Upload a file
await uploadSong(file, { title: 'My Song', artist: 'My Artist' });

// Cancel upload
cancelUpload();

// Reset state
reset();
```

## Type Definitions

### Backend Types

The backend uses a more detailed Song Map format:

```typescript
interface BackendSongMap {
  id: string;
  duration_sec: number;
  tempo: {
    bpm_global: number;
    curve?: [number, number][];
    confidence?: number;
  };
  beats: number[];
  downbeats: number[];
  meter: {
    numerator: number;
    denominator: number;
  };
  chords: Array<{
    start: number;
    end: number;
    label: string;
    conf?: number;
  }>;
  lyrics: Array<{
    start: number;
    end: number;
    text: string;
    conf?: number;
  }>;
  key?: Array<{
    start: number;
    end: number;
    tonic: string;
    mode: string;
    conf?: number;
  }>;
  sections?: Array<{
    start: number;
    end: number;
    label: string;
  }>;
  performance?: {
    melody?: any[];
    bass?: any[];
  };
}
```

### Frontend Types

The frontend uses a simplified format (from `/types.ts`):

```typescript
interface SongMap {
  title: string;
  artist: string;
  key: string;
  bpm: number;
  sections: Array<{
    name: string;
    lines: Array<{
      syllables: Array<{
        text: string;
        startTime: number;
        duration: number;
        chord?: string;
      }>;
    }>;
  }>;
}
```

## Type Mismatches & Conversion

### Key Differences

1. **Backend**: Detailed timing arrays (`beats`, `downbeats`, `chords`, `lyrics`)
   **Frontend**: Simplified sections/lines/syllables structure

2. **Backend**: Multiple key segments with confidence scores
   **Frontend**: Single key string (e.g., "C major")

3. **Backend**: BPM with tempo curve
   **Frontend**: Single BPM value

4. **Backend**: Word-level lyrics with timestamps
   **Frontend**: Syllable-level with durations

### Conversion Strategy

The `convertToFrontendFormat()` method handles the conversion:

- Extracts first key segment and formats as string
- Rounds BPM to integer
- Converts word-level lyrics to syllable-level sections
- Maps chords to syllables by timestamp
- Groups lyrics into lines based on timing gaps

**Note:** The current conversion is simplified. You may want to enhance it to:
- Use backend's `sections` array for structure
- Better handle syllable splitting
- Preserve tempo curves
- Include confidence scores
- Support multiple key changes

## Error Handling

The API client throws `SongMapApiError` for all errors:

```typescript
try {
  await songMapApi.analyzeSong(file);
} catch (error) {
  if (error instanceof SongMapApiError) {
    console.error('API Error:', error.message);
    console.error('Status Code:', error.statusCode);
    console.error('Details:', error.details);
  }
}
```

## Testing

To test the API client:

1. Start the backend API:
   ```bash
   cd backend
   python -m src.services.orchestrator.api
   ```

2. Add the test component to your app:
   ```tsx
   import { SongMapUploadTest } from './components/SongMapUploadTest';

   function App() {
     return <SongMapUploadTest />;
   }
   ```

3. Navigate to the test page and upload `test_music.wav`

## Integration with Library

To automatically add uploaded songs to the library:

```tsx
import { useSongMapUpload } from '../hooks/useSongMapUpload';
import { libraryService } from '../services/libraryService';

function UploadAndSave() {
  const { uploadSong, songMap } = useSongMapUpload();

  const handleUpload = async (file: File) => {
    await uploadSong(file);
  };

  useEffect(() => {
    if (songMap) {
      libraryService.addSong(songMap, {
        tags: ['uploaded'],
        genre: 'auto-generated',
      });
    }
  }, [songMap]);

  return <div>Upload interface...</div>;
}
```

## Configuration

The API client defaults to `http://localhost:8000`. To use a different base URL:

```typescript
import { SongMapApiClient } from '../services/songMapApi';

// Create custom instance
const api = new SongMapApiClient('http://myserver:8000');

// Or set environment variable
const api = new SongMapApiClient(
  process.env.REACT_APP_API_URL || 'http://localhost:8000'
);
```

## Performance Considerations

- **Polling Interval**: Default 1000ms (1 second). Adjust based on expected processing time.
- **File Size**: Large files may take minutes to process.
- **Network**: Upload time depends on file size and connection speed.
- **Cancellation**: Use `cancelUpload()` to stop polling (server-side job continues).

## Future Enhancements

Potential improvements to consider:

1. **WebSocket Support**: Real-time progress updates without polling
2. **Batch Upload**: Process multiple files simultaneously
3. **Resume Support**: Resume interrupted uploads
4. **Advanced Conversion**: Better backend-to-frontend format mapping
5. **Caching**: Cache Song Maps to avoid re-processing
6. **Metadata Extraction**: Auto-detect title/artist from audio metadata
7. **Preview**: Generate preview before full processing

## Troubleshooting

### "Network error: Failed to fetch"
- Backend is not running
- Backend is running on a different port
- CORS is not configured

### "Upload failed: 422"
- Invalid file format
- File is corrupted
- File is too large

### "Status check failed: 404"
- Job ID not found (may have expired)
- Backend restarted (jobs are in-memory)

### Progress stuck at 0%
- Backend is processing but not updating status
- Check backend logs for errors
- Try a shorter audio file
