# Performia Frontend UX Design Specification

**Version:** 2.0
**Date:** October 1, 2024
**Status:** 🎯 DEFINITIVE SPECIFICATION
**Purpose:** Precision UX design for musician-focused performance system

---

## 🎯 Design Philosophy

**Core Principle:** *Musicians need to focus on their performance, not the interface.*

Every design decision must answer: **"Does this help the musician perform better, or does it distract?"**

### Design Pillars

1. **Performance-First**: UI disappears during performance, emerges for control
2. **Zero-Latency Feel**: Every interaction feels instantaneous (<100ms perceived)
3. **Musician Mental Model**: Matches how musicians think (sections, keys, chords)
4. **Progressive Disclosure**: Complexity hidden until needed
5. **Accessibility by Default**: Works for all musicians, all contexts

---

## 👥 User Personas & Workflows

### Persona 1: **Live Performer** (Primary)

**Name:** Sarah, Professional Vocalist
**Context:** Performing at a venue, needs lyrics/chords in real-time
**Environment:** Stage lighting (variable), standing 3-6ft from screen
**Pain Points:** Can't see small text, can't fiddle with controls mid-song, needs chords NOW

**Critical Workflows:**

#### Workflow 1.1: Pre-Performance Setup (30 seconds)
```
GOAL: Get ready to perform in under 30 seconds

1. Open Performia → Shows LAST SONG immediately
2. Click song title → Library opens (search autocomplete ready)
3. Type "yester" → "Yesterday" appears as first result
4. Click → Song loads in Teleprompter View
5. Tap Settings → Adjust font size (ONE slider)
6. Tap Transpose +2 (TWO taps)
7. Close settings → READY TO PERFORM

SUCCESS: <30 seconds from open to ready
```

#### Workflow 1.2: Live Performance (0 distractions)
```
GOAL: Sing song with zero UI distractions

1. Song loads → Teleprompter fills screen (no chrome, no buttons)
2. Syllables highlight in real-time as audio plays
3. Chords appear above words automatically
4. Screen scrolls smoothly, keeping active line centered
5. Nothing else exists - pure performance focus

SUCCESS: Musician never looks at controls, only lyrics
```

#### Workflow 1.3: Emergency Mid-Song Adjustment (2 seconds)
```
GOAL: Fix font size or transpose WITHOUT stopping song

1. Double-tap screen → Mini control bar slides in from side
2. Drag font slider OR tap transpose +1
3. Change happens immediately (no confirmation)
4. Control bar auto-hides after 3 seconds
5. Performance continues uninterrupted

SUCCESS: <2 seconds, zero mental context switch
```

---

### Persona 2: **Rehearsal Musician** (Secondary)

**Name:** Marcus, Band Guitarist
**Context:** Learning new song, needs to edit chords and structure
**Environment:** Home studio, close to screen, has time
**Pain Points:** Chords are wrong, need to rearrange sections, want to annotate

**Critical Workflows:**

#### Workflow 2.1: Song Upload & Edit (2 minutes)
```
GOAL: Upload song, fix chords, rearrange sections

1. Click "Upload Song" button
2. Drag audio file (or browse)
3. Wait for analysis → Progress bar with stages
4. Song loads in Teleprompter → Review auto-generated chords
5. Click song title → Switches to Blueprint View
6. Click any chord → Edit inline (chord autocomplete)
7. Drag section headers → Rearrange (Verse 1 ↔ Chorus)
8. Click "Save to Library" → Tagged and ready

SUCCESS: Song uploaded, edited, and saved in <2 minutes
```

#### Workflow 2.2: Fine-Tune Timing (1 minute)
```
GOAL: Adjust syllable timing for more accurate display

1. In Blueprint View → Click "Timeline Mode" toggle
2. Each syllable shows timing bar underneath
3. Drag syllable timing handles to adjust
4. Changes preview in real-time in side panel
5. Click "Apply" → Timing saved

SUCCESS: Precise timing control without code
```

---

### Persona 3: **Casual User** (Tertiary)

**Name:** Alex, Hobbyist
**Context:** Singing at home, exploring features
**Environment:** Laptop, relaxed pace
**Pain Points:** Overwhelmed by options, needs guidance

**Critical Workflows:**

