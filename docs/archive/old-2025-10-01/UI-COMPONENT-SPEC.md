# Performia UI Component Specification

## Document Purpose
This document serves as a design specification for all UI components in Performia. Use this as a reference when creating mockups, design systems, or implementing enhanced UI versions.

---

## 🎵 Core Components

### 1. **AudioPlayer** ✨ NEW
**File:** `/frontend/components/AudioPlayer.tsx`

**Purpose:** Full-featured audio player with playback controls, progress bar, and volume control

**UI Elements:**
- **Progress Bar**
  - Draggable slider (0-100% of duration)
  - Visual fill showing current position
  - Color: Cyan (#06b6d4) for progress, Gray (#374151) for remaining
  - Height: 8px (2rem equivalent)

- **Play/Pause Button**
  - Background: Performia cyan (#06b6d4)
  - Hover: Lighter cyan (#06d4f1)
  - Text: Black
  - Icon: Play (▶) or Pause (⏸)
  - Padding: 6px vertical, 24px horizontal
  - Border radius: 8px

- **Time Display**
  - Font: Monospace
  - Format: MM:SS / MM:SS (current/total)
  - Size: Small (0.875rem)
  - Color: White
  - Min-width: 100px

- **Volume Controls**
  - Mute/Unmute button
    - Icons: 🔇 (muted), 🔉 (low), 🔊 (high)
    - Color: White, hover cyan
  - Volume slider
    - Width: 80px
    - Same styling as progress bar
    - Range: 0.0 - 1.0

**Container:**
- Background: Gray-800 (#1f2937)
- Padding: 16px
- Border radius: 8px
- Shadow: Large drop shadow

**States:**
- Playing (button shows pause)
- Paused (button shows play)
- Loading (disabled state)

---

### 2. **StemSelector** ✨ NEW
**File:** `/frontend/components/StemSelector.tsx`

**Purpose:** Toggle between audio stems (vocals, drums, bass, etc.)

**UI Elements:**
- **Section Header**
  - Title: "Audio Track" (semibold, gray-300)
  - Subtitle: "Select which audio track to play" (xs, gray-500)
  - Margin bottom: 8px

- **Stem Buttons** (5 buttons in flexbox)
  1. Full Mix (original)
  2. Vocals
  3. Bass
  4. Drums
  5. Other

  **Button States:**
  - **Selected:**
    - Background: Performia cyan (#06b6d4)
    - Text: Black
    - Shadow: Large
    - Scale: 105%
    - Icon: Play ▶

  - **Unselected:**
    - Background: Gray-700
    - Text: White
    - Hover: Gray-600

  - **Loading:**
    - Opacity: 50%
    - Spinning clock icon ⌛
    - Cursor: Wait

  - **Unavailable:**
    - Opacity: 60%
    - Grayed out appearance

- **Info Banner** (conditional)
  - Shows when non-original stem is selected
  - Background: Gray-800
  - Text: Gray-400
  - Cyan accent for "Note:" label
  - Padding: 8px
  - Border radius: 4px

**Layout:**
- Buttons: Horizontal flex-wrap with 8px gap
- Padding: 16px horizontal, 8px vertical
- Border radius: 8px

---

### 3. **TeleprompterView (Audio Controls Section)** ✨ UPDATED
**File:** `/frontend/components/TeleprompterView.tsx`

**New Section:** Audio Controls Bar (fixed at top)

**Two States:**

#### A. With Audio (jobId exists)
- **StemSelector** (top)
- **AudioPlayer** (bottom)
- Background: Gray-900 (#111827)
- Border: Bottom border gray-700
- Padding: 16px

#### B. Demo Mode (no jobId)
- **Placeholder Message:**
  - "Audio playback available for uploaded songs"
  - Sub-text: "Upload a song to enable real-time audio synchronization"
  - Text align: Center
  - Color: Gray-400
  - Font: SM main, XS sub
  - Padding: 8px vertical

**Container:**
- Background: Gray-900
- Border-bottom: 1px solid gray-700
- Z-index: 10 (above teleprompter)
- Position: Fixed at top of teleprompter view

---

## 📋 Existing Components Reference

### 4. **Header**
**File:** `/frontend/components/Header.tsx`

**Elements:**
- Settings button (gear icon, cyan background)
- Upload Song button
- Demo button
- Song title display (center)
- Artist name (subtitle)

### 5. **SettingsPanel**
**File:** `/frontend/components/SettingsPanel.tsx`

**Elements:**
- **LibraryView** (song selection)
- Chord display mode toggle
- Font size slider
- Transpose controls
- Capo settings
- Chord diagram visibility toggles

### 6. **LibraryView**
**File:** `/frontend/components/LibraryView.tsx`

**Elements:**
- Search bar
- Filter by tags/genre
- Song cards with metadata
- Recently played section

### 7. **BlueprintView**
**File:** `/frontend/components/BlueprintView.tsx`

**Elements:**
- Document-style editor
- Section headers
- Lyric line editing
- Chord insertion
- Timing adjustment

### 8. **ChordDiagram**
**File:** `/frontend/components/ChordDiagram.tsx`

**Elements:**
- Fretboard visualization
- Finger positions
- Chord name label

---

## 🎨 Design System

### Color Palette
```css
/* Primary */
--performia-cyan: #06b6d4
--performia-cyan-hover: #06d4f1
--performia-cyan-light: #67e8f9

/* Backgrounds */
--bg-primary: #000000 (black)
--bg-secondary: #111827 (gray-900)
--bg-tertiary: #1f2937 (gray-800)
--bg-quaternary: #374151 (gray-700)

/* Text */
--text-primary: #ffffff (white)
--text-secondary: #d1d5db (gray-300)
--text-tertiary: #9ca3af (gray-400)
--text-muted: #6b7280 (gray-500)

/* Accents */
--accent-orange: #fb923c (chord highlight)
--accent-purple: #a855f7 (active state)
```

### Typography Scale
- **Hero Text:** 3rem base (scales with fontSize setting)
- **Large:** 2rem
- **Medium:** 1rem
- **Small:** 0.875rem
- **Extra Small:** 0.75rem

### Spacing System
- **xs:** 4px
- **sm:** 8px
- **md:** 16px
- **lg:** 24px
- **xl:** 32px
- **2xl:** 48px

### Border Radius
- **sm:** 4px
- **md:** 8px
- **lg:** 12px
- **xl:** 16px
- **full:** 9999px (pill shape)

### Shadows
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1)
--shadow-cyan: 0 10px 15px rgba(6,182,212,0.2)
```

---

## 📐 Layout Grid

### Desktop (1920x1080 reference)
- **Header:** 80px height
- **Audio Controls:** ~120-180px height (dynamic)
- **Main Content:** flex-grow (remaining space)
- **Footer:** 80px height

### Responsive Breakpoints
- **Mobile:** < 640px
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

---

## 🔄 Animation & Transitions

### Standard Transitions
```css
transition: all 200ms ease-in-out
```

### Special Effects
- **Active syllable:** Color wipe animation (left to right)
- **Auto-scroll:** Transform translateY 500ms ease-in-out
- **Button hover:** Scale 105%, 200ms
- **Progress bar:** Width transition 300ms ease-out

---

## 📱 Interactive States

### All Buttons/Inputs
1. **Default:** Base styling
2. **Hover:** Brightness +10%, slight scale
3. **Active/Focus:** Ring outline (cyan, 4px)
4. **Disabled:** Opacity 50%, cursor not-allowed
5. **Loading:** Spinner icon, cursor wait

### Accessibility Requirements
- Minimum touch target: 44x44px
- ARIA labels on all interactive elements
- Keyboard navigation support
- High contrast mode support
- Screen reader friendly

---

## 📦 Component Hierarchy

```
App
├── Header
├── Main Content
│   ├── TeleprompterView
│   │   ├── Audio Controls Bar ✨ NEW
│   │   │   ├── StemSelector ✨ NEW
│   │   │   └── AudioPlayer ✨ NEW
│   │   └── Lyrics Display
│   ├── BlueprintView
│   └── SongMapDemo
├── Footer
└── SettingsPanel
    └── LibraryView
```

---

## 🎯 Component Integration Notes

### AudioPlayer Integration
- **Parent:** TeleprompterView
- **Props Required:**
  - `audioUrl: string` (from backend API or demo file)
  - `onTimeUpdate: (time: number) => void` (for syllable sync)
  - `onPlayStateChange?: (isPlaying: boolean) => void`

### StemSelector Integration
- **Parent:** TeleprompterView (when jobId exists)
- **Props Required:**
  - `jobId: string` (from upload process)
  - `onStemChange: (url: string, type: StemType) => void`

### Data Flow
```
Upload Song → Backend Processing → jobId
  ↓
jobId → Audio URL (original + stems)
  ↓
AudioPlayer + StemSelector render
  ↓
Real-time playback syncs with lyrics
```

---

## 📝 Designer Checklist

When creating mockups/designs, ensure you include:

- [ ] AudioPlayer in all 3 states (playing, paused, with/without audio)
- [ ] StemSelector with selected/unselected/loading states
- [ ] Demo mode placeholder message
- [ ] Audio controls integration with TeleprompterView
- [ ] Responsive layouts for mobile/tablet/desktop
- [ ] Dark theme variants (primary theme)
- [ ] Animation keyframes for progress bar and wipe effect
- [ ] Hover states for all interactive elements
- [ ] Focus/active states for accessibility
- [ ] Error states (audio load failed, stem unavailable)

---

## 🔗 Related Documentation

- [Song Map Schema](../backend/schemas/song_map.schema.json)
- [TypeScript Types](../frontend/types.ts)
- [API Endpoints](../backend/README.md)

---

**Document Version:** 1.0
**Last Updated:** 2025-10-01
**Maintainer:** Performia Development Team
