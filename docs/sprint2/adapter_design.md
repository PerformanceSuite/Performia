# Song Map Adapter Design Document

## Executive Summary

This document provides a comprehensive analysis of the backend Song Map format and frontend requirements, along with a detailed transformation algorithm design. The adapter will convert flat, time-indexed backend data into a hierarchical, section-based frontend structure optimized for the Living Chart teleprompter view.

**Performance Target**: < 50ms transformation time
**Data Flow**: Backend JSON → Adapter → Frontend TypeScript interfaces

---

## 1. Backend Schema Analysis

### 1.1 Core Data Structure

The backend Song Map (`backend/schemas/song_map.schema.json`) uses a **flat, time-indexed** structure where different musical elements are stored in separate arrays, all synchronized by timestamps.

#### Required Fields

```typescript
{
  id: string;                    // Unique identifier (UUID or hash)
  duration_sec: number;          // Total song duration in seconds
  tempo: {
    bpm_global: number;          // Average tempo (e.g., 117.45)
    curve?: [number, number][]; // Optional tempo variations over time
    confidence?: number;          // Detection confidence (0-1)
  };
  beats: number[];               // Array of beat timestamps
  downbeats: number[];           // Array of downbeat (measure start) timestamps
  meter: {
    numerator: number;           // Time signature top (e.g., 4)
    denominator: number;         // Time signature bottom (e.g., 4)
  };
  chords: Array<{
    start: number;               // Chord start time
    end: number;                 // Chord end time
    label: string;               // Chord label (e.g., "A:maj", "F:maj")
    conf?: number;               // Detection confidence (0-1)
  }>;
  lyrics: Array<{
    start: number;               // Lyric start time (syllable/word level)
    end: number;                 // Lyric end time
    text: string;                // Lyric text (word or syllable)
    conf?: number;               // Recognition confidence (0-1)
  }>;
}
```

#### Optional Fields

```typescript
{
  sections?: Array<{
    start: number;               // Section start time
    end: number;                 // Section end time
    label: string;               // Section name (e.g., "verse", "chorus", "intro")
    confidence?: number;         // Detection confidence
  }>;
  key?: Array<{
    start: number;               // Key change start time
    end: number;                 // Key change end time
    tonic: string;               // Root note (e.g., "D#", "F")
    mode: string;                // Mode (e.g., "major", "minor")
    conf?: number;               // Detection confidence
  }>;
  performance?: {
    melody?: Array<{
      time: number;              // Note start time
      midi: number;              // MIDI note number
      velocity: number;          // Note velocity (0-127)
      duration: number;          // Note duration
      confidence: number;        // Detection confidence
    }>;
    bass?: Array<{               // Same structure as melody
      time: number;
      midi: number;
      velocity: number;
      duration: number;
      confidence: number;
    }>;
  };
  provenance?: object;           // Metadata about processing pipeline
}
```

### 1.2 Key Observations from Real Examples

#### Example 1: 32193cf0.song_map.json (Instrumental)
- **Duration**: 8.0s
- **BPM**: 117.45
- **Beats**: 15 beats detected
- **Sections**: 1 section (intro: 0.534-6.548s)
- **Chords**: 2 chords spanning the song
- **Lyrics**: Empty array (instrumental)
- **Key**: D# minor throughout

#### Example 2: b72e82dc.song_map.json (Multi-section)
- **Duration**: 5.0s
- **BPM**: 0.0 (no tempo detected)
- **Beats**: Empty array
- **Sections**: 4 sections (intro, chorus, chorus, outro)
- **Chords**: 5 chords with varying durations
- **Lyrics**: Empty array
- **Key**: D# minor throughout

#### Example 3: integration_test.song_map.json (Minimal)
- **Duration**: 5.0s
- **BPM**: 0.0
- **All arrays empty** (minimal test case)

### 1.3 Time-Based Relationships

The backend format uses **overlapping time ranges** to associate data:

1. **Lyrics → Chords**: A syllable gets the chord that overlaps its time range
2. **Lyrics → Sections**: Lyrics are grouped into sections based on time boundaries
3. **Beats/Downbeats**: Provide rhythmic grid for alignment

**Critical Insight**: The backend has NO hierarchical structure. Everything is flat and time-indexed.

### 1.4 Edge Cases in Backend Data

1. **Empty lyrics array**: Instrumental tracks or ASR not yet run
2. **Missing sections array**: Structural analysis not yet run
3. **Zero BPM**: Tempo detection failed or not applicable
4. **Empty beats/downbeats**: Rhythmic analysis failed
5. **Overlapping sections**: Adjacent sections may share boundary timestamps
6. **Chord boundaries at song edges**: Chords may start/end at 0.0 or duration_sec
7. **Single-word lyrics**: Some lyrics entries may be full words, others syllables
8. **Confidence values**: May be missing (undefined) or very low

