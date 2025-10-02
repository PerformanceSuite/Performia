# Song Map Adapter Integration Guide

**Sprint 2, Story 3: Frontend Integration**

This guide explains how to use the Song Map adapter in frontend components to transform backend data into UI-ready format.

---

## Overview

The Song Map adapter transforms flat, time-indexed backend Song Maps into hierarchical frontend format suitable for rendering in the Living Chart teleprompter.

**Architecture:**
```
Backend Song Map → Adapter → Frontend Song Map → UI Components
  (flat)                      (hierarchical)
```

**Performance:**
- Transform time: <50ms for typical songs
- Render + Transform: <100ms total
- 110 unit tests, 94.55% coverage
- 11 integration tests

---

## Quick Start

### 1. Import the Adapter

```typescript
import {
  adaptBackendToFrontend,
  BackendSongMap,
  FrontendSongMap
} from '../types';
```

All adapter types and functions are re-exported from `/types.ts` for convenience.

### 2. Transform Backend Data

```typescript
// Load backend Song Map (from API, file, etc.)
const backendMap: BackendSongMap = await fetchSongMap('song-id');

// Transform to frontend format
const frontendMap: FrontendSongMap = adaptBackendToFrontend(backendMap, {
  title: 'Yesterday',
  artist: 'The Beatles'
});
```

### 3. Use in Components

```typescript
<TeleprompterView
  songMap={frontendMap}
  transpose={0}
  capo={0}
  chordDisplay="names"
  diagramVisibility={{}}
  onToggleDiagram={() => {}}
/>
```

---

## API Reference

### Core Functions

#### `adaptBackendToFrontend()`

Transforms backend Song Map to frontend format. **Main entry point.**

```typescript
function adaptBackendToFrontend(
  backendMap: BackendSongMap,
  options?: AdapterOptions
): FrontendSongMap
```

**Parameters:**
- `backendMap`: Backend Song Map from API/file
- `options`: Optional transformation parameters

**Options:**
```typescript
interface AdapterOptions {
  title?: string;              // Override title
  artist?: string;             // Override artist
  lineBreakThreshold?: number; // Gap for line breaks (default: 1.0s)
  chordOverlapThreshold?: number; // Chord mapping threshold (default: 0.1)
  simplifyChords?: boolean;    // Simplify chord labels (default: true)
}
```

**Returns:** `FrontendSongMap` - Hierarchical format ready for UI

**Throws:** `AdapterError` if transformation fails

**Example:**
```typescript
const frontendMap = adaptBackendToFrontend(backendMap, {
  title: 'Let It Be',
  artist: 'The Beatles',
  lineBreakThreshold: 1.5, // Longer gaps = new line
  simplifyChords: true     // A:maj → A
});
```

---

#### `adaptBackendToFrontendSafe()`

Safe version that returns `null` on error instead of throwing.

```typescript
function adaptBackendToFrontendSafe(
  backendMap: BackendSongMap,
  options?: AdapterOptions
): FrontendSongMap | null
```

Use this when:
- Batch processing multiple songs
- You don't want errors to stop execution
- You have a fallback UI

**Example:**
```typescript
const frontendMap = adaptBackendToFrontendSafe(backendMap);
if (!frontendMap) {
  // Show error UI or fallback
  return <ErrorMessage />;
}

return <TeleprompterView songMap={frontendMap} />;
```

---

#### `getEmptySongMap()`

Returns empty/fallback Song Map.

```typescript
function getEmptySongMap(
  title?: string,
  artist?: string
): FrontendSongMap
```

Use when no data is available or transformation fails.

**Example:**
```typescript
const fallbackMap = getEmptySongMap('Unknown', 'Unknown Artist');
```

---

#### `validateFrontendSongMap()`

Validates Song Map structure.

```typescript
function validateFrontendSongMap(
  frontendMap: FrontendSongMap
): boolean
```

**Example:**
```typescript
if (!validateFrontendSongMap(frontendMap)) {
  console.error('Invalid Song Map structure');
}
```

---

### Type Guards

#### `isValidBackendSongMap()`

Check if data is valid backend format.

```typescript
function isValidBackendSongMap(data: any): data is BackendSongMap
```

**Example:**
```typescript
const data = JSON.parse(jsonString);

if (isValidBackendSongMap(data)) {
  const frontendMap = adaptBackendToFrontend(data);
}
```

---

## Data Structures

### Backend Song Map (Input)