#### Workflow 3.1: First-Time User (5 minutes)
```
GOAL: Understand Performia and sing first song

1. Launch app → Welcome modal with 3-step tutorial
   - "This is the Teleprompter (show)" → Auto-plays demo
   - "Tap here to change song" → Library tour
   - "Tap Settings for controls" → Font/transpose tour
2. Modal closes → Demo song ready in Teleprompter
3. Click Play → Song plays with highlighting
4. User sings along → Success!

SUCCESS: User understands core features in 5 minutes
```

---

## 🎨 Visual Design System

### Color Psychology for Musicians

**Color choices optimized for stage lighting and visibility:**

#### Primary Palette (Performance Mode)
```css
--bg-performance:     rgb(10, 10, 12);      /* Near-black, minimizes screen glare */
--text-primary:       rgb(240, 240, 245);   /* Cool white, easiest to read */
--text-secondary:     rgb(156, 163, 175);   /* Muted gray for metadata */
--chord-default:      rgb(250, 204, 21);    /* Warm amber (WCAG AAA) */
--chord-active:       rgb(34, 211, 238);    /* Cyan (attention grabbing) */
--highlight-sung:     rgba(34, 211, 238, 0.3); /* Cyan glow for sung lyrics */
--highlight-current:  rgb(34, 211, 238);    /* Bright cyan for current syllable */
```

**Rationale:**
- **Near-black background**: Reduces eye strain, works in dark venues
- **Cool white text**: Maximum legibility, doesn't wash out in stage lights
- **Amber chords**: Warm color distinguishes from lyrics, high contrast
- **Cyan highlights**: Cool color contrasts with warm chords, signals "now"

#### Accent Palette (Edit/Control Mode)
```css
--accent-primary:     rgb(59, 130, 246);    /* Blue (trust, control) */
--accent-secondary:   rgb(168, 85, 247);    /* Purple (creativity) */
--success:            rgb(34, 197, 94);     /* Green (confirmation) */
--warning:            rgb(234, 179, 8);     /* Yellow (caution) */
--error:              rgb(239, 68, 68);     /* Red (error, stop) */
```

### Typography Scale (Stage Visibility)

**Base font must be readable from 6ft away on a 24" screen:**

```css
/* Teleprompter (Performance Mode) */
--font-lyrics-base:   3.5rem;    /* 56px - Default, readable from 6ft */
--font-lyrics-min:    2.5rem;    /* 40px - Smallest allowed */
--font-lyrics-max:    6.0rem;    /* 96px - Maximum for tight stages */
--font-chord:         2.8rem;    /* 45px - 80% of lyrics (clear hierarchy) */

/* Blueprint/Edit Mode */
--font-header-1:      2.5rem;    /* 40px - Song title */
--font-header-2:      1.875rem;  /* 30px - Artist */
--font-section:       1.5rem;    /* 24px - Section headers */
--font-body:          1.125rem;  /* 18px - Editable text */
```

**Dynamic Scaling:**
- User adjusts ONE slider (50% - 150%)
- All text scales proportionally
- Chord-to-lyric ratio ALWAYS maintained (0.8:1)
- Line spacing adjusts automatically (1.5x font size)

### Spacing & Layout (Touch Targets)

**All interactive elements meet AAA accessibility:**

```css
/* Minimum Touch Targets */
--touch-target-min:   44px;      /* iOS/Android standard */
--touch-target-ideal: 52px;      /* Performia standard (easier for stage) */

/* Spacing Scale (8px base) */
--space-xs:   0.5rem;   /* 8px  - Tight (chord-lyric gap) */
--space-sm:   1rem;     /* 16px - Comfortable (button padding) */
--space-md:   1.5rem;   /* 24px - Breathing room (section gaps) */
--space-lg:   2rem;     /* 32px - Clear separation (panels) */
--space-xl:   3rem;     /* 48px - Major divisions (header/body) */

/* Line Spacing (Readability) */
--line-height-tight:   1.2;   /* Titles */
--line-height-normal:  1.5;   /* Lyrics (default) */
--line-height-loose:   1.9;   /* Lyrics (spacious mode) */
```

---

## 📐 Component Architecture

### View Hierarchy

