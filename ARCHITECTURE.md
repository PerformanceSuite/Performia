# Architecture Documentation

Complete technical architecture reference for Performia.

---

## Table of Contents

- [System Overview](#system-overview)
- [Technology Stack](#technology-stack)
- [Architecture Patterns](#architecture-patterns)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [API Design](#api-design)
- [Frontend Architecture](#frontend-architecture)
- [Audio Pipeline](#audio-pipeline)
- [RAG Knowledge Base](#rag-knowledge-base)
- [Performance Optimizations](#performance-optimizations)
- [Security Considerations](#security-considerations)
- [Deployment Architecture](#deployment-architecture)
- [Future Architecture](#future-architecture)

---

## System Overview

Performia is a full-stack music performance system with three main layers:

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │         React Frontend (Port 5001)                │  │
│  │  • Living Chart • Blueprint View • Library        │  │
│  └───────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/WebSocket
┌───────────────────────▼─────────────────────────────────┐
│                   APPLICATION LAYER                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │      FastAPI Backend (Port 8000)                  │  │
│  │  • REST API • Job Management • WebSocket          │  │
│  └───────────┬────────────────────────────────────────┘  │
│              │                                           │
│  ┌───────────▼────────────────────────────────────────┐  │
│  │         Audio Pipeline Services                   │  │
│  │  ASR │ Beats │ Chords │ Melody │ Separation       │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                     DATA LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   SQLite     │  │  File System │  │   ChromaDB   │  │
│  │   Job Store  │  │  Song Maps   │  │  Knowledge   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Frontend, backend, and data layers are independent
2. **Microservices**: Audio pipeline services are modular and independent
3. **Async-First**: Python asyncio for non-blocking I/O
4. **Event-Driven**: WebSocket for real-time updates
5. **Stateless API**: RESTful design for scalability
6. **Progressive Enhancement**: Works offline after initial analysis

---

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.1.1 | UI framework |
| TypeScript | 5.8.2 | Type safety |
| Vite | 6.2.0 | Build tool |
| Tailwind CSS | 4.1.13 | Styling |
| Immer | 10.1.3 | Immutable state |

**Frontend Dependencies**:
```json
{
  "react": "^19.1.1",
  "react-dom": "^19.1.1",
  "immer": "^10.1.3"
}
```

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Backend language |
| FastAPI | 0.109.0+ | Web framework |
| Uvicorn | 0.27.0+ | ASGI server |
| SQLAlchemy | (via FastAPI) | ORM |
| Pydantic | 2.0.0+ | Data validation |

**Audio Processing**:
```python
openai-whisper==20231117  # ASR
librosa==0.10.0           # Audio analysis
demucs==4.0.0             # Source separation
torch==2.0.0              # Deep learning
```

**RAG Knowledge Base**:
```python
docling==2.55.1           # Document processing
chromadb                  # Vector database
sentence-transformers     # Embeddings
```

### Infrastructure Stack

- **Database**: SQLite (dev), PostgreSQL (prod)
- **File Storage**: Local filesystem, S3 (future)
- **Caching**: In-memory, Redis (future)
- **Message Queue**: Background tasks, Celery (future)
- **Container**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: GCP, Cloud Run

---

## Architecture Patterns

### 1. Model-View-Controller (MVC)

**Frontend (React)**:
- **Model**: TypeScript interfaces, Immer state
- **View**: React components
- **Controller**: Hooks, event handlers

**Backend (FastAPI)**:
- **Model**: Pydantic models, SQLAlchemy models
- **View**: JSON responses
- **Controller**: FastAPI route handlers

### 2. Repository Pattern

Data access abstracted through repositories:

```python
# backend/src/services/api/job_manager.py
class JobManager:
    """Repository for job data access"""

    async def create_job(self, job_id: str, audio_path: str) -> Job:
        """Create new job"""

    async def get_job(self, job_id: str) -> Optional[Job]:
        """Retrieve job by ID"""

    async def update_job_status(self, job_id: str, status: JobStatus):
        """Update job status"""
```

### 3. Service Layer Pattern

Business logic in service layer:

```python
# backend/src/services/orchestrator/async_pipeline.py
class AsyncPipeline:
    """Orchestrates audio analysis services"""

    async def run_full_pipeline(self, job_id: str, audio_path: str):
        """Run complete analysis pipeline"""

        # Service composition
        asr_result = await self.run_asr(audio_path)
        beats_result = await self.run_beats(audio_path)
        chords_result = await self.run_chords(audio_path)
        melody_result = await self.run_melody(audio_path)

        # Package into Song Map
        song_map = await self.package_song_map(
            asr_result, beats_result, chords_result, melody_result
        )

        return song_map
```

### 4. Factory Pattern

Song Map creation:

```python
# backend/src/services/packager/song_map_factory.py
class SongMapFactory:
    """Factory for creating Song Maps"""

    def create_song_map(self, analysis_results: Dict) -> SongMap:
        """Create Song Map from analysis results"""

        return SongMap(
            title=self._extract_title(analysis_results),
            sections=self._build_sections(analysis_results),
            tempo=self._calculate_tempo(analysis_results),
            key=self._detect_key(analysis_results)
        )
```

### 5. Observer Pattern

Real-time updates via WebSocket:

```typescript
// frontend/src/services/websocket.ts
class WebSocketService {
  private observers: Set<(event: Event) => void> = new Set();

  subscribe(callback: (event: Event) => void) {
    this.observers.add(callback);
  }

  notify(event: Event) {
    this.observers.forEach(observer => observer(event));
  }
}
```

---

## Core Components

### Backend Components

#### 1. API Server (`backend/src/services/api/main.py`)

FastAPI application serving REST endpoints:

```python
app = FastAPI(
    title="Performia Song Map API",
    description="REST API for generating Song Maps",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Routes
@app.post("/api/analyze")
async def analyze_audio(file: UploadFile) -> Dict:
    """Upload audio for Song Map generation"""

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str) -> Dict:
    """Get job status and progress"""

@app.get("/api/songmap/{job_id}")
async def get_song_map(job_id: str) -> Dict:
    """Get completed Song Map"""
```

#### 2. Job Manager (`backend/src/services/api/job_manager.py`)

Manages job lifecycle and persistence:

```python
class Job:
    job_id: str
    status: JobStatus  # PENDING, PROCESSING, COMPLETE, ERROR
    audio_path: str
    song_map_path: Optional[str]
    progress: float
    created_at: datetime
    updated_at: datetime
    elapsed: float
    error_message: Optional[str]

class JobManager:
    def __init__(self, output_dir: Path, upload_dir: Path):
        self.db_path = "jobs.db"
        self._init_database()

    async def create_job(self, job_id: str, audio_path: str) -> Job:
        """Create new job in database"""

    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: float = None
    ):
        """Update job status and progress"""

    async def load_song_map(self, job_id: str) -> Optional[Dict]:
        """Load Song Map JSON from filesystem"""
```

#### 3. Async Pipeline (`backend/src/services/orchestrator/async_pipeline.py`)

Orchestrates audio analysis services:

```python
class AsyncPipeline:
    """Async orchestrator for audio analysis pipeline"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.services = {
            'asr': ASRService(),
            'beats': BeatsService(),
            'chords': ChordsService(),
            'melody': MelodyService(),
            'separation': SeparationService(),
            'packager': PackagerService()
        }

    async def run_full_pipeline(
        self,
        job_id: str,
        audio_path: str
    ) -> Dict:
        """
        Run complete analysis pipeline:
        1. Source separation (optional)
        2. ASR (lyrics transcription)
        3. Beat detection
        4. Chord analysis
        5. Melody extraction
        6. Package Song Map
        """

        results = {}

        # Run services in parallel where possible
        async with asyncio.TaskGroup() as tg:
            asr_task = tg.create_task(self.run_asr(audio_path))
            beats_task = tg.create_task(self.run_beats(audio_path))

        # Services dependent on separation
        if separation_enabled:
            chords_task = tg.create_task(
                self.run_chords(separated_audio)
            )

        # Package results
        song_map = await self.package_results(results)

        return song_map
```

#### 4. Audio Services

Each service is independent and containerizable:

**ASR Service** (`backend/src/services/asr/`):
```python
class ASRService:
    """Whisper-based speech recognition"""

    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    async def transcribe(self, audio_path: str) -> Dict:
        """Transcribe audio to text with timing"""

        result = self.model.transcribe(
            audio_path,
            word_timestamps=True,
            language="en"
        )

        return {
            "text": result["text"],
            "segments": result["segments"],
            "words": self._extract_words(result)
        }
```

**Beat Detection** (`backend/src/services/beats_key/`):
```python
class BeatsService:
    """Beat and tempo detection using librosa"""

    async def detect_beats(self, audio_path: str) -> Dict:
        """Detect beats, tempo, and key"""

        y, sr = librosa.load(audio_path)

        # Tempo and beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Key detection
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = self._detect_key(chroma)

        return {
            "tempo": float(tempo),
            "beats": beat_times.tolist(),
            "key": key
        }
```

**Chord Analysis** (`backend/src/services/chords/`):
```python
class ChordsService:
    """Chord recognition and progression analysis"""

    async def analyze_chords(self, audio_path: str) -> Dict:
        """Analyze chord progressions"""

        # Chroma feature extraction
        y, sr = librosa.load(audio_path)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Chord template matching
        chords = self._match_chord_templates(chroma)

        return {
            "chords": chords,
            "chord_changes": self._detect_chord_changes(chords)
        }
```

### Frontend Components

#### 1. Living Chart (`frontend/src/components/LivingChart.tsx`)

Real-time performance view:

```typescript
interface LivingChartProps {
  songMap: SongMap;
  currentTime: number;
  settings: DisplaySettings;
}

export const LivingChart: React.FC<LivingChartProps> = ({
  songMap,
  currentTime,
  settings
}) => {
  // Find current syllable based on time
  const currentSyllable = useMemo(() =>
    findSyllableAtTime(songMap, currentTime),
    [songMap, currentTime]
  );

  // Auto-scroll to current position
  useEffect(() => {
    if (currentSyllable) {
      scrollToSyllable(currentSyllable);
    }
  }, [currentSyllable]);

  return (
    <div className="living-chart">
      {songMap.sections.map(section => (
        <Section
          key={section.id}
          section={section}
          currentSyllable={currentSyllable}
          settings={settings}
        />
      ))}
    </div>
  );
};
```

#### 2. Blueprint View (`frontend/src/components/BlueprintView.tsx`)

Song editing interface:

```typescript
export const BlueprintView: React.FC<BlueprintViewProps> = ({
  songMap,
  onUpdate
}) => {
  const [editMode, setEditMode] = useState<'view' | 'edit'>('view');

  // Immer-based state updates
  const updateSection = useCallback((sectionId: string, changes: Partial<Section>) => {
    const updatedSongMap = produce(songMap, draft => {
      const section = draft.sections.find(s => s.id === sectionId);
      if (section) {
        Object.assign(section, changes);
      }
    });
    onUpdate(updatedSongMap);
  }, [songMap, onUpdate]);

  return (
    <div className="blueprint-view">
      <SongHeader songMap={songMap} />
      <SectionList
        sections={songMap.sections}
        onUpdate={updateSection}
        editMode={editMode}
      />
    </div>
  );
};
```

#### 3. Library Service (`frontend/src/services/libraryService.ts`)

Song library management:

```typescript
class LibraryService {
  private songs: Map<string, SongMap> = new Map();

  async uploadSong(file: File): Promise<string> {
    // Upload to backend
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });

    const { job_id } = await response.json();

    // Poll for completion
    return this.pollJobStatus(job_id);
  }

  async getSong(songId: string): Promise<SongMap> {
    const response = await fetch(`/api/songmap/${songId}`);
    const { song_map } = await response.json();
    return song_map;
  }

  async searchSongs(query: string): Promise<SongMap[]> {
    // Client-side search through loaded songs
    return Array.from(this.songs.values())
      .filter(song =>
        song.title.toLowerCase().includes(query.toLowerCase()) ||
        song.artist.toLowerCase().includes(query.toLowerCase())
      );
  }
}
```

---

## Data Flow

### Song Upload and Analysis Flow

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│ Frontend │         │ Backend  │         │ Services │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                    │                     │
     │ POST /api/analyze  │                     │
     ├───────────────────>│                     │
     │                    │ Create Job          │
     │                    ├─────────────────>   │
     │                    │                     │
     │ job_id, status     │                     │
     │<───────────────────┤                     │
     │                    │                     │
     │                    │ Run ASR Service     │
     │                    ├────────────────────>│
     │                    │                     │
     │ GET /api/status    │                     │
     ├───────────────────>│                     │
     │ progress: 20%      │ ASR Complete        │
     │<───────────────────┤<────────────────────┤
     │                    │                     │
     │                    │ Run Beats Service   │
     │                    ├────────────────────>│
     │                    │                     │
     │ GET /api/status    │                     │
     ├───────────────────>│                     │
     │ progress: 40%      │ Beats Complete      │
     │<───────────────────┤<────────────────────┤
     │                    │                     │
     │                    │ Run Chords Service  │
     │                    ├────────────────────>│
     │ GET /api/status    │                     │
     ├───────────────────>│                     │
     │ progress: 60%      │ Chords Complete     │
     │<───────────────────┤<────────────────────┤
     │                    │                     │
     │                    │ Package Song Map    │
     │                    ├────────────────────>│
     │                    │                     │
     │ GET /api/status    │ Song Map Complete   │
     ├───────────────────>│<────────────────────┤
     │ status: COMPLETE   │                     │
     │<───────────────────┤                     │
     │                    │                     │
     │ GET /api/songmap   │                     │
     ├───────────────────>│                     │
     │ Song Map JSON      │                     │
     │<───────────────────┤                     │
     │                    │                     │
     │ Display in Living  │                     │
     │ Chart              │                     │
     │                    │                     │
```

### Real-Time Performance Flow

```
┌──────────┐         ┌──────────┐
│ Living   │         │ Audio    │
│ Chart    │         │ Player   │
└────┬─────┘         └────┬─────┘
     │                    │
     │ Play clicked       │
     ├───────────────────>│
     │                    │ Start playback
     │                    │
     │ timeupdate (60fps) │
     │<───────────────────┤
     │                    │
     │ Find current       │
     │ syllable           │
     │                    │
     │ Highlight syllable │
     │                    │
     │ Auto-scroll        │
     │                    │
     │ timeupdate         │
     │<───────────────────┤
     │                    │
```

---

## Database Schema

### SQLite Schema

**Jobs Table**:
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,  -- PENDING, PROCESSING, COMPLETE, ERROR
    audio_path TEXT NOT NULL,
    song_map_path TEXT,
    progress REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    elapsed REAL,
    error_message TEXT
);

CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
```

### Filesystem Structure

```
output/
├── {job_id}/
│   ├── {job_id}.song_map.json      # Final Song Map
│   ├── {job_id}.vocals.wav         # Separated vocals
│   ├── {job_id}.bass.wav           # Separated bass
│   ├── {job_id}.drums.wav          # Separated drums
│   ├── {job_id}.other.wav          # Other instruments
│   └── analysis/
│       ├── asr_result.json
│       ├── beats_result.json
│       ├── chords_result.json
│       └── melody_result.json
│
uploads/
└── {job_id}.{ext}                  # Original audio file
```

### Song Map JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["title", "artist", "sections"],
  "properties": {
    "title": { "type": "string" },
    "artist": { "type": "string" },
    "album": { "type": "string" },
    "key": { "type": "string" },
    "tempo": { "type": "number" },
    "duration": { "type": "number" },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "startTime", "lines"],
        "properties": {
          "name": { "type": "string" },
          "startTime": { "type": "number" },
          "lines": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "syllables": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["text", "startTime", "duration"],
                    "properties": {
                      "text": { "type": "string" },
                      "startTime": { "type": "number" },
                      "duration": { "type": "number" },
                      "chord": { "type": "string" },
                      "pitch": { "type": "number" }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## API Design

See [API.md](./API.md) for complete API reference.

### REST API Principles

1. **Resource-Based**: URLs represent resources (jobs, songmaps)
2. **HTTP Methods**: GET (read), POST (create), DELETE (delete)
3. **Stateless**: Each request contains all necessary information
4. **JSON**: All requests/responses use JSON
5. **HTTP Status Codes**: Proper use of 200, 201, 202, 400, 404, 500

### API Versioning

```
/api/v1/analyze     # Versioned endpoints
/api/v1/status
```

Current version: v1 (implicit, paths use `/api/` without version)

---

## Frontend Architecture

### Component Hierarchy

```
App
├── Router
│   ├── LibraryView
│   │   ├── SearchBar
│   │   ├── SongList
│   │   │   └── SongCard[]
│   │   └── UploadButton
│   │
│   ├── LivingChart
│   │   ├── Controls
│   │   ├── SectionList
│   │   │   └── Section[]
│   │   │       └── Line[]
│   │   │           └── Syllable[]
│   │   └── AudioPlayer
│   │
│   └── BlueprintView
│       ├── SongHeader
│       ├── SectionEditor[]
│       │   ├── LyricsEditor
│       │   └── ChordEditor
│       └── ToolBar
│
├── Settings
│   ├── DisplaySettings
│   ├── MusicalSettings
│   └── PerformanceSettings
│
└── GlobalState
    ├── SongMapStore
    ├── LibraryStore
    └── SettingsStore
```

### State Management

**Immer for Immutable Updates**:

```typescript
import { produce } from 'immer';

const updateSongMap = (songMap: SongMap, updater: (draft: SongMap) => void) => {
  return produce(songMap, draft => {
    updater(draft);
  });
};

// Usage
const newSongMap = updateSongMap(songMap, draft => {
  draft.sections[0].lines[0].syllables[0].text = "Updated";
});
```

### Performance Optimizations

1. **React.memo**: Prevent unnecessary re-renders
2. **useMemo**: Cache expensive computations
3. **useCallback**: Stable function references
4. **Virtualization**: Render only visible sections (future)
5. **Code Splitting**: Lazy load routes

---

## Audio Pipeline

### Pipeline Architecture

```
Audio File
    │
    ├─> Separation Service (Demucs) [Optional]
    │       │
    │       ├─> vocals.wav
    │       ├─> bass.wav
    │       ├─> drums.wav
    │       └─> other.wav
    │
    ├─> ASR Service (Whisper)
    │       └─> Transcription + Word Timestamps
    │
    ├─> Beats Service (Librosa)
    │       └─> Tempo + Beat Times + Key
    │
    ├─> Chords Service (Librosa + Templates)
    │       └─> Chord Progressions
    │
    ├─> Melody Service (Librosa)
    │       └─> Pitch Contours
    │
    └─> Packager Service
            └─> Song Map JSON
```

### Service Orchestration

**Async Task Group** for parallel execution:

```python
async def run_parallel_services(audio_path: str):
    async with asyncio.TaskGroup() as tg:
        # Services that can run in parallel
        asr_task = tg.create_task(run_asr(audio_path))
        beats_task = tg.create_task(run_beats(audio_path))

    # Wait for all to complete
    asr_result = await asr_task
    beats_result = await beats_task

    return asr_result, beats_result
```

---

## RAG Knowledge Base

### Architecture

```
┌─────────────────────────────────────────┐
│      Knowledge Base Documents           │
│  knowledge-base/                        │
│  ├── audio-dsp/*.md                     │
│  ├── frameworks/*.md                    │
│  └── project/*.md                       │
└──────────────┬──────────────────────────┘
               │
       ┌───────▼────────┐
       │    Docling     │  Document Converter
       │  Ingestion     │  Extract text + metadata
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  Sentence      │  Generate embeddings
       │  Transformers  │  all-MiniLM-L6-v2
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │   ChromaDB     │  Vector database
       │  Vector Store  │  Semantic search
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  Query Engine  │  Retrieve relevant docs
       │  (RAG)         │  for Claude agents
       └────────────────┘
```

### Knowledge Base Usage

```python
from knowledge_rag import KnowledgeBase

kb = KnowledgeBase("knowledge-base")

# Ingest documents (auto-caches)
kb.ingest_all()

# Query knowledge base
results = kb.query("How to implement beat detection?")

# Returns relevant documentation snippets
for result in results:
    print(result['content'])
    print(result['source'])
```

---

## Performance Optimizations

### Backend Optimizations

1. **Async I/O**: Non-blocking file operations
2. **Connection Pooling**: Database connection reuse
3. **Model Caching**: Load ML models once
4. **Result Caching**: Cache analysis results
5. **GPU Acceleration**: CUDA for PyTorch models

### Frontend Optimizations

1. **Code Splitting**: Lazy load routes
2. **Asset Optimization**: Compress images, minify CSS
3. **Service Worker**: Cache static assets
4. **Web Workers**: Offload heavy computations
5. **Virtual Scrolling**: Render only visible items

### Audio Processing Optimizations

1. **Chunk Processing**: Process audio in chunks
2. **Model Selection**: Use appropriate model size (tiny/small/base)
3. **Parallel Services**: Run independent services concurrently
4. **Skip Optional Services**: Skip separation if not needed

---

## Security Considerations

### API Security

1. **CORS**: Restrict origins in production
2. **Rate Limiting**: Prevent abuse (future)
3. **API Keys**: Validate in middleware
4. **Input Validation**: Pydantic models
5. **File Upload Limits**: Max file size

### Data Security

1. **Environment Variables**: Never commit secrets
2. **Database Encryption**: Encrypt sensitive data (future)
3. **HTTPS Only**: Force HTTPS in production
4. **Secure File Storage**: Validate file types, scan uploads

---

## Deployment Architecture

### Development

```
Local Machine
├── Backend: localhost:8000
├── Frontend: localhost:5001
└── Database: SQLite file
```

### Production (GCP Cloud Run)

```
┌─────────────────────────────────────┐
│       Load Balancer (HTTPS)         │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│     Cloud Run (Frontend)            │
│     Docker Container                │
│     Port 5001                       │
└─────────────────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│     Cloud Run (Backend)             │
│     Docker Container                │
│     Port 8000                       │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│     Cloud SQL (PostgreSQL)          │
│     Managed Database                │
└─────────────────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│     Cloud Storage                   │
│     Audio Files + Song Maps         │
└─────────────────────────────────────┘
```

---

## Future Architecture

### Planned Enhancements

1. **Microservices**: Containerize each audio service
2. **Message Queue**: Celery + Redis for background jobs
3. **CDN**: CloudFlare for static assets
4. **WebSocket**: Real-time collaboration
5. **Mobile Apps**: React Native
6. **GraphQL**: Replace/augment REST API
7. **Multi-tenancy**: User accounts and permissions

---

*For API details, see [API.md](./API.md). For deployment, see [INSTALLATION.md](./INSTALLATION.md).*