Flat, time-indexed format from Python backend:

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
  chords: BackendChord[];      // Flat chord array
  lyrics: BackendLyric[];      // Flat syllable array
  sections?: BackendSection[]; // Optional section markers
  key?: BackendKey[];
  performance?: {
    melody?: BackendNote[];
    bass?: BackendNote[];
  };
  provenance?: Record<string, any>;
}

interface BackendChord {
  start: number;  // Time in seconds
  end: number;
  label: string;  // e.g., "C:maj", "Dm7"
  conf?: number;
}

interface BackendLyric {
  start: number;  // Time in seconds
  end: number;
  text: string;   // Single syllable
  conf?: number;
}
```

### Frontend Song Map (Output)

Hierarchical format for UI rendering:

```typescript
interface FrontendSongMap {
  title: string;
  artist: string;
  key: string;        // Formatted: "F Major", "D# Minor"
  bpm: number;
  sections: Section[];
}

interface Section {
  name: string;       // e.g., "Verse 1", "Chorus"
  lines: Line[];
}

interface Line {
  syllables: Syllable[];
}

interface Syllable {
  text: string;
  startTime: number;  // Seconds
  duration: number;   // Seconds
  chord?: string;     // Simplified: "C", "Dm", "Fmaj7"
}
```

---

## Integration Patterns

### Pattern 1: Direct Loading

Load and transform immediately:

```typescript
async function loadSong(songId: string) {
  const backendMap = await fetchBackendSongMap(songId);
  const frontendMap = adaptBackendToFrontend(backendMap);
  setSongMap(frontendMap);
}
```

### Pattern 2: Library Service Integration

The library service automatically handles both formats:

```typescript
import { libraryService } from './services/libraryService';

// Import backend Song Map
const librarySong = libraryService.importBackendSongMap(backendMap, {
  title: 'Song Title',
  artist: 'Artist Name'
});

// Or import from JSON string (auto-detects format)
const librarySong = libraryService.importSong(jsonString);
```

The service will:
1. Detect if data is backend or frontend format
2. Transform backend → frontend automatically
3. Add to library with metadata

### Pattern 3: Safe Error Handling

Robust error handling with fallback:

```typescript
function SongViewer({ backendMap }) {
  const frontendMap = adaptBackendToFrontendSafe(backendMap);

  if (!frontendMap) {
    return <ErrorView message="Failed to load song" />;
  }

  return <TeleprompterView songMap={frontendMap} />;
}
```

### Pattern 4: Batch Processing

Process multiple songs efficiently:

```typescript
import { adaptMultipleSongMaps } from '../types';

const backendMaps = await fetchAllSongs();
const frontendMaps = adaptMultipleSongMaps(backendMaps, {
  simplifyChords: true
});
```

---

## Component Integration

### TeleprompterView

Already compatible! Just pass the transformed Song Map:

```typescript
<TeleprompterView
  songMap={frontendMap}
  transpose={0}
  capo={0}
  chordDisplay="names"
  diagramVisibility={{}}
  onToggleDiagram={() => {}}
/>
```

### LibraryView

Supports both import methods:

```typescript
// Import backend format
libraryService.importBackendSongMap(backendMap, {
  title: 'Song Title',
  artist: 'Artist'
});

// Import from JSON (auto-detects format)
libraryService.importSong(jsonString);
```

### SongMapDemo

Interactive demo showing transformation:

```typescript
// Access via UI: Click "Demo" button in header
// Or navigate to view='demo' state

<SongMapDemo />
```

Features:
- Load different backend examples
- View before/after transformation
- See performance metrics
- Live TeleprompterView rendering

---

## Troubleshooting

### Issue: "Invalid backend Song Map structure"

**Cause:** Missing required fields or invalid data

**Solution:**
```typescript
// Check if data is valid
if (!isValidBackendSongMap(data)) {
  console.error('Missing required fields:', data);
}

// Required fields:
// - id, duration_sec, tempo.bpm_global
// - beats, downbeats, meter, chords, lyrics
```

### Issue: Empty sections or no lyrics

**Cause:** Instrumental track or no lyrics detected

**Solution:**
```typescript
// The adapter handles this gracefully
const frontendMap = adaptBackendToFrontend(backendMap);