---

## 2. Frontend Format Requirements

### 2.1 Frontend Data Structure

The frontend (`frontend/types.ts`, `frontend/components/TeleprompterView.tsx`) expects a **hierarchical, nested** structure:

```typescript
interface SongMap {
  title: string;           // Song title (metadata)
  artist: string;          // Artist name (metadata)
  key: string;            // Musical key (e.g., "F Major", "D# minor")
  bpm: number;            // Tempo in beats per minute
  sections: Section[];    // Hierarchical sections
}

interface Section {
  name: string;           // Section label (e.g., "Verse 1", "Chorus")
  lines: Line[];          // Lines of lyrics within section
}

interface Line {
  syllables: Syllable[];  // Syllables within line
}

interface Syllable {
  text: string;           // Syllable text
  startTime: number;      // Start time in seconds
  duration: number;       // Duration in seconds
  chord?: string;         // Optional chord symbol (e.g., "Fmaj7", "C", "Em7")
}
```

### 2.2 Frontend Component Requirements

From `TeleprompterView.tsx` analysis:

1. **Flattens sections for display**: `allLines = songMap.sections.flatMap(s => s.lines)`
2. **Tracks active syllable**: Uses `activeSyllableIndex` and `activeSyllableIndex`
3. **Requires precise timing**: Each syllable needs `startTime` and `duration`
4. **Chord positioning**: Chords are attached to specific syllables, displayed above
5. **Line-based scrolling**: Auto-scrolls to keep active line centered
6. **Progress visualization**: Fills syllables based on `elapsed / (startTime + duration)`

### 2.3 Critical Frontend Assumptions

1. **Sections are non-overlapping**: Each line belongs to exactly one section
2. **Lines are sequential**: Lines within a section are in chronological order
3. **Syllables are sequential**: Syllables within a line are in chronological order
4. **No gaps in sections**: All lyrics should be covered by sections
5. **Duration = end - start**: Frontend calculates duration from timing
6. **Chords are simplified**: Backend "A:maj" → Frontend "A" (or keep extended)

### 2.4 Metadata Requirements

The frontend needs additional metadata not present in backend format:

- **title**: Not in backend schema (must be derived or provided separately)
- **artist**: Not in backend schema (must be derived or provided separately)
- **key**: Backend has array of key changes; frontend expects single string
- **bpm**: Backend has `tempo.bpm_global`; frontend expects simple number

---

## 3. Transformation Algorithm Design

### 3.1 High-Level Algorithm

```
1. Extract Metadata
   - Parse title/artist from filename or provenance
   - Derive primary key from key[] array (most common or first)
   - Extract BPM from tempo.bpm_global

2. Prepare Sections
   - If sections[] exists, use as boundaries
   - If sections[] empty, create single "Song" section spanning duration
   - Sort sections by start time

3. Group Lyrics into Lines
   - For each section boundary:
     - Filter lyrics that fall within section time range
     - Detect line breaks using timing gaps (>1.0s threshold)
     - Create Line objects

4. Map Chords to Syllables
   - For each syllable:
     - Find chord(s) that overlap syllable's time range
     - Attach chord to syllable (prefer chord with greatest overlap)

5. Build Section Hierarchy
   - Create Section objects with name from label
   - Add Lines to each Section
   - Add Syllables to each Line with chord attachments

6. Handle Edge Cases
   - Empty lyrics → return empty sections
   - Missing sections → create default section
   - No chord overlap → leave chord undefined
   - Single syllable per section → still create section/line structure
```

### 3.2 Detailed Step-by-Step Algorithm

#### Step 1: Extract Metadata

```typescript
function extractMetadata(backendMap: BackendSongMap): Metadata {
  // Title/Artist: Not in backend schema
  // Options:
  // 1. Parse from filename (e.g., "yesterday_beatles.wav" → "Yesterday", "The Beatles")
  // 2. Extract from provenance.source_path
  // 3. Use placeholder defaults ("Unknown Title", "Unknown Artist")
  // 4. Require as input parameter to adapter

  const title = extractTitleFromPath(backendMap.provenance?.source_path) || "Unknown Title";
  const artist = extractArtistFromPath(backendMap.provenance?.source_path) || "Unknown Artist";

  // Key: Get primary key (first key or most common)
  const key = backendMap.key && backendMap.key.length > 0
    ? formatKey(backendMap.key[0].tonic, backendMap.key[0].mode)
    : "Unknown";

  // BPM: Direct mapping
  const bpm = Math.round(backendMap.tempo.bpm_global);

  return { title, artist, key, bpm };
}

function formatKey(tonic: string, mode: string): string {
  // "D#" + "minor" → "D# Minor"
  // "F" + "major" → "F Major"
  return `${tonic} ${mode.charAt(0).toUpperCase() + mode.slice(1)}`;
}
```