```
App (State Manager)
├── Header (Always Visible)
│   ├── Logo/Brand (left)
│   ├── Song Title/Artist (center) → Click to toggle views
│   ├── Settings Button (right) → Opens SettingsPanel
│   └── Upload Button (right) → Triggers upload flow
│
├── Main Content (View-Switched)
│   ├── TeleprompterView (Performance Mode)
│   │   └── Living Chart (Fullscreen, auto-scroll)
│   │
│   ├── BlueprintView (Edit Mode)
│   │   ├── Song Metadata (editable)
│   │   └── Sections (drag-to-reorder, inline-edit)
│   │
│   └── UploadView (Upload Flow)
│       ├── File Picker (drag-drop or browse)
│       └── Progress Indicator (staged updates)
│
├── Footer (Minimal)
│   └── AI Status Indicator (small, non-intrusive)
│
└── SettingsPanel (Modal Overlay)
    ├── Tab: Now Playing (quick controls)
    ├── Tab: Library (song management)
    └── Tab: AI Band (future: accompaniment)
```

---

## 🎭 Detailed View Specifications

### View 1: Teleprompter (Living Chart)

**Purpose:** Fullscreen lyrics display with real-time highlighting during performance

**Layout:**
```
┌─────────────────────────────────────────────┐
│  [minimal header: song title + settings]    │  ← 60px height
├─────────────────────────────────────────────┤
│                                             │
│                                             │
│        [ Verse 1 ]   ← past section         │  ← Dimmed (30% opacity)
│        Sung lyrics   ← sung lines           │
│                                             │
│  ╔═══════════════════════════════════════╗ │
│  ║   C              G                    ║ │  ← Current line (centered)
│  ║   Here comes the sun ◆ doo doo doo   ║ │  ← ◆ = current syllable
│  ╚═══════════════════════════════════════╝ │     Cyan highlight + pulse
│                                             │
│        Upcoming lyrics                      │  ← Full brightness
│                                             │
│        [ Chorus ]   ← next section          │
│                                             │
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

**Interaction Design:**

1. **Auto-Scroll Behavior**
   - Active line ALWAYS vertically centered (50% viewport)
   - Smooth transform animation (500ms ease-in-out)
   - Past lines scroll up, fade to 30% opacity
   - Future lines wait at full brightness below

2. **Syllable Highlighting**
   - Current syllable: Cyan background + white text + subtle pulse
   - Progress bar below syllable fills left-to-right
   - Sung syllables: Dimmed text (70% opacity)
   - Unsung syllables: Full brightness (100% opacity)

3. **Chord Display**
   - Chords appear ABOVE syllables (not inline)
   - Amber color (#FACC15) for maximum contrast
   - Click chord → Shows fingering diagram (optional)
   - Diagram appears as overlay, doesn't shift layout

4. **Emergency Controls** (NEW)
   - **Double-tap screen** → Mini control bar slides in from right
   - Controls: Font slider, Transpose ±, Pause/Play
   - Auto-hides after 3 seconds of inactivity
   - Translucent background (doesn't obscure lyrics)

5. **Performance Metrics** (Subtle, Bottom Corner)
   - Small "listening" icon pulses with beat
   - BPM display (optional, settings toggle)
   - Key indicator (optional)

**States:**

| State | Visual Treatment | Interaction |
|-------|------------------|-------------|
| **Idle** | Lyrics visible, no highlights | Waiting for playback |
| **Playing** | Syllables highlight in real-time | Auto-scroll active |
| **Paused** | Current syllable frozen | Scroll position held |
| **Seeking** | Jump to new position | Smooth scroll to target |
| **Error** | Gentle red tint on header | Error message in overlay |

**Accessibility:**

- High contrast mode: Black text on white (toggle in settings)
- Keyboard navigation: Space = play/pause, ←/→ = prev/next section
- Screen reader: Announces section changes, current line
- Reduced motion: Instant jump instead of smooth scroll

---

### View 2: Blueprint (Edit Mode)

**Purpose:** Document-style editor for song structure, chords, and metadata

**Layout:**
```
┌─────────────────────────────────────────────┐
│  [Header with "Back to Performance" button] │
├─────────────────────────────────────────────┤
│                                             │
│   ┌───────────────────────────────────┐    │
│   │  Song Title (editable)            │    │  ← Click to edit inline
│   │  Artist Name (editable)           │    │
│   │  Key: C Major  |  BPM: 120  |  4/4│    │  ← Metadata bar
│   └───────────────────────────────────┘    │
│                                             │
│   ┌─ [ Verse 1 ] ────────────────────┐    │
│   │                                   │    │
│   │   C                    G          │    │  ← Chord line (editable)
│   │   Here comes the sun             │    │  ← Lyric line (editable)
│   │                                   │    │
│   │   C            Em         D       │    │
│   │   Little darling, it's been a... │    │
│   │                                   │    │
│   └───────────────────────────────────┘    │
│                                             │
│   ┌─ [ Chorus ] ──────────── [⋮] ──┐      │  ← Drag handle (reorder)
│   │   ...                           │      │
│   └─────────────────────────────────┘      │
│                                             │
│   [+ Add Section]                          │  ← Button to insert
│                                             │
└─────────────────────────────────────────────┘
```

**Interaction Design:**

1. **Inline Editing**
   - Click any text → Contenteditable mode
   - Type chord symbols → Autocomplete popup (C, Cm, C7, etc.)
   - Press Enter → Save, move to next line
   - Press Esc → Cancel edit

2. **Drag-to-Reorder**
   - Hover section header → Drag handle (⋮) appears
   - Click + drag → Section lifts, others shift down
   - Drop → Smooth animation to new position
   - Visual feedback: Drop zones highlighted

3. **Chord Autocomplete** (NEW, Critical Feature)
   ```
   User types: "Cma"
   Popup shows:
   ┌──────────────┐
   │ Cmaj        │ ← Most common
   │ Cmaj7       │
   │ Cmaj9       │
   │ Cm/Ab       │
   └──────────────┘
   Arrow keys to navigate, Enter to select
   ```

4. **Timeline Mode** (Future Enhancement)
   - Toggle button in header
   - Shows syllable timing bars below lyrics
   - Drag edges to adjust timing
   - Real-time preview in side panel

5. **Section Management**
   - Right-click section header → Context menu
     - Duplicate Section
     - Delete Section
     - Change Type (Verse/Chorus/Bridge/etc.)
   - Keyboard shortcuts: Cmd+D duplicate, Del to delete

**Validation:**

- Real-time chord validation (invalid → red underline)
- Timing conflict detection (overlapping syllables → warning icon)
- Empty section warning (section with no lyrics → yellow border)

---

### View 3: Library

**Purpose:** Fast song search and selection, library management

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Library                            [✕ Close]│
├─────────────────────────────────────────────┤
│  ┌───────────────────────────────────────┐  │
│  │  🔍 Search songs...                   │  │  ← Instant search (autocomplete)
│  └───────────────────────────────────────┘  │
│                                             │
│  Sort by: [Title ▼]  [↑ Asc]  [Grid/List]  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  ♪  Yesterday                       │   │  ← Song card (click to load)
│  │      The Beatles                    │   │
│  │      Key: F  •  BPM: 76  •  Rock    │   │  ← Metadata
│  │      [▶ Play]  [✏ Edit]  [⋯ More]  │   │  ← Quick actions
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  ♪  Here Comes The Sun              │   │
│  │      The Beatles                    │   │
│  │      Key: A  •  BPM: 129  •  Rock   │   │
│  │      [▶ Play]  [✏ Edit]  [⋯ More]  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [+ Upload New Song]                        │
│                                             │
└─────────────────────────────────────────────┘
```

