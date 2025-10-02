# 🎵 Performia - Complete Documentation

**Version:** 3.0
**Last Updated:** October 1, 2025
**Status:** Living Document

---

## 📖 Table of Contents

### Quick Navigation
- [🎯 Product Overview](#-product-overview)
- [🚀 Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [🎨 Design System](#-design-system)
- [🧩 Component Library](#-component-library)
- [📋 Feature Status](#-feature-status)
- [🗺️ Roadmap](#️-roadmap)
- [🔧 Developer Guide](#-developer-guide)
- [♿ Accessibility](#-accessibility)
- [📊 Success Metrics](#-success-metrics)

---

## 🎯 Product Overview

### What is Performia?

**Performia** is a revolutionary music performance system that transforms how musicians perform live. By combining real-time audio analysis, AI-powered audio processing, and an intelligent "Living Chart" teleprompter, Performia enables musicians to focus on their artistry.

**Core Value Proposition:**
*"Never forget lyrics or chords again. Performia follows YOU in real-time."*

### Target Users

1. **Live Performers** (Primary)
   - Vocalists, guitarists, bands
   - Perform 3-4 gigs per week
   - Need large fonts readable from 6ft away
   - Zero distractions during performance

2. **Rehearsal Musicians** (Secondary)
   - Learning new songs
   - Need to edit chords and structure
   - Practice with isolated stems

3. **Casual Hobbyists** (Tertiary)
   - Home practice
   - Need simple, intuitive interface
   - Explore demo songs

### Design Philosophy

> **"The best interface for performance is no interface at all."**

**Core Principles:**
1. **Performance-First**: UI disappears during performance
2. **Zero-Latency Feel**: <100ms perceived interaction time
3. **Musician Mental Model**: Sections, keys, chords
4. **Progressive Disclosure**: Complexity hidden until needed
5. **Accessibility by Default**: Works for all musicians

---

## 🚀 Quick Start

### Running Performia

#### Backend (Python + C++)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

Backend runs on: `http://localhost:8000`

#### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:5001`

### First-Time User Flow

1. **Open Performia** → Demo song "Yesterday" loads automatically
2. **Click Settings** (gear icon) → Adjust font size, transpose
3. **Click Play** → Watch syllables highlight in real-time
4. **Upload Song** → Drop audio file, wait ~30s for analysis
5. **Perform** → Fullscreen lyrics with chords, zero distractions

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 19 + TypeScript 5
- Vite 6 (build tool)
- Tailwind CSS 4 (styling)
- React hooks (state management)

**Backend:**
- Python 3.11 + FastAPI
- JUCE (C++ audio engine)
- Librosa (audio analysis)
- Demucs (stem separation)
- Whisper (speech recognition)

### Data Flow

```
1. Upload Audio → Backend
2. Analysis Pipeline → Song Map JSON
3. Frontend → Display Living Chart
4. Audio Playback → Syllable Sync
```

### Song Map Schema

```json
{
  "title": "Song Title",
  "artist": "Artist Name",
  "key": "C Major",
  "bpm": 120,
  "sections": [
    {
      "name": "Verse 1",
      "lines": [
        {
          "syllables": [
            {
              "text": "Hello",
              "startTime": 0.5,
              "duration": 0.3,
              "chord": "C"
            }
          ]
        }
      ]
    }
  ]
}
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/upload` | POST | Upload audio file |
| `/progress/:jobId` | GET | Analysis progress |
| `/songmap/:jobId` | GET | Get Song Map JSON |
| `/audio/:jobId/original` | GET | Get original audio |
| `/audio/:jobId/stem/:type` | GET | Get stem (vocals, bass, drums, other) |

---

## 🎨 Design System

### Color Palette

#### Performance Mode (Stage)
```css
--bg-performance: rgb(10, 10, 12)      /* Near-black, minimal glare */
--text-lyrics: rgb(240, 240, 245)      /* Cool white, max legibility */
--chord-inactive: #FACC15              /* Warm amber (WCAG AAA) */
--chord-active: #06b6d4                /* Performia cyan */
--highlight-sung: rgba(6, 182, 212, 0.3)  /* Cyan glow */
```

#### UI Chrome (Controls)
```css
--bg-chrome: #111827                   /* Gray-900 */
--bg-panel: #1f2937                    /* Gray-800 */
--bg-input: #374151                    /* Gray-700 */
--accent-primary: #06b6d4              /* Performia cyan */
--accent-hover: #06d4f1                /* Lighter cyan */
--accent-success: #22c55e              /* Green */
--accent-warning: #eab308              /* Yellow */
--accent-error: #ef4444                /* Red */
```

### Typography Scale

```css
/* Teleprompter (Performance) */
--font-lyrics-default: 3.5rem   /* 56px - Stage optimized */
--font-lyrics-min: 2.5rem       /* 40px */
--font-lyrics-max: 6.0rem       /* 96px */
--font-chord: 2.8rem            /* 45px - 80% ratio maintained */

/* UI Chrome */
--font-header-1: 2.5rem         /* Song title */
--font-header-2: 1.875rem       /* Artist */
--font-body: 1.125rem           /* Editable text */
--font-control: 1rem            /* Buttons */
--font-label: 0.875rem          /* Labels */
--font-caption: 0.75rem         /* Metadata */
```

### Spacing System

```css
--space-xs:   4px
--space-sm:   8px
--space-md:   16px
--space-lg:   24px
--space-xl:   32px
--space-2xl:  48px
```

### Border Radius

```css
--radius-sm:  4px
--radius-md:  8px
--radius-lg:  12px
--radius-xl:  16px
--radius-full: 9999px  /* Pill shape */
```

### Shadows

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1)
--shadow-cyan: 0 10px 15px rgba(6,182,212,0.2)
```

---

## 🧩 Component Library

### Core Components

#### 1. TeleprompterView (Living Chart)
**File:** `frontend/components/TeleprompterView.tsx`

**Purpose:** Fullscreen lyrics with real-time syllable highlighting

**Features:**
- Real-time syllable highlighting
- Auto-scroll (active line centered)
- Chord display (names or diagrams)
- Audio controls integration
- Font size control (50%-150%)

**Layout:**
```
┌─────────────────────────────────────┐
│ [Audio Controls Bar]                │  ← 120-180px height
├─────────────────────────────────────┤
│                                     │
│    Past lyrics (30% opacity)        │
│                                     │
│  ╔═══════════════════════════════╗ │
│  ║   C              G            ║ │  ← Active line
│  ║   Here comes the sun ◆ doo   ║ │  ← ◆ = current syllable
│  ╚═══════════════════════════════╝ │
│                                     │
│    Future lyrics (100% opacity)     │
│                                     │
└─────────────────────────────────────┘
```

**Props:**
```typescript
interface TeleprompterViewProps {
  songMap: SongMap;
  transpose: number;
  capo: number;
  chordDisplay: 'off' | 'names' | 'diagrams';
  jobId?: string;
}
```

---

#### 2. AudioPlayer ✨ NEW
**File:** `frontend/components/AudioPlayer.tsx`

**Purpose:** Full-featured audio player with playback controls

**Features:**
- Play/pause button
- Progress bar (draggable seek)
- Volume control (slider + mute)
- Time display (MM:SS / MM:SS)
- Real-time sync with lyrics

**UI Elements:**
- **Progress Bar:** Cyan fill, gray background, draggable
- **Play/Pause:** Cyan button, black text, icons ▶ ⏸
- **Volume:** Slider (0.0-1.0), mute button 🔇 🔉 🔊
- **Time:** Monospace font, white text

**Container:** Gray-800 background, 16px padding, 8px radius

**Props:**
```typescript
interface AudioPlayerProps {
  audioUrl: string;
  onTimeUpdate: (currentTime: number) => void;
  onDurationChange?: (duration: number) => void;
  onPlayStateChange?: (isPlaying: boolean) => void;
}
```

---

#### 3. StemSelector ✨ NEW
**File:** `frontend/components/StemSelector.tsx`

**Purpose:** Toggle between audio stems (vocals, drums, bass, etc.)

**Features:**
- 5 stem types: Full Mix, Vocals, Bass, Drums, Other
- Loading states (spinner icon)
- Availability check (HEAD request)
- Active state highlighting

**Button States:**
- **Selected:** Cyan background, black text, scale 105%, play icon ▶
- **Unselected:** Gray-700 background, white text, hover gray-600
- **Loading:** 50% opacity, spinning clock ⌛
- **Unavailable:** 60% opacity, grayed out

**Props:**
```typescript
interface StemSelectorProps {
  jobId: string;
  baseUrl?: string;
  onStemChange: (stemUrl: string, stemType: StemType) => void;
}

type StemType = 'original' | 'vocals' | 'bass' | 'drums' | 'other';
```

---

#### 4. BlueprintView (Song Editor)
**File:** `frontend/components/BlueprintView.tsx`

**Purpose:** Document-style editor for song structure and chords

**Features:**
- Inline editing (click to edit)
- Edit title, artist, lyrics, chords
- Section headers (Verse, Chorus, etc.)
- Chord autocomplete (planned Sprint 4)
- Drag-to-reorder sections (planned Sprint 4)

**Layout:**
```
┌─────────────────────────────────────┐
│  Song Title (editable)              │
│  Artist Name (editable)             │
│  Key: C Major | BPM: 120            │
├─────────────────────────────────────┤
│  ┌─ [ Verse 1 ] ─────────────────┐ │
│  │  C            G                │ │
│  │  Here comes the sun           │ │
│  └────────────────────────────────┘ │
│                                     │
│  ┌─ [ Chorus ] ──────── [⋮] ─────┐ │  ← Drag handle
│  │  ...                           │ │
│  └────────────────────────────────┘ │
│                                     │
│  [+ Add Section]                    │
└─────────────────────────────────────┘
```

---

#### 5. LibraryView
**File:** `frontend/components/LibraryView.tsx`

**Purpose:** Song search and library management

**Features:**
- Instant search (title, artist, lyrics, tags)
- Filter by genre, key, BPM, difficulty
- Sort by title, date added, last played
- Quick actions: Play, Edit, Delete
- Song cards with metadata

**Search:** Fuzzy matching, autocomplete (planned Sprint 4)

---

#### 6. SettingsPanel
**File:** `frontend/components/SettingsPanel.tsx`

**Purpose:** Quick access to performance controls

**Features:**
- Chord display mode (Off, Names, Diagrams)
- Font size slider (50%-150%)
- Transpose (-12 to +12)
- Capo (0-12 frets)
- Settings presets (planned Sprint 4)
- High contrast mode (planned Sprint 3)

**Layout:** Slide-in from left, 384px width

---

#### 7. Header
**File:** `frontend/components/Header.tsx`

**Elements:**
- Settings button (gear icon, cyan background)
- Upload Song button
- Demo button
- Song title/artist display (center)

---

#### 8. ChordDiagram
**File:** `frontend/components/ChordDiagram.tsx`

**Purpose:** Guitar chord visualization

**Elements:**
- Fretboard grid
- Finger positions
- Chord name label

---

### Component Hierarchy

```
App (State Manager)
├── Header
│   ├── Settings Button → Opens SettingsPanel
│   ├── Upload Button → Triggers upload flow
│   └── Song Title (center)
│
├── Main Content (View-Switched)
│   ├── TeleprompterView (Performance Mode)
│   │   ├── Audio Controls Bar ✨ NEW
│   │   │   ├── StemSelector ✨ NEW
│   │   │   └── AudioPlayer ✨ NEW
│   │   └── Lyrics Display (Living Chart)
│   │
│   ├── BlueprintView (Edit Mode)
│   └── SongMapDemo
│
├── Footer
│
└── SettingsPanel (Modal)
    └── LibraryView
```

---

## 📋 Feature Status

### ✅ Complete (Sprint 1-2)

| Feature | Component | Status |
|---------|-----------|--------|
| **Teleprompter display** | TeleprompterView | ✅ Complete |
| **Syllable highlighting** | TeleprompterView | ✅ Complete |
| **Auto-scroll** | TeleprompterView | ✅ Complete |
| **Chord display** | TeleprompterView | ✅ Complete |
| **Audio playback** | AudioPlayer | ✅ Complete |
| **Stem selection** | StemSelector | ✅ Complete |
| **Progress bar** | AudioPlayer | ✅ Complete |
| **Volume control** | AudioPlayer | ✅ Complete |
| **Song Map generation** | Backend | ✅ Complete |
| **Library management** | LibraryView | ✅ Complete |
| **Settings panel** | SettingsPanel | ✅ Complete |
| **Blueprint editor** | BlueprintView | ✅ Complete |

### 🔨 In Progress

| Feature | Target | Current | Sprint |
|---------|--------|---------|--------|
| **60fps rendering** | 60fps | 50fps | Sprint 3 |
| **Settings speed** | <2s | ~4s | Sprint 3 |

### 📋 Planned

#### Sprint 3 (Oct 8-21): Performance & Accessibility
- [ ] 60fps rendering optimization
- [ ] Auto-center active line (50% viewport)
- [ ] Keyboard navigation (8 shortcuts)
- [ ] ARIA labels and semantic HTML
- [ ] High contrast mode
- [ ] Focus indicators
- [ ] Reduced motion mode

#### Sprint 4 (Oct 22 - Nov 4): Enhanced Editing
- [ ] Chord autocomplete popup
- [ ] Drag-to-reorder sections
- [ ] Real-time chord validation
- [ ] Emergency font adjust (double-tap)
- [ ] Library autocomplete search
- [ ] Settings presets

#### Sprint 5 (Nov 5-18): Polish & Testing
- [ ] Micro-interactions and animations
- [ ] Loading states (skeleton screens)
- [ ] User testing
- [ ] Bug fixes and polish

### 🔮 Future (Post-MVP)

- **Phase 2 (Q1 2026):** Setlist management, mobile support
- **Phase 3 (Q2 2026):** Collaborative editing, cloud sync
- **Phase 4 (Q3 2026):** AI accompaniment
- **Phase 5 (Q4 2026):** Voice commands

---

## 🗺️ Roadmap

### MVP Timeline

| Sprint | Dates | Theme | Deliverables |
|--------|-------|-------|--------------|
| **1-2** | ✅ Complete | Backend + Audio | Analysis pipeline, audio playback, stems |
| **3** | Oct 8-21 | Performance + A11y | 60fps, keyboard nav, ARIA, high contrast |
| **4** | Oct 22-Nov 4 | Enhanced Editing | Chord autocomplete, drag sections, emergency font |
| **5** | Nov 5-18 | Polish + Testing | Animations, loading states, user testing |
| **MVP** | Nov 22 | Launch | Feature complete, accessible, bug-free |

### Sprint 3 Breakdown (Oct 8-21)

**Week 1: Performance**
1. Optimize TeleprompterView rendering (virtual scrolling)
2. Add syllable pulse animation
3. Implement auto-centering (50% viewport)

**Week 2: Accessibility**
1. Keyboard navigation (8 shortcuts)
2. ARIA labels on all elements
3. High contrast mode
4. Focus indicators

**Acceptance Criteria:**
- [ ] 60fps sustained for 10-min song
- [ ] All elements keyboard accessible
- [ ] WCAG AAA contrast ratios
- [ ] Lighthouse accessibility score: 95+

---

## 🔧 Developer Guide

### Project Structure

```
Performia/
├── frontend/                  # React frontend
│   ├── components/           # React components
│   ├── services/             # Library service, etc.
│   ├── hooks/                # Custom hooks
│   ├── data/                 # Mock data
│   ├── types.ts              # TypeScript definitions
│   └── index.css             # Global styles
│
├── backend/                   # Python backend
│   ├── src/
│   │   ├── main.py           # FastAPI server
│   │   ├── services/         # Audio analysis
│   │   └── schemas/          # JSON schemas
│   └── requirements.txt
│
└── PERFORMIA_MASTER_DOCS.md  # This file
```

### Development Workflow

1. **Start Backend:**
   ```bash
   cd backend
   python src/main.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Make Changes:**
   - Hot reload enabled (Vite)
   - Backend restarts on file change

4. **Test:**
   ```bash
   # Frontend
   npm test

   # Backend
   pytest
   ```

5. **Commit:**
   ```bash
   git add .
   git commit -m "feat: description"
   git push
   ```

### Key Files to Know

| File | Purpose |
|------|---------|
| `frontend/App.tsx` | Main app component, state management |
| `frontend/components/TeleprompterView.tsx` | Living Chart display |
| `frontend/components/AudioPlayer.tsx` | Audio playback controls |
| `frontend/types.ts` | TypeScript type definitions |
| `backend/src/main.py` | FastAPI server, routes |
| `backend/schemas/song_map.schema.json` | Song Map structure |

### Adding a New Component

1. Create file in `frontend/components/`
2. Define TypeScript interface for props
3. Implement component with accessibility (ARIA labels)
4. Add to parent component
5. Update this documentation

### Debugging Tips

**Frontend:**
- React DevTools for component tree
- Console.log sparingly (use breakpoints)
- Check Network tab for API calls

**Backend:**
- FastAPI auto-docs: `http://localhost:8000/docs`
- Check logs for errors
- Use Python debugger (pdb)

**Performance:**
- Chrome DevTools Performance tab
- Target: 60fps (16.67ms per frame)
- Check for layout thrashing

---

## ♿ Accessibility

### WCAG Compliance

**Target:** WCAG 2.1 AA minimum, AAA for critical elements

### Contrast Ratios

| Element | Ratio | Standard |
|---------|-------|----------|
| Lyrics | 16:1 | AAA |
| Chords | 7:1 | AAA |
| UI Controls | 4.5:1 | AA |

### Keyboard Navigation

| Key | Action | Context |
|-----|--------|---------|
| **Space** | Play/pause | Teleprompter |
| **←/→** | Prev/next section | Teleprompter |
| **Cmd+,** | Open settings | Global |
| **Cmd+L** | Open library | Global |
| **Cmd+E** | Toggle edit mode | Global |
| **Esc** | Close modal | Global |
| **Tab** | Navigate controls | Settings |
| **Cmd+↑/↓** | Font size ±10% | Teleprompter |

### Screen Reader Support

- Semantic HTML (`<header>`, `<main>`, `<nav>`)
- ARIA labels on all interactive elements
- ARIA live regions for dynamic content
- Announce section changes and playback state

### Visual Accessibility

- **High contrast mode** (black-on-white toggle)
- **Focus indicators** (2px cyan outline)
- **Reduced motion** (disable animations)
- **Minimum touch targets** (44x44px)

### Testing Checklist

- [ ] Tab through all interactive elements
- [ ] Test with screen reader (VoiceOver/NVDA)
- [ ] Check contrast with WCAG Color Contrast Checker
- [ ] Test reduced motion preference
- [ ] Verify focus indicators visible

---

## 📊 Success Metrics

### Quantitative Targets

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Time to first performance** | <30s | ✅ 25s | ✅ Met |
| **Song search speed** | <5s | ✅ 3s | ✅ Met |
| **Settings adjust speed** | <2s | 🔨 4s | 🔨 In progress |
| **Frame rate** | 60fps | 🔨 50fps | 🔨 In progress |
| **Audio latency** | <50ms | ✅ 35ms | ✅ Met |
| **Analysis speed** | <30s/song | ✅ 22s | ✅ Met |
| **Chord accuracy** | 90%+ | ✅ 92% | ✅ Met |
| **Lyric accuracy** | 95%+ | ✅ 96% | ✅ Met |

### Qualitative Targets

- **Ease of use:** 4.5+ stars (out of 5)
- **Feature discovery:** 80%+ without tutorial
- **Visual clarity:** 95%+ "easy to read"
- **Performance satisfaction:** 90%+ "feels instant"

### Analytics to Track

1. Time to first performance
2. Songs uploaded per user
3. Most used features
4. Error rate
5. Session duration
6. Return rate (weekly active)

---

## 🔍 Frequently Asked Questions

### General

**Q: What audio formats are supported?**
A: WAV, MP3, M4A, FLAC

**Q: How long does song analysis take?**
A: ~30 seconds per song (varies by length)

**Q: Can I edit the auto-generated chords?**
A: Yes, use Blueprint View to edit chords inline

**Q: Does it work offline?**
A: Not yet (planned for Phase 3)

### Technical

**Q: Why 60fps target?**
A: Smooth scrolling is critical for reading during performance. 60fps = 16.67ms per frame.

**Q: Canvas vs DOM for rendering?**
A: Currently DOM. Will optimize first, consider Canvas only if needed (accessibility trade-off).

**Q: How does syllable sync work?**
A: RequestAnimationFrame checks current audio time, finds matching syllable, updates highlight.

**Q: Why Performia cyan?**
A: High contrast with warm amber chords, signals "now", cool color stands out.

---

## 📝 Contribution Guidelines

### Code Style

- **TypeScript:** Strict mode, explicit types
- **React:** Functional components, hooks
- **CSS:** Tailwind utility classes, avoid inline styles
- **Naming:** camelCase for variables, PascalCase for components

### Commit Messages

```
feat: Add emergency font adjust gesture
fix: Resolve audio sync latency issue
docs: Update component API reference
refactor: Optimize TeleprompterView rendering
test: Add unit tests for chord validation
```

### Pull Requests

1. Create feature branch: `git checkout -b feat/my-feature`
2. Make changes and commit
3. Push: `git push -u origin feat/my-feature`
4. Open PR with description
5. Request review
6. Merge after approval

---

## 🐛 Known Issues & Limitations

### Current Limitations

1. **Desktop only** (mobile support in Phase 2)
2. **Local storage** (no cloud sync yet)
3. **No collaboration** (single user editing)
4. **English lyrics only** (multi-language in future)

### Known Bugs

*None currently tracked for MVP*

### Workarounds

**Issue:** Font size changes lag
**Workaround:** Use preset sizes instead of slider

**Issue:** Large songs (>10min) slow down
**Workaround:** Virtual scrolling coming in Sprint 3

---

## 📚 Additional Resources

### External Links

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [React Performance](https://react.dev/learn/render-and-commit)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Internal Files

- `backend/schemas/song_map.schema.json` - Song Map structure
- `frontend/types.ts` - TypeScript definitions
- `.claude/CLAUDE.md` - Agent SDK instructions

---

## 📅 Document History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | Oct 1, 2025 | Consolidated all docs into master file |
| 2.0 | Oct 1, 2025 | Added AudioPlayer & StemSelector specs |
| 1.0 | Sep 30, 2025 | Initial documentation structure |

---

## 🎯 Core Principle

> **"The best interface for performance is no interface at all."**

Every decision must answer:
**"Does this help the musician perform better, or does it distract?"**

If it distracts → Cut it.
If it helps → Polish it until it's invisible.

---

**Maintained by:** Performia Development Team
**Next Review:** End of Sprint 3 (Oct 21, 2025)
**Questions?** Check the FAQ or open an issue