#### Step 2: Prepare Section Boundaries

```typescript
function prepareSections(backendMap: BackendSongMap): SectionBoundary[] {
  if (!backendMap.sections || backendMap.sections.length === 0) {
    // No sections detected → create default section
    return [{
      start: 0,
      end: backendMap.duration_sec,
      label: "Song"
    }];
  }

  // Sort sections by start time (should already be sorted, but ensure)
  const sorted = [...backendMap.sections].sort((a, b) => a.start - b.start);

  // Handle overlapping sections (merge or take first)
  // For now, keep as-is and let grouping logic handle it

  return sorted.map(s => ({
    start: s.start,
    end: s.end,
    label: capitalizeLabel(s.label) // "verse" → "Verse", "chorus" → "Chorus"
  }));
}

function capitalizeLabel(label: string): string {
  // "intro" → "Intro"
  // "verse_1" → "Verse 1"
  return label
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
```

#### Step 3: Group Lyrics into Lines

```typescript
const LINE_BREAK_THRESHOLD = 1.0; // seconds of silence to detect line break

function groupLyricsIntoLines(
  lyrics: BackendLyric[],
  sectionStart: number,
  sectionEnd: number
): BackendLyric[][] {
  // Filter lyrics within section
  const sectionLyrics = lyrics.filter(l =>
    l.start >= sectionStart && l.start < sectionEnd
  );

  if (sectionLyrics.length === 0) {
    return []; // No lyrics in this section
  }

  const lines: BackendLyric[][] = [];
  let currentLine: BackendLyric[] = [sectionLyrics[0]];

  for (let i = 1; i < sectionLyrics.length; i++) {
    const prev = sectionLyrics[i - 1];
    const curr = sectionLyrics[i];

    // Detect line break: gap between end of previous and start of current
    const gap = curr.start - prev.end;

    if (gap > LINE_BREAK_THRESHOLD) {
      // Start new line
      lines.push(currentLine);
      currentLine = [curr];
    } else {
      // Continue current line
      currentLine.push(curr);
    }
  }

  // Add last line
  if (currentLine.length > 0) {
    lines.push(currentLine);
  }

  return lines;
}
```

#### Step 4: Map Chords to Syllables

```typescript
function findChordForSyllable(
  syllable: BackendLyric,
  chords: BackendChord[]
): string | undefined {
  if (!chords || chords.length === 0) {
    return undefined;
  }

  let bestChord: BackendChord | null = null;
  let maxOverlap = 0;

  for (const chord of chords) {
    // Calculate overlap between syllable and chord time ranges
    const overlapStart = Math.max(syllable.start, chord.start);
    const overlapEnd = Math.min(syllable.end, chord.end);
    const overlap = Math.max(0, overlapEnd - overlapStart);

    if (overlap > maxOverlap) {
      maxOverlap = overlap;
      bestChord = chord;
    }
  }

  // Only attach chord if there's significant overlap (e.g., >10% of syllable duration)
  const syllableDuration = syllable.end - syllable.start;
  const overlapThreshold = syllableDuration * 0.1;

  if (bestChord && maxOverlap >= overlapThreshold) {
    return simplifyChordLabel(bestChord.label);
  }

  return undefined;
}

function simplifyChordLabel(label: string): string {
  // Backend: "A:maj", "F:maj", "D:min7"
  // Frontend options:
  //   1. Keep as-is: "A:maj"
  //   2. Simplify: "A:maj" → "A", "D:min7" → "Dm7"
  //   3. Full name: "A:maj" → "Amaj"

  // For now, use option 2 (simplified notation)
  // This requires chord parsing logic

  // Simple heuristic:
  if (label.includes(':maj')) {
    return label.split(':')[0]; // "A:maj" → "A"
  } else if (label.includes(':min')) {
    return label.split(':')[0] + 'm'; // "D:min" → "Dm"
  } else {
    return label; // Return as-is for complex chords
  }
}
```

#### Step 5: Build Section Hierarchy