**Search Behavior:**

- **Instant results** as user types (no search button)
- Searches: Title, Artist, Lyrics content, Tags, Key, Genre
- Fuzzy matching ("yester" finds "Yesterday")
- Highlight matching text in results
- Keyboard navigation: ↑/↓ to navigate, Enter to select

**Quick Actions:**

- **▶ Play**: Load in Teleprompter, start playback immediately
- **✏ Edit**: Open in Blueprint View
- **⋯ More**:
  - Export as JSON
  - Duplicate
  - Add to Setlist (future)
  - Delete (with confirmation)

**Sorting & Filtering:**

- Sort by: Title, Artist, Date Added, Last Played, BPM, Key
- Filter by: Genre, Difficulty, Tags
- Save filter presets (e.g., "Jazz Standards", "Easy Songs")

---

### Component: Settings Panel

**Purpose:** Quick access to performance controls without leaving current view

**Layout (Slide-in from Left):**
```
┌─────────────────────────┐
│  Settings         [✕]  │
├─────────────────────────┤
│  ┌─ Now Playing ─┐     │  ← Tab 1 (Active)
│  │  Library       │     │  ← Tab 2
│  │  AI Band       │     │  ← Tab 3 (Future)
│  └────────────────┘     │
│                         │
│  ⚡ Live Controls        │
│  ┌─────────────────┐   │
│  │ Chord Display   │   │
│  │ [Off|Names|Diagrams]│  ← Segmented control
│  └─────────────────┘   │
│                         │
│  Font Size: 120%       │
│  [───●────────────]    │  ← Slider (50-150%)
│                         │
│  🎵 Musical Tools       │
│  Transpose: +2         │
│  [-] [+2] [+]          │  ← Quick adjust
│                         │
│  Capo: Fret 3          │
│  [-] [Fret 3] [+]      │
│                         │
│  ──────────────────    │
│                         │
│  [Reset All Settings]  │
│                         │
└─────────────────────────┘
```

