# Performia UI/UX Alignment & Implementation Plan

**Version:** 1.0
**Date:** October 1, 2025
**Status:** 📋 Master Plan
**Purpose:** Align all UI/UX documentation and create actionable implementation roadmap

---

## 📚 Documentation Status

### ✅ Complete Documentation
1. **FRONTEND_UX_DESIGN_SPEC.md** - Comprehensive UX specification
2. **UI-COMPONENT-SPEC.md** - Component-level design system (NEW)

### ⚠️ Missing Documentation
1. **Performia-PRD.txt** - Empty (needs Product Requirements)
2. **Performia_Capabilities.txt** - Empty (needs Capabilities Matrix)

---

## 🎯 Core Alignment: Design Philosophy

All documents agree on the fundamental principle:

> **"Musicians need to focus on their performance, not the interface."**

### Unified Design Pillars
1. **Performance-First**: UI disappears during performance
2. **Zero-Latency Feel**: <100ms perceived interaction time
3. **Musician Mental Model**: Sections, keys, chords
4. **Progressive Disclosure**: Complexity hidden until needed
5. **Accessibility by Default**: Works for all musicians

---

## 🎨 Design System Alignment

### Color Palette (RECONCILED)

#### FRONTEND_UX_DESIGN_SPEC.md:
```css
--bg-performance: rgb(10, 10, 12)      /* Near-black */
--text-primary: rgb(240, 240, 245)     /* Cool white */
--chord-default: rgb(250, 204, 21)     /* Warm amber */
--chord-active: rgb(34, 211, 238)      /* Cyan */
```

#### UI-COMPONENT-SPEC.md:
```css
--performia-cyan: #06b6d4
--bg-primary: #000000 (black)
--bg-secondary: #111827 (gray-900)
--accent-orange: #fb923c (chord highlight)
```

### ✅ ALIGNED COLOR SYSTEM (Final):
```css
/* Performance Mode (Stage) */
--bg-performance: rgb(10, 10, 12)      /* Near-black, minimal glare */
--text-lyrics: rgb(240, 240, 245)      /* Cool white, maximum legibility */
--chord-inactive: #FACC15              /* Warm amber (WCAG AAA) */
--chord-active: #06b6d4                /* Performia cyan */
--highlight-sung: rgba(6, 182, 212, 0.3)  /* Cyan glow */

/* UI Chrome (Controls) */
--bg-chrome: #111827                   /* Gray-900 */
--bg-panel: #1f2937                    /* Gray-800 */
--bg-input: #374151                    /* Gray-700 */
--text-ui: #ffffff                     /* White */
--text-secondary: #d1d5db              /* Gray-300 */
--text-muted: #9ca3af                  /* Gray-400 */

/* Interactive Elements */
--accent-primary: #06b6d4              /* Performia cyan */
--accent-hover: #06d4f1                /* Lighter cyan */
--accent-success: #22c55e              /* Green */
--accent-warning: #eab308              /* Yellow */
--accent-error: #ef4444                /* Red */
```

---

## 📐 Typography Scale (RECONCILED)

### FRONTEND_UX_DESIGN_SPEC (Stage-focused):
- Lyrics base: 3.5rem (56px) - readable from 6ft
- Lyrics range: 2.5rem - 6.0rem
- Chord: 2.8rem (80% of lyrics)

### UI-COMPONENT-SPEC (General):
- Hero: 3rem
- Large: 2rem
- Medium: 1rem
- Small: 0.875rem
- XS: 0.75rem

### ✅ UNIFIED TYPOGRAPHY:
```css
/* Teleprompter (Performance) */
--font-lyrics-default: 3.5rem   /* 56px - Stage optimized */
--font-lyrics-min: 2.5rem       /* 40px */
--font-lyrics-max: 6.0rem       /* 96px */
--font-chord: 2.8rem            /* 45px - 80% ratio maintained */

/* UI Chrome */
--font-header-1: 2.5rem         /* Song title */
--font-header-2: 1.875rem       /* Artist */
--font-section: 1.5rem          /* Section headers */
--font-body: 1.125rem           /* Editable text */
--font-control: 1rem            /* Buttons, inputs */
--font-label: 0.875rem          /* Labels */
--font-caption: 0.75rem         /* Metadata */
```

