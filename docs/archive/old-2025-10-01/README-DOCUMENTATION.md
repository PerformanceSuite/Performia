# Performia Documentation Guide

**Last Updated:** October 1, 2025
**Purpose:** Navigation guide for all Performia documentation

---

## 📚 Documentation Structure

### 1. **Product & Requirements**
| Document | Purpose | When to Use |
|----------|---------|-------------|
| **Performia-PRD.txt** | Product Requirements Document | Understanding what we're building and why |
| **Performia_Capabilities.txt** | Feature inventory & status | Checking what's implemented and what's planned |

### 2. **Design & UX**
| Document | Purpose | When to Use |
|----------|---------|-------------|
| **FRONTEND_UX_DESIGN_SPEC.md** | Comprehensive UX specification | User workflows, personas, interaction patterns |
| **UI-COMPONENT-SPEC.md** | Component-level design system | Implementing specific components, designer reference |

### 3. **Planning & Alignment**
| Document | Purpose | When to Use |
|----------|---------|-------------|
| **UI-UX-ALIGNMENT-AND-PLAN.md** | Implementation roadmap | Sprint planning, task breakdown, alignment check |

---

## 🎯 Quick Reference: Which Doc Do I Need?

### "I need to understand the product vision"
→ **Performia-PRD.txt**
- Target users and personas
- Core features and priorities
- Success metrics
- Release plan

### "I need to know what features exist"
→ **Performia_Capabilities.txt**
- Complete feature inventory (65 MVP + 40 future)
- Implementation status (✅ 🔨 📋 🔮)
- Sprint breakdown
- Testing checklists

### "I need to design a user workflow"
→ **FRONTEND_UX_DESIGN_SPEC.md**
- User personas and workflows
- Color psychology and design rationale
- Accessibility requirements
- Performance targets

### "I need to implement a specific component"
→ **UI-COMPONENT-SPEC.md**
- Component specifications
- Design system tokens (colors, spacing, typography)
- State diagrams
- Props and integration notes

### "I need to plan the next sprint"
→ **UI-UX-ALIGNMENT-AND-PLAN.md**
- Sprint roadmap (Sprints 3-5)
- Task breakdown with priorities
- Acceptance criteria
- Open questions and decisions

---

## 🎨 Design System Quick Reference

### Color Palette
```css
/* Performance Mode */
--bg-performance: rgb(10, 10, 12)     /* Near-black */
--text-lyrics: rgb(240, 240, 245)     /* Cool white */
--chord-inactive: #FACC15             /* Amber */
--chord-active: #06b6d4               /* Performia cyan */

/* UI Chrome */
--bg-chrome: #111827                  /* Gray-900 */
--accent-primary: #06b6d4             /* Performia cyan */
```

### Typography
```css
/* Teleprompter */
--font-lyrics-default: 3.5rem         /* Stage optimized */
--font-chord: 2.8rem                  /* 80% of lyrics */

/* UI */
--font-control: 1rem                  /* Buttons */
--font-label: 0.875rem                /* Labels */
```

### Spacing
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

---

## 📊 Current Status (Sprint 2 Complete)

### ✅ Implemented (32 capabilities)
- Core teleprompter (display, highlight, scroll)
- Audio playback with stems (NEW)
- AudioPlayer component (NEW)
- StemSelector component (NEW)
- Song Map generation (backend)
- Basic library management
- Basic settings (font, transpose, capo)

### 🔨 In Progress
- 60fps rendering optimization (currently 50fps)
- Settings adjustment speed (currently 4s, target <2s)

### 📋 Next Sprint (Sprint 3: Oct 8-21)
- Accessibility (keyboard nav, ARIA labels)
- High contrast mode
- 60fps performance
- Focus indicators

---

## 🚀 Sprint Roadmap

| Sprint | Dates | Theme | Key Deliverables |
|--------|-------|-------|------------------|
| **3** | Oct 8-21 | Performance & Accessibility | 60fps, keyboard nav, ARIA, high contrast |
| **4** | Oct 22 - Nov 4 | Enhanced Editing | Chord autocomplete, drag sections, emergency font |
| **5** | Nov 5-18 | Polish & Testing | Animations, loading states, user testing |
| **MVP** | Nov 22 | Launch | Feature complete, bug-free, accessible |

---

## 🎯 Key Decisions & Rationale

### 1. Color System
**Decision:** Performia cyan (#06b6d4) as primary accent
**Rationale:** High contrast, distinguishes from warm amber chords, signals "now"

### 2. Typography Scale
**Decision:** 3.5rem base for lyrics (readable from 6ft)
**Rationale:** Stage visibility is critical, 80% ratio for chords maintains hierarchy

### 3. Audio Playback for Demo
**Decision:** Show placeholder message (no audio for demo song)
**Open Question:** Should we add demo.mp3? (Recommendation: Yes, for better UX)

### 4. Canvas vs DOM for Teleprompter
**Decision:** Optimize DOM first, Canvas as fallback
**Rationale:** Accessibility with DOM is easier, 60fps achievable with optimization

### 5. Emergency Font Adjust
**Decision:** Double-tap gesture on background
**Rationale:** Doesn't conflict with chord click, easy for stage use

---

## 🧩 Component Hierarchy

```
App
├── Header (Settings, Upload, Demo buttons)
├── Main Content
│   ├── TeleprompterView (Performance Mode)
│   │   ├── Audio Controls Bar (NEW)
│   │   │   ├── StemSelector (NEW)
│   │   │   └── AudioPlayer (NEW)
│   │   └── Lyrics Display (Living Chart)
│   ├── BlueprintView (Edit Mode)
│   └── SongMapDemo
├── Footer
└── SettingsPanel (Modal)
    └── LibraryView
```

---

## 📝 Success Metrics

### Quantitative
- **Time to first performance:** <30 seconds ✅
- **Song search:** <5 seconds ✅
- **Settings adjust:** <2 seconds 🔨 (currently 4s)
- **Frame rate:** 60fps 🔨 (currently 50fps)
- **Audio latency:** <50ms ✅

### Qualitative
- **Ease of use:** 4.5+ stars
- **Feature discovery:** 80%+ without tutorial
- **Visual clarity:** 95%+ "easy to read"

---

## 🔗 Related Files

### Backend
- `backend/schemas/song_map.schema.json` - Song Map data structure
- `backend/src/services/` - Audio analysis services

### Frontend
- `frontend/types.ts` - TypeScript type definitions
- `frontend/components/` - React components
- `frontend/index.css` - Global styles and design tokens

---

## 📌 Quick Actions

### For Developers:
1. Read **UI-UX-ALIGNMENT-AND-PLAN.md** for sprint tasks
2. Check **Performia_Capabilities.txt** for feature status
3. Reference **UI-COMPONENT-SPEC.md** when implementing components

### For Designers:
1. Review **FRONTEND_UX_DESIGN_SPEC.md** for workflows
2. Use **UI-COMPONENT-SPEC.md** for component specs
3. Create mockups using design system tokens

### For Product:
1. Review **Performia-PRD.txt** for requirements
2. Track progress in **Performia_Capabilities.txt**
3. Plan sprints using **UI-UX-ALIGNMENT-AND-PLAN.md**

---

## 🎯 North Star Principle

> **"The best interface for performance is no interface at all."**

Every decision must answer:
**"Does this help the musician perform better, or does it distract?"**

If it distracts → Cut it.
If it helps → Polish it until it's invisible.

---

**Version:** 1.0
**Maintained by:** Performia Team
**Next Review:** End of Sprint 3 (Oct 21, 2025)