**Tab 1: Now Playing**
- Performance controls (font, chords, transpose, capo)
- Quick reset button
- Preset save/load (future)

**Tab 2: Library**
- Embedded LibraryView (search + select)
- Current song indicator
- Recent songs list

**Tab 3: AI Band** (Future)
- Accompaniment settings
- Instrument selection
- Mix volume controls

**Behavior:**

- Opens from left side (384px width)
- Backdrop overlay (dimmed, click to close)
- Changes apply instantly (no "Save" button)
- Auto-closes when song selected from library
- Keyboard shortcut: Cmd+, to toggle

---

## 🎬 Interaction Patterns

### Pattern 1: View Switching

**Trigger:** Click song title in header

**Behavior:**
```
Teleprompter ⟷ Blueprint
   (Instant toggle, no animation)

State preserved:
- Font size
- Transpose
- Scroll position (on return)
```

**Rationale:** Musicians need to quickly jump to editing without losing context.

---

### Pattern 2: Real-Time Highlighting

**Trigger:** Audio playback with syllable timing

**Algorithm:**
```javascript
Every 16ms (60fps):
  1. Get current playback time
  2. Find syllable where: startTime ≤ currentTime < endTime
  3. Calculate progress: (currentTime - startTime) / duration
  4. Update:
     - Highlight current syllable (background + border)
     - Fill progress bar (0-100%)
     - Scroll if active line changed
  5. Dim past syllables
```

**Performance:**
- Use CSS transforms (GPU-accelerated)
- RequestAnimationFrame for smooth 60fps
- Memoize syllable lookups (binary search by time)

---

### Pattern 3: Emergency Font Adjust

**Trigger:** Double-tap screen during performance

**Flow:**
```
1. Double-tap detected → Mini control bar slides in (300ms)
2. Shows: Font slider ONLY (most critical control)
3. User drags → Font changes in real-time
4. 3 seconds of inactivity → Auto-hide (300ms fade)
```

**Rationale:** Performer realizes font too small mid-song, needs instant fix without menu diving.

---

### Pattern 4: Chord Autocomplete

**Trigger:** Typing in Blueprint chord field

**Flow:**
```
1. User types "C" → Popup shows: C, Cm, C7, Cmaj7, C9...
2. Types "m" → Filters to: Cm, Cm7, Cmaj7, Cmin...
3. Arrow down → Highlight "Cm7"
4. Enter → Insert "Cm7", close popup, move to next field
```

**Smart Features:**
- Common chords first (C, Cm, C7 before C13sus4)
- Recent chords bubble up
- Suggest chord progression (if in key of C, suggest C → F → G)

---

## ♿ Accessibility Requirements

### Keyboard Navigation (Full Coverage)

| Key | Action | Context |
|-----|--------|---------|
| **Space** | Play/Pause | Teleprompter |
| **←/→** | Prev/Next Section | Teleprompter |
| **Cmd/Ctrl + ,** | Open Settings | Global |
| **Cmd/Ctrl + L** | Open Library | Global |
| **Cmd/Ctrl + E** | Toggle Edit Mode | Global |
| **Esc** | Close Overlay/Modal | Global |
| **Tab** | Navigate Controls | Settings |
| **Cmd/Ctrl + ↑/↓** | Font Size ±10% | Teleprompter |

### Screen Reader Support

- Semantic HTML: `<header>`, `<main>`, `<nav>`, `<section>`
- ARIA labels: `aria-label`, `aria-live` for dynamic content
- Announce: Section changes, playback state, errors
- Skip links: "Skip to lyrics", "Skip to controls"

### Visual Accessibility