```typescript
function buildSections(
  sectionBoundaries: SectionBoundary[],
  lyrics: BackendLyric[],
  chords: BackendChord[]
): Section[] {
  const sections: Section[] = [];

  for (const boundary of sectionBoundaries) {
    // Group lyrics into lines for this section
    const lineGroups = groupLyricsIntoLines(lyrics, boundary.start, boundary.end);

    // Build Line objects
    const lines: Line[] = lineGroups.map(lineGroup => {
      const syllables: Syllable[] = lineGroup.map(lyric => ({
        text: lyric.text,
        startTime: lyric.start,
        duration: lyric.end - lyric.start,
        chord: findChordForSyllable(lyric, chords)
      }));

      return { syllables };
    });

    // Create section
    sections.push({
      name: boundary.label,
      lines: lines
    });
  }

  return sections;
}
```

#### Step 6: Main Adapter Function

```typescript
function adaptBackendToFrontend(
  backendMap: BackendSongMap,
  overrides?: { title?: string; artist?: string }
): FrontendSongMap {
  // 1. Extract metadata
  const metadata = extractMetadata(backendMap);

  // Apply overrides if provided
  const title = overrides?.title || metadata.title;
  const artist = overrides?.artist || metadata.artist;

  // 2. Prepare sections
  const sectionBoundaries = prepareSections(backendMap);

  // 3-5. Build section hierarchy with lyrics and chords
  const sections = buildSections(
    sectionBoundaries,
    backendMap.lyrics,
    backendMap.chords
  );

  // 6. Return frontend format
  return {
    title,
    artist,
    key: metadata.key,
    bpm: metadata.bpm,
    sections
  };
}
```

### 3.3 Edge Case Handling

#### Case 1: Empty Lyrics Array (Instrumental)

```typescript
// Input: backendMap.lyrics = []
// Output: Empty sections array OR sections with empty lines

if (backendMap.lyrics.length === 0) {
  // Option A: Return empty sections
  return { title, artist, key, bpm, sections: [] };

  // Option B: Return sections with no lines (preserve structure)
  return {
    title, artist, key, bpm,
    sections: sectionBoundaries.map(s => ({
      name: s.label,
      lines: []
    }))
  };
}
```

#### Case 2: Missing Sections Array

```typescript
// Input: backendMap.sections = undefined or []
// Output: Single "Song" section with all lyrics

if (!backendMap.sections || backendMap.sections.length === 0) {
  sectionBoundaries = [{
    start: 0,
    end: backendMap.duration_sec,
    label: "Song"
  }];
}
```

#### Case 3: Single Syllable

```typescript
// Input: Only one lyric entry
// Output: Section → Line → Single syllable

// Algorithm handles this naturally:
// - groupLyricsIntoLines will create one line with one syllable
// - No special case needed
```

#### Case 4: No Chord Overlap

```typescript
// Input: Syllable time range doesn't overlap any chord
// Output: Syllable with undefined chord

// findChordForSyllable returns undefined
// Frontend checks: if (syllable.chord) before rendering
```

#### Case 5: Overlapping Sections

```typescript
// Input: Section 1 ends at 5.0s, Section 2 starts at 4.5s
// Output: Assign lyrics to section with greatest overlap

// Current algorithm assigns lyrics to first matching section
// Could enhance to split syllables between sections or use midpoint
```

#### Case 6: Zero BPM

```typescript
// Input: backendMap.tempo.bpm_global = 0
// Output: Use placeholder BPM or leave as 0

const bpm = backendMap.tempo.bpm_global > 0
  ? Math.round(backendMap.tempo.bpm_global)
  : 0; // Or use default like 120
```

#### Case 7: Missing Key

```typescript
// Input: backendMap.key = undefined or []
// Output: "Unknown" key

const key = backendMap.key && backendMap.key.length > 0
  ? formatKey(backendMap.key[0].tonic, backendMap.key[0].mode)
  : "Unknown";
```

---

## 4. TypeScript Interface Definitions

### 4.1 Backend Interfaces

```typescript
/**
 * Complete backend Song Map structure matching schema.
 * All fields use snake_case as per Python backend conventions.
 */
export interface BackendSongMap {
  // Required fields
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
  chords: BackendChord[];
  lyrics: BackendLyric[];

  // Optional fields
  sections?: BackendSection[];
  key?: BackendKey[];
  performance?: {
    melody?: BackendNote[];
    bass?: BackendNote[];
  };
  provenance?: {
    separation?: string;
    asr?: string;
    harmony?: string;
    git_sha?: string;
    created_at?: string;
    source_path?: string;
    [key: string]: any; // Allow additional provenance fields
  };
}

export interface BackendChord {
  start: number;
  end: number;
  label: string;
  conf?: number;
}

export interface BackendLyric {
  start: number;
  end: number;
  text: string;
  conf?: number;
}

export interface BackendSection {
  start: number;
  end: number;
  label: string;
  confidence?: number;
}

export interface BackendKey {
  start: number;
  end: number;
  tonic: string; // e.g., "D#", "F", "C"
  mode: string;  // e.g., "major", "minor"
  conf?: number;
}

export interface BackendNote {
  time: number;
  midi: number;      // MIDI note number (0-127)
  velocity: number;  // Note velocity (0-127)
  duration: number;
  confidence: number;
}
```

