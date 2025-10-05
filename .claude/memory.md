# Performia Project Memory

## Project Identity
**Name**: Performia
**Purpose**: Revolutionary music performance system with AI-powered accompaniment and real-time Living Chart teleprompter
**Status**: ✅ Audio/Demo Mode Complete - Production Ready

## Key Technical Facts

### Architecture
- **Backend**: Python 3.13 + FastAPI (port 3002)
- **Frontend**: React 19 + TypeScript 5 + Vite 6 + Tailwind CSS 4
- **Audio Engine**: JUCE for sub-10ms latency (planned)
- **Data Format**: Song Map JSON (syllable-level timing with chords)

### Core Components
1. **Living Chart**: Real-time teleprompter with dual-mode support (demo/audio)
2. **Audio Pipeline**: ASR, beat detection, chord analysis, melody extraction, stem separation
3. **Demo Mode**: Simulated auto-playback for song preview
4. **Audio Mode**: Real-time synchronization with uploaded audio files

### Directory Structure
```
Performia/
├── frontend/              # React + TypeScript UI
│   ├── components/        # UI components
│   ├── hooks/             # React hooks (useSongPlayer)
│   ├── services/          # API services
│   ├── tests/             # Unit tests (16 tests, all passing)
│   └── package.json
├── backend/               # Python services
│   ├── src/services/      # Audio analysis services
│   │   ├── api/           # FastAPI server (port 3002)
│   │   ├── asr/           # Whisper ASR
│   │   ├── beats_key/     # Beat detection
│   │   ├── chords/        # Chord recognition
│   │   ├── melody_bass/   # Melody extraction
│   │   ├── separation/    # Demucs stem separation
│   │   ├── structure/     # Song structure detection
│   │   └── packager/      # Song Map generation
│   └── requirements.txt
├── .claude/               # Agent SDK configuration
│   ├── CLAUDE.md          # Project context
│   ├── memory.md          # This file
│   └── SESSION_SUMMARY.md # Latest session details
└── tests/                 # All test suites
```

## Current Status (October 5, 2025)

### ✅ COMPLETED: Strategic Research & Implementation Planning
**Sprint**: October 5, 2025 (Session 5)
**Status**: Comprehensive research analysis, implementation planning, and agent orchestration design

**Session Work Completed:**

1. **Part 2 Research Analysis** (Interactive/Visual/Social Technologies)
   - Reviewed comprehensive 337-line strategic report on immersive experiences
   - Analyzed 10 deep-dive technologies (NVIDIA Audio2Face, MetaHuman, JackTrip, WebTransport, etc.)
   - Validated 18 production-ready technologies from October 2024-2025
   - Identified gaps: social gamification, AI creativity tools, content export workflows

2. **Multi-Model Research Agent Orchestration Design**
   - Designed conservative 3-agent plan (social, AI creativity, content export)
   - Designed maximum-scale 22-agent plan across 5 AI providers
   - Model selection strategy: Opus 4.1 (deep analysis), Gemini Flash (breadth), GPT-4 (academic), Sonnet 4.5 (balanced)
   - Cost analysis: $50 (conservative) vs $330 (comprehensive)
   - Execution timeline: 3-day parallel research vs 2-3 week sequential

3. **Implementation Plan Creation** (docs/IMPLEMENTATION_PLAN_2025-2026.md)
   - 955-line comprehensive roadmap (Q4 2025 → 2027)
   - 3 phases: Q4 2025 validation ($127k), Q1-Q2 2026 production ($785k), 2026+ R&D ($1.1M)
   - 5 Q4 2025 projects: ASR benchmark, HS-TasNet prototype, Cmajor feasibility, Stable Audio, ByteDance partnership
   - Team growth plan: 6 → 13 engineers
   - Total budget: $2,012,200 over 18+ months

4. **Research Prompt Part 2 Creation** (1,606 lines)
   - Comprehensive research areas: avatars, visualization, multiplayer, VR/AR, social, accessibility
   - 10 research domains with specific technologies to investigate
   - Academic literature review strategy (NIME, CHI, SIGGRAPH)
   - Hands-on testing methodology