- **Contrast Ratios:**
  - Lyrics: 16:1 (AAA)
  - Chords: 7:1 (AAA)
  - UI Controls: 4.5:1 (AA minimum)
- **High Contrast Mode:** Invert to black-on-white
- **Reduced Motion:** Disable smooth scrolling/animations
- **Focus Indicators:** 2px cyan outline on all interactive elements

### Touch Accessibility

- Minimum touch target: 44x44px (WCAG AAA)
- Spacing between targets: 8px minimum
- Swipe gestures optional (keyboard alternative always available)

---

## 📱 Responsive Design (Future)

### Breakpoints

```css
/* Desktop (Default) */
@media (min-width: 1024px) {
  /* Full feature set, side-by-side panels */
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Stacked panels, settings as fullscreen modal */
}

/* Mobile (< 768px) */
@media (max-width: 767px) {
  /* Teleprompter only, minimal chrome */
  /* Settings as bottom sheet */
  /* Font automatically larger (viewport-relative) */
}
```

---

## 🚀 Performance Targets

### Core Web Vitals

| Metric | Target | Rationale |
|--------|--------|-----------|
| **LCP** (Largest Contentful Paint) | <1.5s | Lyrics must appear instantly |
| **FID** (First Input Delay) | <50ms | Controls must feel instant |
| **CLS** (Cumulative Layout Shift) | 0 | Layout shift during performance = disaster |
| **Frame Rate** | 60fps | Smooth scrolling, no jank |
| **Syllable Highlight Latency** | <16ms | Real-time feel (1 frame) |

### Bundle Size

- Initial JS: <200KB gzipped
- Initial CSS: <50KB gzipped
- Font files: <100KB (subset to used glyphs)
- Total TTI (Time to Interactive): <2s on 3G

---

## 🎨 Animation Specifications

### Scroll Animation (Teleprompter)

```css
.lyrics-container {
  transition: transform 500ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Easing:** Ease-in-out for natural feel
**Duration:** 500ms (perceived as smooth, not sluggish)

### Syllable Highlight

```css
.syllable-active {
  animation: pulse 1s ease-in-out infinite;
  background: var(--highlight-current);
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.6);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}
```

### Modal/Panel Transitions

```css
.settings-panel {
  transition: transform 300ms ease-out;
  transform: translateX(-100%); /* Hidden */
}