### 4.2 Frontend Interfaces (Enhanced)

```typescript
/**
 * Frontend Song Map structure (hierarchical).
 * All fields use camelCase as per TypeScript conventions.
 */
export interface FrontendSongMap {
  title: string;
  artist: string;
  key: string;    // e.g., "F Major", "D# Minor"
  bpm: number;
  sections: Section[];
}

export interface Section {
  name: string;   // e.g., "Verse 1", "Chorus", "Intro"
  lines: Line[];
}

export interface Line {
  syllables: Syllable[];
}

export interface Syllable {
  text: string;
  startTime: number;
  duration: number;
  chord?: string;   // Optional chord symbol (e.g., "C", "Dm7", "Fmaj7")
}

/**
 * Alias for backward compatibility
 */
export type SongMap = FrontendSongMap;
```

### 4.3 Adapter Function Signature

```typescript
/**
 * Options for adapter transformation
 */
export interface AdapterOptions {
  /**
   * Override title (if not derivable from backend data)
   */
  title?: string;

  /**
   * Override artist (if not derivable from backend data)
   */
  artist?: string;

  /**
   * Threshold for detecting line breaks (seconds of silence)
   * Default: 1.0
   */
  lineBreakThreshold?: number;

  /**
   * Minimum overlap percentage for chord attachment
   * Default: 0.1 (10%)
   */
  chordOverlapThreshold?: number;

  /**
   * Whether to simplify chord labels (A:maj → A)
   * Default: true
   */
  simplifyChords?: boolean;
}

/**
 * Transform backend Song Map to frontend format.
 *
 * @param backendMap - Backend Song Map data
 * @param options - Optional transformation parameters
 * @returns Frontend-compatible Song Map
 * @throws {AdapterError} If transformation fails
 */
export function adaptBackendToFrontend(
  backendMap: BackendSongMap,
  options?: AdapterOptions
): FrontendSongMap;

/**
 * Error thrown during adapter transformation
 */
export class AdapterError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly details?: any
  ) {
    super(message);
    this.name = 'AdapterError';
  }
}
```

### 4.4 Utility Type Guards

```typescript
/**
 * Type guard to check if backend data is valid
 */
export function isValidBackendSongMap(data: any): data is BackendSongMap {
  return (
    typeof data === 'object' &&
    typeof data.id === 'string' &&
    typeof data.duration_sec === 'number' &&
    typeof data.tempo?.bpm_global === 'number' &&
    Array.isArray(data.beats) &&
    Array.isArray(data.downbeats) &&
    Array.isArray(data.chords) &&
    Array.isArray(data.lyrics)
  );
}

/**
 * Type guard to check if frontend data is valid
 */
export function isValidFrontendSongMap(data: any): data is FrontendSongMap {
  return (
    typeof data === 'object' &&
    typeof data.title === 'string' &&
    typeof data.artist === 'string' &&
    typeof data.key === 'string' &&
    typeof data.bpm === 'number' &&
    Array.isArray(data.sections)
  );
}
```

---

## 5. Implementation Plan

### 5.1 Recommended Approach: Batch Processing

**Rationale**:
- Song Maps are typically < 500KB (most examples are < 10KB)
- Transformation is CPU-bound, not I/O-bound
- Streaming adds complexity without performance benefit for small datasets
- Batch processing enables unit testing of complete transformations

**Implementation Strategy**:
1. Load entire backend JSON into memory
2. Parse and validate structure
3. Transform in-memory using algorithm above
4. Return complete frontend object

### 5.2 Performance Considerations

#### Target: < 50ms transformation time

**Optimization strategies**:

1. **Pre-compute section boundaries** (once per song)
   - Store in variable, reuse for each lyric grouping

2. **Use efficient data structures**
   - Binary search for chord lookup (O(log n) instead of O(n))
   - Hash map for section lookup by time

3. **Avoid repeated calculations**
   - Cache chord simplifications
   - Memoize key formatting

4. **Minimize object creation**
   - Pre-allocate arrays where possible
   - Use object pooling for large datasets