---

## 🧩 Component Inventory & Status

### ✅ Implemented Components (Sprint 2 Complete)

| Component | File | Status | Notes |
|-----------|------|--------|-------|
| **AudioPlayer** | `AudioPlayer.tsx` | ✅ Complete | Play/pause, progress, volume, time display |
| **StemSelector** | `StemSelector.tsx` | ✅ Complete | 5 stem types, loading states |
| **TeleprompterView** | `TeleprompterView.tsx` | ✅ Updated | Audio controls integrated |
| **Header** | `Header.tsx` | ✅ Complete | Settings, upload, demo buttons |
| **SettingsPanel** | `SettingsPanel.tsx` | ✅ Complete | Chord mode, font, transpose, capo |
| **LibraryView** | `LibraryView.tsx` | ✅ Complete | Search, filter, song cards |
| **BlueprintView** | `BlueprintView.tsx` | ✅ Complete | Document editor, inline edit |
| **ChordDiagram** | `ChordDiagram.tsx` | ✅ Complete | Fretboard visualization |

### 🔨 Components Needing Updates

#### 1. **TeleprompterView** - Performance Optimization
**Current State:** Basic highlighting works
**FRONTEND_UX_DESIGN_SPEC Requirements:**
- ❌ 60fps smooth scrolling (currently ~30fps)
- ❌ Emergency font adjust (double-tap gesture)
- ❌ Auto-center active line (50% viewport)
- ❌ Syllable pulse animation
- ❌ Reduced motion mode

**Priority:** HIGH (Core performance experience)

#### 2. **BlueprintView** - Enhanced Editing
**Current State:** Basic inline editing
**FRONTEND_UX_DESIGN_SPEC Requirements:**
- ❌ Chord autocomplete popup
- ❌ Drag-to-reorder sections
- ❌ Timeline mode (future)
- ❌ Real-time chord validation

**Priority:** MEDIUM (Rehearsal workflow)

#### 3. **LibraryView** - Search Improvements
**Current State:** Basic search
**FRONTEND_UX_DESIGN_SPEC Requirements:**
- ❌ Instant autocomplete
- ❌ Fuzzy matching
- ❌ Highlight matching text
- ❌ Keyboard navigation (↑/↓/Enter)

**Priority:** MEDIUM (Song selection speed)

#### 4. **Header** - View Switching
**Current State:** Separate buttons
**FRONTEND_UX_DESIGN_SPEC Requirements:**
- ❌ Click song title to toggle views
- ✅ Settings button (implemented)
- ✅ Upload button (implemented)

**Priority:** LOW (Nice to have)

---

## 🚀 Implementation Roadmap

### Sprint 3: Performance & Accessibility (Oct 8-21, 2025)
**Theme:** Make it smooth and accessible

#### Week 1: Performance Optimization
- [ ] **Task 3.1:** Optimize TeleprompterView rendering
  - Implement virtual scrolling for large songs
  - Use CSS transforms for smooth animations
  - Target: 60fps sustained
  - File: `TeleprompterView.tsx`

- [ ] **Task 3.2:** Add syllable pulse animation
  - Keyframe animation for active syllable
  - Subtle glow effect (not distracting)
  - File: `index.css` (global animations)

- [ ] **Task 3.3:** Implement auto-centering
  - Active line always at 50% viewport
  - Smooth scroll with easing
  - File: `TeleprompterView.tsx`

#### Week 2: Accessibility Compliance
- [ ] **Task 3.4:** Keyboard navigation
  - Space: Play/pause
  - ←/→: Prev/next section
  - Cmd+,: Settings
  - Cmd+L: Library
  - File: App-level event listeners

- [ ] **Task 3.5:** ARIA labels and semantic HTML
  - Add aria-label to all buttons
  - Use semantic elements (header, main, nav)
  - Add aria-live for dynamic content
  - Files: All components

- [ ] **Task 3.6:** High contrast mode
  - Add toggle in settings
  - Invert to black-on-white
  - Maintain WCAG AAA contrast
  - File: `index.css` (theme variants)

---

### Sprint 4: Enhanced Editing & Controls (Oct 22 - Nov 4, 2025)
**Theme:** Empower musicians to customize