.settings-panel.open {
  transform: translateX(0); /* Visible */
}
```

---

## 🧩 Component API Reference

### TeleprompterView

```typescript
interface TeleprompterViewProps {
  songMap: SongMap;
  transpose: number;        // -12 to +12
  capo: number;             // 0 to 12
  chordDisplay: 'off' | 'names' | 'diagrams';
  fontSize: number;         // 50 to 150 (percentage)
  isPlaying: boolean;
  currentTime: number;      // Seconds (for highlighting)
  onSeek: (time: number) => void;
  onChordClick?: (chord: string) => void;
}
```

### BlueprintView

```typescript
interface BlueprintViewProps {
  songMap: SongMap;
  onSongMapChange: (newSongMap: SongMap) => void;
  onSectionReorder?: (fromIndex: number, toIndex: number) => void;
  readOnly?: boolean;
}
```

### LibraryView

```typescript
interface LibraryViewProps {
  songs: LibrarySong[];
  currentSongId?: string;
  onSongSelect: (songMap: SongMap) => void;
  onSongDelete?: (id: string) => void;
  onSongEdit?: (id: string) => void;
}
```

---

## 🔮 Future Enhancements (Post-MVP)

### Phase 2: Advanced Features

1. **Setlist Management**
   - Create setlists from library
   - Drag-to-order songs
   - Quick navigation between songs in set
   - Setlist sharing (export/import)

2. **Timeline Editor**
   - Visual syllable timing adjustment
   - Waveform display with lyrics overlay
   - Click-to-place syllable markers
   - Batch timing adjustments

3. **Collaborative Editing**
   - Share song with band members
   - Real-time collaborative edits
   - Comment/annotation system
   - Version history

4. **AI Accompaniment Controls**
   - Instrument selection (piano, guitar, drums, bass)
   - Mix volume sliders
   - Style selection (rock, jazz, blues, etc.)
   - Real-time accompaniment preview

### Phase 3: Advanced UX

5. **Gesture Controls**
   - Swipe left/right: Prev/Next section
   - Pinch to zoom: Font size
   - Two-finger scroll: Manual scroll override
   - Shake to reset

6. **Voice Commands**
   - "Next section"
   - "Transpose up 2"
   - "Play from chorus"
   - Works during performance (background listening)

7. **Customizable Themes**
   - Dark mode (default)
   - Light mode (daytime rehearsal)
   - High contrast mode
   - Custom color schemes
   - Save theme presets

---

## ✅ Definition of Done (UX Implementation)

A feature is complete when:

1. **Functional:**
   - ✅ Works as specified in all user workflows
   - ✅ Handles edge cases gracefully
   - ✅ No console errors

2. **Accessible:**
   - ✅ Keyboard navigable
   - ✅ Screen reader compatible
   - ✅ WCAG AA minimum (AAA for critical elements)
   - ✅ Meets touch target minimums

3. **Performant:**
   - ✅ Meets performance targets (60fps, <100ms interactions)
   - ✅ No layout shifts
   - ✅ Smooth on mid-range devices

4. **Tested:**
   - ✅ Unit tests for logic
   - ✅ Integration tests for workflows
   - ✅ Manual testing on 3 devices (desktop, tablet, mobile)
   - ✅ Accessibility audit passed

5. **Documented:**
   - ✅ Component API documented
   - ✅ User-facing help text added
   - ✅ Code comments for complex logic

---

## 📊 Success Metrics

### Quantitative (Track in Analytics)

- **Time to First Performance:** <30 seconds (from app open)
- **Song Selection Speed:** <5 seconds (search → select)
- **Settings Adjustment Speed:** <2 seconds (open → change → close)
- **Error Rate:** <1% of sessions
- **Frame Rate:** >58fps average (allow 2 dropped frames)

### Qualitative (User Feedback)

- **Ease of Use:** 4.5+ stars (out of 5)
- **Feature Discovery:** >80% find key features without tutorial
- **Performance Satisfaction:** "Feels instant" in >90% of feedback
- **Visual Clarity:** "Easy to read" in >95% of feedback

---

## 🎯 Implementation Priority (Roadmap Alignment)

### Sprint 2 (This Week) - BACKEND FOCUS
**Frontend:** Minimal changes, prepare for adapter
- Document adapter integration points
- Plan UI for Song Map upload feedback

### Sprint 3 (Oct 8-21) - UX IMPROVEMENTS
**Frontend:** Implement accessibility + performance
1. VIZTRITR contrast fixes (one at a time)
2. Focus indicators
3. Hover states
4. 60fps rendering optimization

### Sprint 4 (Oct 22 - Nov 4) - POLISH
**Frontend:** Final UX refinements
5. Emergency font adjust (double-tap)
6. Chord autocomplete in Blueprint
7. Library search autocomplete
8. Animation polish

### Sprint 5 (Nov 5-18) - ADVANCED FEATURES
**Frontend:** New capabilities
9. Setlist management
10. Timeline editor (if backend supports)
11. Theme customization

---

## 📝 Notes for Developer

**While I work on the backend adapter, you should:**

1. **Review this spec thoroughly** - Challenge any unclear parts
2. **Sketch UI mockups** - Visualize the workflows
3. **Identify technical blockers** - What needs backend changes?
4. **Prioritize quick wins** - Which improvements are low-hanging fruit?

**Questions to Consider:**

- Does the "double-tap for font adjust" gesture conflict with anything?
- Is 44px touch target feasible given current layout?
- Can we achieve 60fps with current React architecture? (Virtual DOM overhead?)
- Should we use Canvas for Teleprompter instead of DOM? (Performance vs accessibility trade-off)

---

## 🏁 Conclusion

This specification defines a **musician-first UI** that:

✅ **Disappears during performance** - Fullscreen lyrics, zero chrome
✅ **Emerges for control** - Quick settings access, no menu diving
✅ **Matches mental models** - Sections, chords, keys (how musicians think)
✅ **Accessible by default** - Keyboard, screen reader, high contrast
✅ **Feels instant** - <100ms interactions, 60fps animations

**Core Philosophy:** *The best interface for performance is no interface at all.*

---

**Version:** 2.0 - Definitive UX Specification
**Last Updated:** October 1, 2024
**Next Review:** End of Sprint 3 (Oct 21, 2024)
**Owner:** Frontend Team (Daniel + Claude frontend-dev agent)