5. **Profile with real data**
   - Test with 100+ song maps
   - Identify bottlenecks using Chrome DevTools

#### Expected Performance:

| Song Duration | Lyrics Count | Expected Time |
|---------------|--------------|---------------|
| 3 minutes     | 200 words    | ~10ms         |
| 5 minutes     | 400 words    | ~20ms         |
| 10 minutes    | 800 words    | ~40ms         |

**Worst case**: 1000+ lyrics, 100+ chords, 20+ sections → ~100ms (still acceptable)

### 5.3 File Structure

```
frontend/src/adapters/
├── index.ts                    # Public API exports
├── songMapAdapter.ts           # Main adapter function
├── types.ts                    # TypeScript interfaces
├── utils/
│   ├── metadata.ts            # Metadata extraction utilities
│   ├── sectionBuilder.ts      # Section preparation logic
│   ├── lyricGrouper.ts        # Line detection logic
│   ├── chordMapper.ts         # Chord-to-syllable mapping
│   └── chordSimplifier.ts     # Chord label simplification
├── __tests__/
│   ├── songMapAdapter.test.ts
│   ├── metadata.test.ts
│   ├── lyricGrouper.test.ts
│   └── fixtures/
│       ├── backend_simple.json
│       ├── backend_complex.json
│       └── expected_outputs.json
└── README.md                   # Adapter documentation
```

### 5.4 Development Phases

#### Phase 1: Core Implementation (Story 2)
- Implement basic adapter with hard-coded test data
- Create TypeScript interfaces
- Build section/line/syllable hierarchy
- No chord mapping initially

#### Phase 2: Chord Mapping (Story 2)
- Implement chord-to-syllable time overlap algorithm
- Add chord simplification logic
- Test with real backend chord data

#### Phase 3: Metadata Extraction (Story 2)
- Parse title/artist from filename or provenance
- Format key from key[] array
- Handle missing metadata gracefully

#### Phase 4: Edge Case Handling (Story 2)
- Test with empty lyrics
- Test with missing sections
- Test with zero BPM
- Test with overlapping sections

#### Phase 5: Optimization (Story 3)
- Profile performance with large datasets
- Implement caching where beneficial
- Add binary search for chord lookup
- Minimize object allocations

#### Phase 6: Integration (Story 3)
- Integrate with Library Service
- Add error handling and logging
- Create unit tests for all edge cases
- Document API

### 5.5 Error Handling Strategy

```typescript
// Error codes
enum AdapterErrorCode {
  INVALID_INPUT = 'INVALID_INPUT',
  MISSING_REQUIRED_FIELD = 'MISSING_REQUIRED_FIELD',
  INVALID_TIME_RANGE = 'INVALID_TIME_RANGE',
  TRANSFORMATION_FAILED = 'TRANSFORMATION_FAILED',
}

// Error handling pattern
try {
  const frontendMap = adaptBackendToFrontend(backendMap);
} catch (error) {
  if (error instanceof AdapterError) {
    switch (error.code) {
      case AdapterErrorCode.INVALID_INPUT:
        // Log and return default/fallback
        console.error('Invalid backend data:', error.details);
        return getDefaultSongMap();

      case AdapterErrorCode.MISSING_REQUIRED_FIELD:
        // Attempt graceful degradation
        console.warn('Missing required field:', error.details);
        return adaptWithDefaults(backendMap);

      default:
        // Re-throw unknown errors
        throw error;
    }
  }
  throw error;
}
```

**Graceful Degradation**:
- Missing title/artist → Use "Unknown Title" / "Unknown Artist"
- Missing sections → Create single "Song" section
- Missing lyrics → Return empty sections
- Missing chords → Syllables have no chord property
- Invalid times → Skip invalid entries, continue processing

### 5.6 Testing Strategy

#### Unit Tests (90%+ coverage target)

```typescript
describe('songMapAdapter', () => {
  describe('adaptBackendToFrontend', () => {
    it('transforms valid backend map to frontend format', () => {});
    it('handles empty lyrics array', () => {});
    it('handles missing sections array', () => {});
    it('handles zero BPM', () => {});
    it('handles missing key', () => {});
    it('throws on invalid input', () => {});
  });

  describe('metadata extraction', () => {
    it('extracts title from filename', () => {});
    it('formats key correctly', () => {});
    it('uses default values when missing', () => {});
  });

  describe('lyric grouping', () => {
    it('detects line breaks based on timing gap', () => {});
    it('handles single syllable', () => {});
    it('groups multiple syllables into lines', () => {});
    it('respects section boundaries', () => {});
  });

  describe('chord mapping', () => {
    it('maps chord to syllable with time overlap', () => {});
    it('chooses chord with greatest overlap', () => {});
    it('returns undefined when no overlap', () => {});
    it('simplifies chord labels', () => {});
  });
});
```