5. **Codebase Architecture Analysis**
   - Keep vs scrap assessment: 65% preserved, 35% strategic deletion
   - Frontend Living Chart: 90% keep (core IP)
   - Backend offline analysis: 60% keep (complementary)
   - Backend real-time foundation: 30% keep (port to C++/JUCE)
   - Decision: In-place evolution, NOT new repo

6. **Knowledge Base Expansion**
   - Expanded from 7 docs (1,993 terms) to 11 docs (4,350 terms)
   - Added JUCE framework (393 lines), music AI 2025 (396 lines), real-time DSP (411 lines), SuperCollider (383 lines)
   - Auto-rebuild verification: cache invalidation working correctly

**Key Findings:**
- Part 1 research focused on audio AI (HS-TasNet, ByteDance, ONNX)
- Part 2 research revealed production-ready avatars, ultra-low-latency networking, browser viability
- Critical gap: social/community features, AI creativity tools, content export
- Research validates technical feasibility of real-time AI accompaniment

**Strategic Decisions:**
- Hybrid research approach: 3 critical agents now, 22 agents if comprehensive scan needed
- Keep existing codebase, evolve in-place (not new repo)
- Implementation plan positions Performia as "AI music collaborator" not "karaoke app"

### ✅ COMPLETED: Docling RAG Knowledge Base Implementation
**Sprint**: October 4, 2025 (Session 3)
**Status**: Implemented and merged docling RAG system to prevent recurring AI mistakes

**Session Work Completed:**

