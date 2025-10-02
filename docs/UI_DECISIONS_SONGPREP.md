# UI Architecture Decisions for SongPrep Integration

**Date:** October 2, 2025
**Status:** CRITICAL - Decisions Needed Now
**Stakeholder:** Development Team

---

## Executive Summary

**Question:** "If we're using SongPrep for sections, what UI decisions must we make NOW?"

**Answer:** The current UI already supports section-based structure - **we can keep it unchanged**. However, we should add **optional enhancements** now to fully leverage SongPrep's capabilities.

**Critical Decision:** Keep current UI, add **Section Navigation Panel** as optional enhancement in Sprint 3-4.

---

## Current UI Analysis

### What We Have Today

**1. TeleprompterView (Living Chart)**
- ✅ **Already section-aware**: Displays `songMap.sections[].lines[].syllables[]`
- ✅ Scrolls through all sections sequentially
- ✅ Highlights active line/syllable
- ❌ **No visual section boundaries** (verses/choruses blend together)
- ❌ **No section navigation** (can't jump to "Chorus 2")

**2. Full Chart (Editor)**
- ✅ **Already section-aware**: Shows `[ Verse 1 ]`, `[ Chorus ]` headers
- ✅ Editable section names
- ✅ Per-section editing
- ✅ **Perfect for SongPrep integration** - no changes needed

**3. Song Map Adapter**
- ✅ **Already handles sections**: `prepareSectionBoundaries()`, `buildSections()`
- ✅ Groups lyrics into sections
- ✅ Compatible with SongPrep output format
- ✅ **Will work with minimal changes**

### UI Dependencies on Sections

| Component | Current Behavior | SongPrep Impact |
|-----------|------------------|-----------------|
| **TeleprompterView** | Displays sections sequentially | ✅ No breaking changes - better data |
| **Full Chart** | Shows section headers | ✅ Better auto-detection |
| **Song Map Adapter** | Groups lyrics into sections | ✅ Use SongPrep output directly |
| **Settings Panel** | No section-related settings | 🟡 Could add section navigation |
| **Library View** | No section metadata | 🟡 Could show section count |

---

## The Critical Question: Do We Need a Different UI?

### Answer: **NO - Current UI works with SongPrep**

**Why:**
1. **Data structure is compatible** - Both use hierarchical sections
2. **Components already section-aware** - No architectural changes needed
3. **SongPrep improves data quality** - Not data format
4. **Backwards compatible** - Works with or without SongPrep

**But:**
- ⚠️ Current UI doesn't **showcase** SongPrep's capabilities
- ⚠️ Musicians can't **navigate** by section (major UX gap)
- ⚠️ No visual **section boundaries** in Living Chart

---

## Decision Matrix: What to Build Now vs Later

### 🟢 Build NOW (Sprint 3 - Before SongPrep)

These features make sense **regardless** of SongPrep integration:

#### 1. **Visual Section Separators in Living Chart** ⭐ HIGH PRIORITY
**What:** Add visual dividers between sections in TeleprompterView

**Why Now:**
- Improves UX even with manual section tagging
- Simple CSS change (1-2 hours)
- Makes sections visible to performers

**Design:**
```
┌─────────────────────────┐
│  Yesterday, all my...   │
│  troubles seemed...     │
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤  ← Section separator
│  [ CHORUS ]             │  ← Optional header
├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤
│  Why she had to go...   │
└─────────────────────────┘
```

**Implementation:**
```css
/* Add to index.css */
.section-boundary {
    border-top: 2px dashed rgba(6, 182, 212, 0.3);
    margin: 2rem 0;
    padding-top: 2rem;
}

.section-header {
    color: #06b6d4;
    font-size: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
    opacity: 0.6;
}
```

```tsx
// Update TeleprompterView.tsx
{songMap.sections.map((section, sectionIndex) => (
    <div key={sectionIndex}>
        {sectionIndex > 0 && <div className="section-boundary" />}
        <div className="section-header">[ {section.name} ]</div>
        {section.lines.map(line => /* existing code */)}
    </div>
))}
```

**Effort:** 2-3 hours
**Impact:** Medium - Better visual structure

---

#### 2. **Section Metadata in Song Map** ⭐ HIGH PRIORITY
**What:** Add confidence scores and source tracking to sections

**Why Now:**
- Needed regardless of SongPrep (future-proofing)
- Enables A/B testing (manual vs SongPrep sections)
- Shows users detection confidence

**Schema Update:**
```typescript
// frontend/types.ts
export interface Section {
    name: string;
    lines: Line[];
    confidence?: number;    // NEW: 0-1 confidence score
    source?: 'manual' | 'heuristic' | 'songprep';  // NEW: detection method
}
```

**Effort:** 1-2 hours
**Impact:** Low now, High later (enables SongPrep integration)

---

### 🟡 Build MAYBE (Sprint 4 - With SongPrep Experimentation)

Decide based on Sprint 4 SongPrep results:

#### 3. **Section Navigation Panel** 🎯 MEDIUM PRIORITY
**What:** Mini-map showing song structure with jump-to navigation

**Design:**
```
┌─ SONG STRUCTURE ─┐
│ ● Intro          │  ← Click to jump
│ ● Verse 1        │
│ ▶ Chorus  ←──────┼─ Currently playing
│   Verse 2        │
│   Chorus         │
│   Bridge         │
│   Chorus         │
│   Outro          │
└──────────────────┘
```

**Why Maybe:**
- Only valuable if SongPrep provides accurate sections
- Adds UI complexity
- May distract during performance (conflicts with "no interface" philosophy)

**Decision Criteria:**
- ✅ Build if SongPrep achieves <25% error rate in Sprint 4 tests
- ❌ Defer if section detection unreliable

**Implementation:**
```tsx
// New component: SectionNavigator.tsx
const SectionNavigator = ({ sections, currentSection, onJumpTo }) => (
    <div className="section-navigator">
        {sections.map((section, idx) => (
            <button
                key={idx}
                className={idx === currentSection ? 'active' : ''}
                onClick={() => onJumpTo(idx)}
            >
                {section.name}
            </button>
        ))}
    </div>
);
```

**Effort:** 6-8 hours (component + integration)
**Impact:** High if SongPrep works, Low otherwise

---

#### 4. **Section-Based Setlist Management** 🎯 LOW PRIORITY
**What:** Create setlists by dragging sections (e.g., Verse 1 → Chorus → Verse 2)

**Why Maybe:**
- Only useful with accurate section detection
- Phase 2 feature (post-MVP)
- Requires complex UI

**Decision:** Defer to Phase 2 (Q1 2026)

---

### 🔴 Don't Build Now

#### 5. **Completely New UI** ❌ NOT RECOMMENDED
**What:** Redesign TeleprompterView from scratch

**Why Not:**
- Current UI already section-aware
- No architectural incompatibility
- Wastes time before SongPrep validation
- Breaks existing user workflows

**Alternative:** Enhance current UI incrementally

---

## Recommended Action Plan

### Week 1 (This Week - Sprint 3 Start)

**Priority 1: Visual Enhancements**
1. ✅ Add section separators to TeleprompterView (2-3 hours)
2. ✅ Add section headers (optional toggle in settings) (1 hour)
3. ✅ Update Song Map schema with confidence/source fields (1-2 hours)

**Total Effort:** 4-6 hours
**Risk:** Low (enhances existing UI)

### Week 2-3 (Sprint 3 Continued)

**Priority 2: Accessibility & Performance**
- Focus on 60fps optimization (existing roadmap)
- Keyboard shortcuts (existing roadmap)
- Prepare for SongPrep experimentation

### Sprint 4 (Oct 22 - Nov 4)

**Decision Point: Section Navigation**
1. Complete SongPrep experimentation (Week 1)
2. Evaluate section accuracy
3. **If accurate (✅):** Build Section Navigator (Week 2)
4. **If inaccurate (❌):** Defer, keep manual editing

### Sprint 5 (Nov 5-18)

**Integration or Polish**
- **If SongPrep approved:** Full integration + navigator
- **If SongPrep deferred:** Continue with manual sections + polish existing UI

---

## UI Architecture Principles

### 1. **Data-Driven, Not Feature-Driven**
- UI displays whatever section data exists
- Works with manual tags, heuristics, OR SongPrep
- No hard dependency on any detection method

### 2. **Progressive Enhancement**
- Basic: Show lyrics in sections (current)
- Enhanced: Show section boundaries (Sprint 3)
- Advanced: Section navigation (Sprint 4, conditional)
- Future: Setlist builder (Phase 2)

### 3. **Backwards Compatibility**
- All enhancements are optional
- Degrades gracefully without section data
- Existing songs continue to work

### 4. **Performance-First**
- No navigation panel during active performance (distraction)
- Section headers fade out when not active
- Minimal DOM changes (60fps target)

---

## Technical Implementation Details

### Schema Updates Needed

**Backend (song_map.schema.json):**
```json
{
  "sections": {
    "type": "array",
    "items": {
      "properties": {
        "start": { "type": "number" },
        "end": { "type": "number" },
        "label": { "type": "string" },
        "confidence": { "type": "number" },
        "source": { "type": "string", "enum": ["manual", "heuristic", "songprep"] }
      }
    }
  }
}
```

**Frontend (types.ts):**
```typescript
export interface Section {
    name: string;
    lines: Line[];
    confidence?: number;
    source?: 'manual' | 'heuristic' | 'songprep';
}
```

**Adapter (songMapAdapter.ts):**
```typescript
// Add to sectionBuilder.ts
export function buildSections(
    backendMap: BackendSongMap,
    options: AdapterOptions
): Section[] {
    return backendMap.sections.map(sec => ({
        name: sec.label,
        lines: groupLinesInSection(sec, backendMap.lyrics),
        confidence: sec.conf,  // NEW
        source: sec.source || 'heuristic'  // NEW
    }));
}
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SongPrep sections inaccurate | Medium | High | Make navigation optional, keep manual editing |
| UI changes break existing flow | Low | High | A/B test, feature flag |
| Section navigation distracts performers | Medium | Medium | Hide during performance, settings toggle |
| Over-engineering before validation | High | Medium | Build minimal enhancements only |
| Backwards incompatibility | Low | Critical | Ensure graceful degradation |

---

## FAQ

**Q: Can we keep the current UI and still use SongPrep?**
A: **Yes!** Current UI is section-aware. SongPrep just improves section data quality.

**Q: What's the minimum UI change needed for SongPrep?**
A: **Zero.** Adapter already handles sections. SongPrep just provides better detection.

**Q: What's the maximum value-add UI change?**
A: **Section Navigation Panel** - lets users jump to "Chorus 2" instantly.

**Q: Should we build section navigation before testing SongPrep?**
A: **No.** Wait for Sprint 4 experimentation. Only build if SongPrep proves accurate.

**Q: What if SongPrep doesn't work out?**
A: **No problem.** Section separators and schema updates are useful anyway. Navigation can be manual.

**Q: Can we A/B test manual vs SongPrep sections?**
A: **Yes!** With `source` field, we can track which detection method works better.

---

## Decision Record

### Decision 1: Keep Current UI Architecture ✅
- **Rationale:** Current UI already supports sections, no breaking changes needed
- **Date:** October 2, 2025
- **Alternatives Considered:** Complete redesign (rejected - too risky)

### Decision 2: Add Section Separators Now ✅
- **Rationale:** Improves UX regardless of SongPrep, low effort
- **Date:** October 2, 2025
- **Implementation:** Sprint 3 (this week)

### Decision 3: Add Section Navigator Conditionally 🟡
- **Rationale:** Only if SongPrep proves accurate (Sprint 4 validation)
- **Date:** October 2, 2025
- **Decision Point:** End of Sprint 4 (Nov 4, 2025)

### Decision 4: Defer Setlist Builder ⏸️
- **Rationale:** Phase 2 feature, not critical for MVP
- **Date:** October 2, 2025
- **Review Date:** January 2026

---

## Next Steps

### Immediate (This Week)
1. [ ] Implement section separators in TeleprompterView
2. [ ] Add section headers (with settings toggle)
3. [ ] Update TypeScript types with confidence/source
4. [ ] Test with existing demo songs

### Sprint 4 (Oct 22 - Nov 4)
1. [ ] Complete SongPrep experimentation
2. [ ] Measure section detection accuracy
3. [ ] **Decision Point:** Build Section Navigator? (Yes/No)
4. [ ] If Yes: Design and implement navigator
5. [ ] If No: Enhance manual section editing

### Sprint 5 (Nov 5-18)
1. [ ] Integrate SongPrep (if approved)
2. [ ] Polish section-related UI
3. [ ] User testing with sections
4. [ ] Document section-based workflows

---

## Conclusion

**TLDR: Keep current UI, add small enhancements now, big features after validation.**

**Current UI Status:**
- ✅ Compatible with SongPrep
- ✅ Section-aware architecture
- ✅ No breaking changes needed

**Recommended Enhancements:**
- 🟢 **Now:** Section separators + schema updates (4-6 hours)
- 🟡 **Sprint 4:** Section navigator (if SongPrep works)
- 🔴 **Later:** Setlist builder (Phase 2)

**Key Principle:**
> "Build minimal enhancements that add value regardless of SongPrep success."

---

**Prepared by:** Claude (Performia AI Assistant)
**Reviewed by:** Development Team
**Status:** Awaiting approval
**Next Review:** End of Sprint 3 (Oct 21, 2025)