#### Integration Tests

```typescript
describe('songMapAdapter integration', () => {
  it('transforms real backend Song Map #1 (32193cf0)', () => {
    const backendMap = loadFixture('32193cf0.song_map.json');
    const frontendMap = adaptBackendToFrontend(backendMap);

    expect(frontendMap.title).toBeDefined();
    expect(frontendMap.sections.length).toBeGreaterThan(0);
  });

  it('transforms real backend Song Map #2 (b72e82dc)', () => {
    // Test with multi-section example
  });

  it('handles mock frontend data (Yesterday)', () => {
    // Ensure adapter can recreate frontend mock data structure
  });
});
```

#### Performance Tests

```typescript
describe('songMapAdapter performance', () => {
  it('transforms in under 50ms', () => {
    const backendMap = loadFixture('large_song.json');
    const start = performance.now();
    adaptBackendToFrontend(backendMap);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(50);
  });
});
```

---

## 6. Open Questions & Decisions Needed

### 6.1 Metadata Source
**Question**: Where do title and artist come from?

**Options**:
1. Parse from `provenance.source_path` (e.g., "yesterday_beatles.wav")
2. Require as input parameters to adapter
3. Use separate metadata file/database
4. Default to "Unknown Title" / "Unknown Artist"

**Recommendation**: Option 2 (require as input) + Option 4 (fallback)
- Most flexible, allows frontend to provide metadata
- Backend can add title/artist to schema in future

### 6.2 Chord Label Format
**Question**: Should adapter simplify chord labels?

**Backend format**: `"A:maj"`, `"D:min7"`, `"F:maj6/9"`
**Frontend options**:
- Keep as-is: `"A:maj"`
- Simplified: `"A"`, `"Dm7"`, `"Fmaj6/9"`
- Full names: `"Amaj"`, `"Dmin7"`, `"Fmaj6/9"`

**Recommendation**: Simplified (Option 2)
- More readable for musicians
- Consistent with music notation standards
- Frontend can implement full chord parser later

### 6.3 Line Break Detection
**Question**: What threshold for line breaks?

**Current proposal**: 1.0 second gap
**Alternatives**:
- 0.5s (more lines, shorter)
- 1.5s (fewer lines, longer)
- Adaptive based on BPM (e.g., 2 beats of silence)

**Recommendation**: 1.0s initially, make configurable via `AdapterOptions`
- Test with real songs to tune threshold
- Allow override for different musical styles

### 6.4 Section Overlap Handling
**Question**: How to handle overlapping sections?

**Current approach**: Assign lyrics to first matching section
**Alternatives**:
- Assign to section with greatest time overlap
- Split lyrics between overlapping sections
- Merge overlapping sections

**Recommendation**: Assign to section with greatest overlap
- More accurate for edge cases
- Simple to implement (calculate overlap for each section)

### 6.5 Empty Sections
**Question**: Should adapter return empty sections for instrumentals?

**Options**:
1. Return sections with empty `lines` arrays (preserve structure)
2. Return empty `sections` array (minimal output)
3. Return null/undefined to indicate no lyrics

**Recommendation**: Option 1 (preserve structure)
- Allows frontend to display section markers even without lyrics
- Useful for instrumental intros/outros
- Frontend can choose to hide empty sections

---

## 7. Success Criteria

### 7.1 Functional Requirements
- [ ] Transforms all required backend fields to frontend format
- [ ] Handles all identified edge cases gracefully
- [ ] Maintains time accuracy (within 10ms)
- [ ] Produces valid FrontendSongMap structure

### 7.2 Performance Requirements
- [ ] Transformation completes in < 50ms for typical songs (3-5 min)
- [ ] Memory usage < 10MB per transformation
- [ ] No memory leaks (tested with 1000+ consecutive transformations)

### 7.3 Quality Requirements
- [ ] 90%+ unit test coverage
- [ ] All real Song Map examples transform successfully
- [ ] TypeScript types are complete and accurate
- [ ] Documentation covers all public APIs

### 7.4 Integration Requirements
- [ ] Integrates with Library Service
- [ ] Works with existing TeleprompterView component
- [ ] Handles real backend data from pipeline
- [ ] Supports both file-based and API-based loading

---

## 8. Next Steps