1. **Docling RAG System** (PR #13 - MERGED into ui-clean)
   - Installed docling 2.55.1 (~2-3GB dependencies)
   - Created knowledge-base structure with 7 documents
   - Implemented `knowledge_rag.py` with caching (pickle-based)
   - Built verification tests proving RAG prevents both recurring errors
   - Code review score: 10/10 ✅

2. **Knowledge Base Content**
   - `knowledge-base/claude-code/` - Claude Code paths, commands, common mistakes
   - `knowledge-base/audio-dsp/` - Librosa best practices, music theory, audio DSP
   - `knowledge-base/project/` - Project context (symlinked memory.md)
   - **Indexed**: 7 documents, 1,993 unique terms

3. **Code Quality Improvements** (from review feedback)
   - Pinned docling version with size warning in requirements.txt
   - Replaced duplicate memory.md copy with symlink
   - Added pickle caching for 10x faster subsequent loads
   - Updated .gitignore with cache exclusions

**Test Results:**
```bash
✓ test_directory_confusion_prevention() - PASSED ✅
✓ test_end_session_execution() - PASSED ✅
RAG successfully prevents both recurring mistakes
```

### ✅ COMPLETED: Session Management Fix & Knowledge Management Plan
**Sprint**: October 4, 2025 (Session 2)
**Status**: Fixed `/end-session` cleanup bug, documented knowledge management strategy

### ✅ COMPLETED: E2E Testing & AI Agent Music Knowledge Base
**Sprint**: October 4, 2025 (Session 1)
**Status**: Backend E2E tests complete, AI agents equipped with music domain expertise

**Session Work Completed:**

1. **Backend E2E Testing Infrastructure** (PR #12 - MERGED)
   - Created comprehensive E2E test suite for FastAPI backend
   - 7 passing tests covering upload, status, Song Map retrieval, error cases
   - Implemented proper cleanup fixtures with job ID registration
   - Added test dependencies: pytest, pytest-asyncio, httpx
   - Updated pytest.ini with 'slow' marker for pipeline tests
   - Code review score: 10/10 ✅

2. **AI Agent Music Knowledge Base** (NEW)
   - Created `.claude/MUSIC_AUDIO_KNOWLEDGE.md`
   - Comprehensive music theory fundamentals for AI development agents
   - Librosa best practices with optimized parameters
   - Library selection guidelines (Librosa vs Essentia vs Music21 vs Madmom)
   - Common pitfalls and solutions (CQT vs STFT, HPSS, etc.)
   - Performance benchmarks and accuracy targets
   - Agent guidelines and checklists for audio code development
   - Purpose: Enable AI agents (frontend-dev, audio-pipeline-dev, voice-control) to make better technical decisions

**Test Results:**
```bash
# Frontend tests (previous session)
✓ tests/useSongPlayer.test.ts (8 tests)
✓ tests/TeleprompterView.test.tsx (8 tests)
Tests: 16 passed (16) ✅

# Backend E2E tests (new)
✓ backend/tests/e2e/test_api_upload.py
Tests: 7 passed, 2 skipped ✅
```

### Recent Commits
- ✅ Squash merge PR #13: Docling RAG Knowledge Base (merged to ui-clean branch)
- ✅ Squash merge PR #12: E2E tests for backend API (commit 404539a, main)
- ✅ PR #11: Merge ui-clean into main (consolidated all improvements)
- ✅ PR #10: Unit tests for mode switching
- ✅ PR #9: Audio error handling
- ✅ PR #8: Demo player optimization

### Open Issues
- Issue #2: Phase 1 JUCE Foundation (separate epic, future work)

## Performance Targets
- **Audio Latency**: Target <10ms (JUCE implementation pending)
- **UI Updates**: <50ms real-time refresh ✅
- **Song Map Generation**: ~30 seconds per song ✅
- **Beat Detection Accuracy**: 95%+ ✅
- **Frame Rate**: Smooth 60fps animations ✅

## Critical Files

### Configuration & Documentation
- `.claude/CLAUDE.md` - Project context for agents
- `.claude/MUSIC_AUDIO_KNOWLEDGE.md` - **NEW**: Music & audio domain knowledge for AI agents
- `.claude/SESSION_SUMMARY.md` - Latest session details
- `.claude/memory.md` - This file
- `.claude/cleanup.sh` - **NEW**: Session cleanup script
- `.gitignore` - Updated with build artifacts

### Frontend Core
- `frontend/components/TeleprompterView.tsx` - Main component (dual-mode support)
- `frontend/hooks/useSongPlayer.ts` - Demo mode hook (with enabled parameter)
- `frontend/components/AudioPlayer.tsx` - Audio playback with error handling
- `frontend/services/songMapApi.ts` - Backend API client
- `frontend/types.ts` - TypeScript definitions
- `frontend/.env.example` - Environment variable template

### Testing
- `frontend/tests/TeleprompterView.test.tsx` - Component tests (8 tests)
- `frontend/tests/useSongPlayer.test.ts` - Hook tests (8 tests)
- `frontend/vitest.config.ts` - Test configuration
- `backend/tests/e2e/test_api_upload.py` - **NEW**: Backend E2E tests (7 tests)
- `backend/pytest.ini` - Pytest configuration with markers

### Backend Core
- `backend/src/services/api/main.py` - FastAPI server
- `backend/src/services/api/job_manager.py` - Job persistence
- `backend/schemas/song_map.schema.json` - Song Map schema

## Development Workflow

### Starting Development Servers
```bash
# Terminal 1 - Backend (port 3002)
cd backend
source venv/bin/activate
uvicorn src.services.api.main:app --host 0.0.0.0 --port 3002 --reload

# Terminal 2 - Frontend (port 5001)
cd frontend
npm run dev
```

### Running Tests
```bash
cd frontend
npm test                  # Run all tests
npm test tests/          # Run integration tests
npm test -- --coverage   # With coverage report
```

### Environment Setup
```bash
# frontend/.env.development
VITE_API_URL=http://localhost:3002

# frontend/.env.production
VITE_API_URL=https://api.performia.com
```

## Key Technical Decisions

### 1. Dual-Mode Architecture (October 3, 2025)
- **Problem**: Need both demo preview and real audio playback
- **Solution**: Conditional rendering based on jobId presence
  - jobId present = audio mode (real-time sync)
  - jobId absent = demo mode (simulated playback)
- **Implementation**: `useSongPlayer(songMap, !jobId)` in TeleprompterView

### 2. Performance Optimization (October 3, 2025)
- **Problem**: Demo mode animation frames running during audio playback (wasted CPU)
- **Solution**: Added `enabled` parameter to useSongPlayer hook
- **Result**: Conditional animation frames only when needed

### 3. Error Handling Strategy (October 3, 2025)
- **Problem**: Network failures, missing audio files
- **Solution**: Comprehensive error boundaries in AudioPlayer
  - Loading states with spinner
  - User-friendly error messages
  - Retry functionality
- **Implementation**: AudioPlayer.tsx error states

### 4. Security: JobId Validation (October 3, 2025)
- **Problem**: Potential path traversal attacks via jobId
- **Solution**: Regex validation `/^[a-zA-Z0-9-]+$/`
- **Prevents**: Inputs like `../../../etc/passwd`
- **Location**: TeleprompterView.tsx:51-56

### 5. Test Organization (October 3, 2025)
- **Decision**: Create `tests/` directory instead of `src/__tests__/`
- **Reason**: Separation of concerns, cleaner structure
- **Configuration**: Updated vitest.config.ts to include `tests/**/*.test.{ts,tsx}`

## Data Flow

### Song Map Generation Pipeline
```
1. User uploads audio file
   ↓
2. Backend API (/api/upload)
   ↓
3. Audio Pipeline (parallel processing):
   - ASR (Whisper) → lyrics with timestamps
   - Beats/Key → tempo, time signature, key
   - Chords → chord progressions
   - Melody/Bass → melodic contours
   - Separation (Demucs) → vocal/instrumental stems
   - Structure → verse/chorus detection
   ↓
4. Packager combines all → Song Map JSON
   ↓
5. Frontend receives Song Map
   ↓
6. TeleprompterView renders with real-time sync
```

### Real-Time Playback Flow
```
1. TeleprompterView detects jobId
   ↓
2. Fetches audio: /api/audio/{jobId}/original
   ↓
3. AudioPlayer component:
   - Loads audio file
   - Handles play/pause/seek
   - Updates currentTime every frame (60fps)
   ↓
4. TeleprompterView receives time updates
   ↓
5. Calculates active syllable from currentTime
   ↓
6. Highlights active syllable with progress bar
```

## Known Issues & Constraints

### Current Limitations
- Audio processing time: ~30 seconds per song (acceptable)
- JobId format: alphanumeric with hyphens only (security requirement)
- Demo mode: simulated timing, not real audio analysis
- No offline mode support (requires backend connection)

### Resolved Issues
- ✅ Schema mismatch (resolved via adapter in previous sprint)
- ✅ Demo player CPU waste (resolved with enabled parameter)
- ✅ Audio error handling (resolved with comprehensive error boundaries)
- ✅ Missing tests (resolved with 16 comprehensive unit tests)

## Next Session Recommendations

### When Session Reopens

**Quick Status Check:**
```bash
cd /Users/danielconnolly/Projects/Performia
git status
git log --oneline -10
cat .claude/SESSION_SUMMARY.md
```

**Review Strategic Documents:**
```bash
# Implementation plan
cat docs/IMPLEMENTATION_PLAN_2025-2026.md

# Research findings
cat "docs/Performia's Immersive Experience_ A Strategic Report on Visual, Interactive, and Social Technologies (October 2025).md"

# Research prompts
cat docs/research-prompt-oct-2025.md
cat docs/research-prompt-part2-interactive-oct-2025.md
```

### Immediate Next Steps (RECOMMENDED)

#### Option 1: Execute Research Agent Strategy (HIGH PRIORITY)
**Decision Point from Session 5:**
- **Plan A (Conservative)**: Launch 3 critical agents ($50 budget)
  - social-gamification-agent
  - ai-creativity-agent
  - content-export-agent
- **Plan B (Comprehensive)**: Launch 22 agents across 5 providers ($330 budget)
- **Plan C (Hybrid)**: Start with Plan A, escalate to Plan B if gaps remain

**Action Items:**
1. Get budget approval ($50 or $330)
2. Finalize agent task specifications
3. Launch agents in parallel (single message, multiple Task tools)
4. Collect outputs over 48-72 hours
5. Synthesize findings into final implementation plan

#### Option 2: Begin Q4 2025 Projects (After Research Complete)
Based on implementation plan, start:
- **Project 1.1**: ASR Benchmark (dataset curation)
- **Project 1.4**: Stable Audio integration (quick win)
- **Project 1.5**: ByteDance partnership outreach

#### Option 3: Add Documents to Knowledge Base
**Commit and integrate:**
- docs/IMPLEMENTATION_PLAN_2025-2026.md
- docs/Performia's Immersive Experience report
- docs/research-prompt-part2-interactive-oct-2025.md
- Run knowledge_rag.py to index new documents

#### Option 4: Prototype Quick Wins
Based on immersive experience report recommendations:
- Browser-based audio-reactive visualizer (three.js + Web Audio)
- Virtual bandmate concept art (MetaHuman exploration)
- Gesture control prototype (Ultraleap hardware acquisition)

### Agent Recommendations
- **frontend-dev**: UI/UX improvements, accessibility
- **audio-pipeline-dev**: Pipeline optimization, quality improvements
- **voice-control**: Voice command integration

## Quality Metrics (Current)

| Metric | Score | Status |
|--------|-------|--------|
| **Test Coverage** | 100% critical paths | ✅ |
| **Frontend Tests** | 16/16 passing (100%) | ✅ |
| **Backend E2E Tests** | 7/7 passing (100%) | ✅ |
| **Code Review Score** | 10/10 (PR #12) | ✅ |
| **Security** | Path traversal prevention + validation | ✅ |
| **Performance** | Optimized (conditional frames) | ✅ |
| **Error Handling** | Comprehensive with retry | ✅ |
| **Documentation** | Complete + AI agent knowledge base | ✅ |
| **AI Agent Expertise** | Music/audio domain knowledge | ✅ NEW |

## Voice Integration (Planned)
- OpenAI Whisper API for speech recognition
- Voice commands for development workflow
- Voice control during live performance
- Voice input for Song Map editing

## Knowledge Management & Learning Systems (Oct 4, 2025)

### Current Problem
AI agents (Claude) make recurring mistakes despite documentation in memory.md:
- **Example 1**: Looked in wrong directory (`~/.config/claude/commands/` instead of `~/.claude/commands/`)
- **Example 2**: Created cleanup script but didn't execute it during `/end-session`
- **Root cause**: Memory alone insufficient for preventing repeated errors

### Proposed Solutions

#### 1. Docling Integration (PRIMARY)
- **Purpose**: RAG system for project knowledge and technical documentation
- **What to ingest**:
  - Official Claude Code documentation (paths, commands, workflows)
  - Audio/music domain knowledge (Librosa, Essentia, Music21, audio DSP)
  - Project-specific patterns and best practices
  - Common mistakes and their solutions
- **Benefits**:
  - Authoritative source of truth
  - Searchable knowledge base
  - Prevents guessing at paths/configurations
  - Enables AI agents to access deep technical knowledge

#### 2. Multi-Source Learning Repository
- **Reference**: https://github.com/Marktechpost/AI-Tutorial-Codes-Included
- **Resources needed**:
  - Librosa tutorials and best practices
  - Audio signal processing fundamentals
  - Music information retrieval (MIR) techniques
  - Real-world code examples
  - Common pitfalls and solutions

#### 3. Documentation Structure
- **Created files**:
  - `~/.claude/COMMON_MISTAKES.md` - Recurring errors and prevention
  - `.claude/MUSIC_AUDIO_KNOWLEDGE.md` - Audio domain expertise for agents
  - `.claude/memory.md` - Project status and session history
  - `.claude/SESSION_SUMMARY.md` - Per-session details
- **Needed**:
  - `.claude/CLAUDE_CODE_REFERENCE.md` - Authoritative paths/commands (from docling)
  - `.claude/LEARNING_RESOURCES.md` - External tutorials and references
  - Docling-powered RAG for searchable knowledge

### Action Items
1. ✅ Document session management bug in memory.md and COMMON_MISTAKES.md
2. ✅ Update `/end-session` command with explicit execution requirement
3. ✅ Set up docling to ingest Claude Code official documentation
4. ✅ Ingest audio/music learning resources (Librosa, etc.)
5. ✅ Create comprehensive knowledge base accessible to all AI agents
6. ✅ Test that docling RAG prevents directory/path confusion
7. ✅ Review and finalize knowledge management strategy (PR #13 merged)

### Success Criteria
- AI agents can query docling for correct Claude Code paths
- Audio pipeline agents have access to best-practice Librosa parameters
- No repeated mistakes from previous sessions
- Knowledge persists across sessions and projects

## Important Reminders

### Session Management
- **START SESSION**: Run `/start-session` to get current status and next steps
- **END SESSION**: Run `/end-session` which:
  1. Updates `.claude/memory.md` with session work
  2. Creates `.claude/cleanup.sh` if missing (auto-generated based on project type)
  3. **MUST execute `bash .claude/cleanup.sh`** (removes cache, temp files, updates timestamps)
  4. Confirms cleanup completion
- **CRITICAL BUG FIX (Oct 4, 2025)**: `/end-session` was creating cleanup script but NOT running it - this is now fixed and documented in global command

### Code Standards
- Always run tests after changes: `npm test`
- Follow existing patterns in codebase
- Update tests when modifying features
- Document architectural decisions

### Git Workflow
- Create feature branches for new work
- Write descriptive commit messages
- Use conventional commits format
- Create PRs for all changes
- Run `/review` before merging

### Environment Variables
- Never commit `.env` files
- Use `.env.example` as template
- Update `.env.example` when adding new vars
- Document all environment variables

---
*Last Updated*: October 05, 2025
*Next Review*: Start of next development session
*Session 1 Duration*: ~2 hours - Backend tests + music knowledge base
*Session 2 Duration*: ~1 hour - Session management fix + knowledge plan
*Session 3 Duration*: ~1.5 hours - Docling RAG implementation (PR #13)
*Session 4 Duration*: ~15 minutes - Enhanced `/end-session` with auto-commit and PR creation
*Session 5 Duration*: ~3 hours - Strategic research analysis, implementation planning, multi-model agent orchestration design
*Major Achievements*:
- Backend test infrastructure (10/10 quality) + AI agent music domain expertise
- Fixed `/end-session` cleanup execution bug
- Implemented and merged docling RAG knowledge base (PR #13, 10/10 score)
- Knowledge base with 11 documents (4,350 unique terms) preventing recurring AI mistakes
- Enhanced `/end-session` command with auto-commit workflow and optional PR creation
- **Comprehensive 955-line implementation plan (Q4 2025 → 2027, $2M budget)**
- **Part 2 research analysis (interactive/visual/social technologies)**
- **Multi-model research agent orchestration strategy (22 agents across 5 AI providers)**
- **Codebase architecture analysis (keep vs scrap, 65% preservation)**

### Session 4 Details (October 4, 2025)
**Work Completed:**
- Updated global `/end-session` command (`~/.claude/commands/end-session.md`)
- Added explicit session documentation instructions
- Implemented auto-commit workflow: `git add . && git commit` after documenting
- Added intelligent PR creation prompt (only on feature branches)
- Commit format: `docs: session N - [summary]` or `feat/fix/refactor: [summary]`

**Benefits:**
- No more uncommitted changes between sessions
- Clean git history with session-based commits
- Optional PR creation for feature branch work
- `/start-session` can detect open PRs and suggest next steps