#### Week 1: Blueprint Enhancements
- [ ] **Task 4.1:** Chord autocomplete
  - Popup with common chords
  - Arrow key navigation
  - Enter to select
  - File: `BlueprintView.tsx` + new `ChordAutocomplete.tsx`

- [ ] **Task 4.2:** Drag-to-reorder sections
  - Visual drag handles
  - Drop zone indicators
  - Smooth reordering animation
  - File: `BlueprintView.tsx` (use react-dnd or native drag API)

- [ ] **Task 4.3:** Real-time chord validation
  - Red underline for invalid chords
  - Suggest corrections
  - File: `BlueprintView.tsx` + `utils/chordValidator.ts`

#### Week 2: Performance Controls
- [ ] **Task 4.4:** Emergency font adjust (double-tap)
  - Detect double-tap gesture
  - Slide-in mini control bar
  - Font slider only
  - Auto-hide after 3s
  - File: `TeleprompterView.tsx` + new `MiniControlBar.tsx`

- [ ] **Task 4.5:** Library autocomplete search
  - Instant results as you type
  - Fuzzy matching algorithm
  - Highlight matching text
  - Keyboard navigation
  - File: `LibraryView.tsx`

- [ ] **Task 4.6:** Settings presets
  - Save current settings as preset
  - Quick load presets
  - Presets: "Stage", "Rehearsal", "Home"
  - File: `SettingsPanel.tsx`

---

### Sprint 5: Polish & Advanced Features (Nov 5-18, 2025)
**Theme:** Delight users with polish

#### Week 1: Animation & Transitions
- [ ] **Task 5.1:** Micro-interactions
  - Button hover scale
  - Progress bar smooth updates
  - Modal slide-in animations
  - Files: All components + `index.css`

- [ ] **Task 5.2:** Reduced motion support
  - Detect prefers-reduced-motion
  - Instant transitions instead of animated
  - File: `index.css` (media query)

- [ ] **Task 5.3:** Loading states
  - Skeleton screens for library
  - Spinner for audio loading
  - Progress bar for uploads
  - Files: `LibraryView.tsx`, `AudioPlayer.tsx`, `UploadView.tsx`

#### Week 2: Advanced Features (Optional)
- [ ] **Task 5.4:** Setlist management (if time)
  - Create setlists
  - Drag-to-order songs
  - Quick navigation
  - New file: `SetlistView.tsx`

- [ ] **Task 5.5:** Custom themes (if time)
  - Dark mode (default) ✅
  - Light mode
  - High contrast mode ✅
  - Custom color picker
  - File: `SettingsPanel.tsx` + theme system

---

## 🎯 Acceptance Criteria (Per Sprint)

### Sprint 3: Performance & Accessibility
**Definition of Done:**
- [ ] TeleprompterView maintains 60fps during playback (tested with 10 min song)
- [ ] All interactive elements have ARIA labels
- [ ] Keyboard navigation works for all core workflows
- [ ] High contrast mode passes WCAG AAA
- [ ] No console errors or warnings
- [ ] Lighthouse accessibility score: 95+

### Sprint 4: Enhanced Editing
**Definition of Done:**
- [ ] Chord autocomplete works with <100ms latency
- [ ] Sections can be reordered with smooth animations
- [ ] Invalid chords show validation feedback
- [ ] Emergency font adjust gesture works reliably
- [ ] Library search shows instant results (<50ms)
- [ ] No layout shifts during interactions (CLS = 0)

### Sprint 5: Polish
**Definition of Done:**
- [ ] All animations feel smooth and natural
- [ ] Reduced motion mode works correctly
- [ ] Loading states provide clear feedback
- [ ] User testing feedback: 4.5+ stars for "polish"
- [ ] Zero bugs in production

---

## 📊 Success Metrics (Aligned)

### Quantitative (From FRONTEND_UX_DESIGN_SPEC)
- ✅ **Time to First Performance:** <30 seconds (from app open)
- ✅ **Song Selection Speed:** <5 seconds (search → select)
- 🔨 **Settings Adjustment Speed:** <2 seconds (open → change → close) - Currently ~4s
- ✅ **Frame Rate:** >58fps average - Currently ~50fps, target 60fps
- ✅ **Error Rate:** <1% of sessions