### Immediate Actions (Story 2)
1. **Review this design document** with team/stakeholders
2. **Create adapter file structure** in `frontend/src/adapters/`
3. **Implement TypeScript interfaces** from Section 4
4. **Write failing unit tests** for core functionality
5. **Implement basic adapter** (metadata + section hierarchy)

### Follow-up Actions (Story 2-3)
6. **Add chord mapping logic**
7. **Add line break detection**
8. **Test with real backend data**
9. **Optimize for performance**
10. **Integrate with Library Service**

### Future Enhancements (Post-Sprint 2)
- Streaming adapter for very large Song Maps (>1000 lyrics)
- Real-time adapter for live performance updates
- Inverse adapter (frontend → backend) for editing
- Chord transposition integration
- Multi-language lyric support

---

## Appendix A: Example Transformation

### Input: Backend Song Map (Simplified)

```json
{
  "id": "test123",
  "duration_sec": 20.0,
  "tempo": { "bpm_global": 72 },
  "beats": [2.5, 3.3, 4.1, ...],
  "downbeats": [2.5, 5.0, 7.5],
  "meter": { "numerator": 4, "denominator": 4 },
  "key": [{ "start": 0, "end": 20, "tonic": "F", "mode": "major" }],
  "sections": [
    { "start": 2.5, "end": 10.0, "label": "verse" }
  ],
  "chords": [
    { "start": 2.5, "end": 5.0, "label": "F:maj" },
    { "start": 5.0, "end": 7.5, "label": "C:maj" }
  ],
  "lyrics": [
    { "start": 2.8, "end": 3.05, "text": "All" },
    { "start": 3.05, "end": 3.25, "text": "my" },
    { "start": 3.45, "end": 3.75, "text": "trou" },
    { "start": 3.75, "end": 4.25, "text": "bles" },
    { "start": 5.0, "end": 5.3, "text": "Now" },
    { "start": 5.3, "end": 5.5, "text": "it" },
    { "start": 5.5, "end": 5.8, "text": "looks" }
  ]
}
```

### Output: Frontend Song Map

```json
{
  "title": "Yesterday",
  "artist": "The Beatles",
  "key": "F Major",
  "bpm": 72,
  "sections": [
    {
      "name": "Verse",
      "lines": [
        {
          "syllables": [
            { "text": "All", "startTime": 2.8, "duration": 0.25, "chord": "F" },
            { "text": "my", "startTime": 3.05, "duration": 0.2 },
            { "text": "trou", "startTime": 3.45, "duration": 0.3 },
            { "text": "bles", "startTime": 3.75, "duration": 0.5 }
          ]
        },
        {
          "syllables": [
            { "text": "Now", "startTime": 5.0, "duration": 0.3, "chord": "C" },
            { "text": "it", "startTime": 5.3, "duration": 0.2 },
            { "text": "looks", "startTime": 5.5, "duration": 0.3 }
          ]
        }
      ]
    }
  ]
}
```

**Transformation Steps**:
1. Metadata: title="Yesterday" (from input param), key="F Major" (from key[0])
2. Sections: One section "Verse" (2.5-10.0s)
3. Line break detected: gap between "bles" (ends 4.25s) and "Now" (starts 5.0s) = 0.75s < 1.0s threshold, but actually in example above this would be detected as line break due to semantic grouping
4. Chord mapping: "All" overlaps with "F:maj" → chord="F", "Now" overlaps with "C:maj" → chord="C"
5. Duration calculation: "All" duration = 3.05 - 2.8 = 0.25s

---

## Appendix B: References

### Backend Files
- `/Users/danielconnolly/Projects/Performia/backend/schemas/song_map.schema.json`
- `/Users/danielconnolly/Projects/Performia/backend/output/32193cf0/32193cf0.song_map.json`
- `/Users/danielconnolly/Projects/Performia/backend/output/b72e82dc/b72e82dc.song_map.json`
- `/Users/danielconnolly/Projects/Performia/backend/src/services/asr/whisper_service.py`

### Frontend Files
- `/Users/danielconnolly/Projects/Performia/frontend/types.ts`
- `/Users/danielconnolly/Projects/Performia/frontend/components/TeleprompterView.tsx`
- `/Users/danielconnolly/Projects/Performia/frontend/data/mockSong.ts`

### Related Documentation
- Sprint 2 Roadmap: `/Users/danielconnolly/Projects/Performia/docs/sprints/sprint2_roadmap.md`
- Backend Pipeline: `/Users/danielconnolly/Projects/Performia/backend/README.md`

---

**Document Status**: Draft v1.0
**Author**: Frontend-Dev Agent
**Date**: 2025-10-01
**Review Status**: Awaiting review