// Check result
if (frontendMap.sections.length === 0) {
  console.log('No lyrics - instrumental track');
}
```

### Issue: Chords not appearing

**Cause:** Chord timing doesn't overlap with syllables

**Solution:**
```typescript
// Adjust overlap threshold
const frontendMap = adaptBackendToFrontend(backendMap, {
  chordOverlapThreshold: 0.05 // More lenient (default: 0.1)
});
```

### Issue: Too many/few lines

**Cause:** Line break threshold too high/low

**Solution:**
```typescript
const frontendMap = adaptBackendToFrontend(backendMap, {
  lineBreakThreshold: 1.5 // Longer gaps = new line (default: 1.0)
});
```

---

## Performance Tips

1. **Transform once, use many times**
   ```typescript
   // Good: Transform once
   const frontendMap = adaptBackendToFrontend(backendMap);

   // Reuse in multiple components
   <TeleprompterView songMap={frontendMap} />
   <BlueprintView songMap={frontendMap} />
   ```

2. **Use safe version for batch processing**
   ```typescript
   const results = backendMaps.map(map =>
     adaptBackendToFrontendSafe(map)
   ).filter(Boolean); // Remove nulls
   ```

3. **Cache transformed results**
   ```typescript
   const cache = new Map<string, FrontendSongMap>();

   function getCachedSongMap(id: string, backendMap: BackendSongMap) {
     if (!cache.has(id)) {
       cache.set(id, adaptBackendToFrontend(backendMap));
     }
     return cache.get(id)!;
   }
   ```

---

## Testing

### Unit Tests

The adapter has 110 unit tests covering:
- Metadata extraction
- Chord mapping
- Lyric grouping
- Section building
- Edge cases

Run tests:
```bash
npm test
```

### Integration Tests

11 integration tests verify E2E flow:
- Backend → Frontend transformation
- UI component rendering
- Performance benchmarks
- Error handling

Location: `/src/__tests__/integration/songMapIntegration.test.tsx`

---

## Advanced Usage

### Custom Chord Simplification

```typescript
import { simplifyChordLabel } from '../types';

// Manual chord simplification
const chord = simplifyChordLabel('C:maj7'); // → "Cmaj7"
```

### Access Transformation Stats

```typescript
import { getChordMappingStats, getLineGroupingStats } from '../types';

const chordStats = getChordMappingStats(syllables, chords);
console.log(`Mapped ${chordStats.mappedCount}/${chordStats.totalSyllables} syllables`);
```

---

## Migration from Old Types

If you have existing code using old types:

### Before:
```typescript
interface Syllable {
  text: string;
  startTime: number;
  duration: number;
  chord?: string;
}
```

### After:
No changes needed! The adapter types are backward compatible.

All old types are now aliases to adapter types:
- `SongMap` → `FrontendSongMap`
- `Section`, `Line`, `Syllable` → Same

---

## Examples

### Example 1: Simple Load

```typescript
import { adaptBackendToFrontend } from '../types';

async function loadSong() {
  const response = await fetch('/api/songs/123');
  const backendMap = await response.json();

  const frontendMap = adaptBackendToFrontend(backendMap);
  setSongMap(frontendMap);
}
```

### Example 2: With Error Handling

```typescript
import { adaptBackendToFrontendSafe, getEmptySongMap } from '../types';

function useSongMap(backendMap: BackendSongMap | null) {
  const [songMap, setSongMap] = useState(getEmptySongMap());

  useEffect(() => {
    if (!backendMap) return;

    const transformed = adaptBackendToFrontendSafe(backendMap);
    setSongMap(transformed || getEmptySongMap('Error', 'Failed to load'));
  }, [backendMap]);

  return songMap;
}
```

### Example 3: Library Import

```typescript
import { libraryService } from './services/libraryService';

// From file input
async function handleFileUpload(file: File) {
  const text = await file.text();
  const librarySong = libraryService.importSong(text, {
    title: 'Uploaded Song',
    artist: 'Unknown'
  });

  if (librarySong) {
    console.log('Added to library:', librarySong.id);
  }
}
```

---

## Summary

✅ **Fast**: <50ms transformation, <100ms render + transform
✅ **Robust**: 121 tests, comprehensive error handling
✅ **Simple**: One function call to transform
✅ **Flexible**: Options for customization
✅ **Type-safe**: Full TypeScript support

**Key Function:**
```typescript
const frontendMap = adaptBackendToFrontend(backendMap);
```

That's it! You're ready to integrate backend Song Maps into your UI.

---

## Support

- Adapter code: `/frontend/src/adapters/`
- Tests: `/frontend/src/adapters/__tests__/`
- Integration tests: `/frontend/src/__tests__/integration/`
- Demo component: `/frontend/components/SongMapDemo.tsx`

For issues or questions, see the adapter test files for examples.