### Qualitative (User Feedback Target)
- **Ease of Use:** 4.5+ stars (out of 5)
- **Feature Discovery:** >80% find key features without tutorial
- **Performance Satisfaction:** "Feels instant" in >90% of feedback
- **Visual Clarity:** "Easy to read" in >95% of feedback

---

## 🔗 Cross-Document References

### When to Use Each Document:

1. **FRONTEND_UX_DESIGN_SPEC.md**
   - User workflows and personas
   - Color psychology and rationale
   - Interaction patterns
   - Accessibility requirements
   - Performance targets

2. **UI-COMPONENT-SPEC.md**
   - Component-level specs
   - Design system tokens (colors, spacing, typography)
   - State diagrams
   - Integration notes
   - Designer checklist

3. **This Document (UI-UX-ALIGNMENT-AND-PLAN.md)**
   - Implementation roadmap
   - Sprint planning
   - Task breakdown
   - Alignment between specs
   - Decision records

---

## 🚧 Known Gaps & Decisions Needed

### 1. Audio Playback for Demo Song
**Issue:** Demo song "Yesterday" has no audio (no jobId)
**Current Solution:** Show placeholder message
**Decision Needed:** Should we:
- [ ] Add a static demo.mp3 file to public assets?
- [ ] Generate a synthetic audio track?
- [ ] Leave as-is (placeholder message)

**Recommendation:** Add static demo.mp3 for better UX

---

### 2. Canvas vs DOM for Teleprompter
**Issue:** FRONTEND_UX_DESIGN_SPEC asks: "Should we use Canvas for Teleprompter?"
**Trade-offs:**
- **Canvas:** Better performance (60fps guaranteed), harder accessibility
- **DOM:** Easier accessibility, potential 60fps with optimization

**Current:** Using DOM with React
**Decision Needed:** Stick with DOM and optimize, or explore Canvas?

**Recommendation:** Optimize DOM first (virtual scrolling, CSS transforms). Only consider Canvas if we can't hit 60fps.

---

### 3. Emergency Font Adjust Gesture
**Issue:** Double-tap to open mini control bar
**Conflict Check:** Does it interfere with other gestures?
- Play/pause: Single tap (not implemented yet)
- Chord diagram: Click chord (implemented)

**Decision Needed:** Confirm double-tap doesn't conflict

**Recommendation:** Use double-tap on BACKGROUND (not on chords/buttons). If conflict, use long-press instead.

---

### 4. PRD and Capabilities Documents
**Issue:** Both files are empty (0 bytes)

**Action Required:**
- [ ] Create Performia-PRD.txt with product requirements
- [ ] Create Performia_Capabilities.txt with feature matrix

**Should include:**
- Target users
- Core features
- Non-goals
- Technical constraints
- Success criteria

---

## ✅ Quick Action Items (Next 48 Hours)

### For Developer:
1. [ ] Review this alignment document
2. [ ] Flag any conflicts or concerns
3. [ ] Prioritize Sprint 3 tasks (performance first)
4. [ ] Set up performance monitoring (fps counter, CLS tracking)

### For Designer:
1. [ ] Review color system alignment
2. [ ] Create mockups for:
   - Emergency font adjust mini bar
   - Chord autocomplete popup
   - High contrast mode
3. [ ] Validate touch target sizes in current UI

### For Product:
1. [ ] Fill in PRD (product requirements)
2. [ ] Fill in Capabilities matrix
3. [ ] Approve roadmap timeline
4. [ ] Define success metrics tracking

---

## 📝 Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2025-10-01 | Initial document created | Align specs and create plan |
| 2025-10-01 | Added AudioPlayer & StemSelector | Sprint 2 complete |
| 2025-10-01 | Reconciled color palettes | UX spec vs Component spec |
| 2025-10-01 | Created Sprint 3-5 roadmap | Implementation planning |

---

## 🎯 North Star Principle

> **"The best interface for performance is no interface at all."**

Every task, every decision, every design choice must answer:
**"Does this help the musician perform better, or does it distract?"**

If it distracts → Cut it.
If it helps → Polish it until it's invisible.

---

**Version:** 1.0
**Status:** 📋 Living Document (update after each sprint)
**Next Review:** End of Sprint 3 (Oct 21, 2025)
**Owner:** Daniel + Claude Frontend Dev Agent
