# Sprint 2 Quick Start Guide

**Sprint:** Schema Integration & Adapter Layer
**Dates:** October 1-7, 2024 (7 days)
**Status:** Day 1 - Ready to Begin

---

## 🎯 What We're Building This Week

**Goal:** Create a TypeScript adapter that transforms backend Song Maps into the format the frontend Living Chart expects.

**Why:** Backend outputs time-series data (`lyrics[]`, `chords[]`, `beats[]`), but frontend needs hierarchical structure (`sections → lines → syllables`).

**Impact:** Once complete, full E2E pipeline works: audio file → backend analysis → adapter → Living Chart display.

---

## 📋 Your Sprint 2 Checklist

### Days 1-2: Understanding & Design ✏️
- [ ] Read backend Song Map schema (`backend/schemas/song_map.schema.json`)
- [ ] Examine real examples (`backend/output/*.song_map.json`)
- [ ] Sketch transformation algorithm (lyrics + sections → hierarchical)
- [ ] Document edge cases (empty sections, missing chords, etc.)

### Days 3-4: Implementation 💻
- [ ] Create `frontend/src/utils/songMapAdapter.ts`
- [ ] Implement transformation with TypeScript
- [ ] Write comprehensive unit tests (>90% coverage)
- [ ] Test with real backend fixtures

### Days 5-6: Integration & Testing 🔗
- [ ] E2E test: backend output → adapter → TeleprompterView
- [ ] Performance validation (<50ms transformation)
- [ ] Update frontend components to use adapter
- [ ] Fix any integration issues

### Day 7: Documentation & Demo 📚
- [ ] Write ADR-001: Song Map transformation strategy
- [ ] Document adapter API with JSDoc
- [ ] Record demo video (audio → display)
- [ ] Sprint review presentation

---

## 🤖 Using Claude Agent SDK

### How to Invoke the Agent

The `frontend-dev` agent is specialized for this work. Invoke it like this:

```
"Act as the frontend-dev agent working on Sprint 2, Story 1: Analyze Backend Song Map Structure.
Review the backend schema at backend/schemas/song_map.schema.json and real examples in
backend/output/*.song_map.json to understand the data structure we need to transform."
```

### Agent Will Handle
- Reading and analyzing backend files
- Designing transformation algorithms
- Writing TypeScript implementation
- Creating comprehensive tests
- Documenting decisions in ADR format

### You Review & Approve
- Transformation algorithm design
- Test coverage adequacy
- Performance benchmarks
- Final implementation

---

## 📊 How to Track Progress

### Daily Status Updates

Check `.claude/sprint_status.md` every day. The agent updates this file with:
- What was completed yesterday
- What's planned for today
- Any blockers encountered
- Time spent vs estimates

### Story Progress

Current sprint has **12 stories**. Track completion:
- Stories 1-4: Analysis & Design (16h total)
- Stories 5-6: Implementation (16h total)
- Stories 7-9: Integration (16h total)
- Stories 10-12: Documentation (8h total)

### Success Metrics

Watch these numbers in sprint_status.md:
- **Adapter Accuracy:** Must be 100%
- **Transformation Speed:** Must be <50ms
- **Test Coverage:** Must be >90%
- **E2E Success:** Must be 100%

---

## 🔑 Key Files Reference

### Backend (Read-Only)
- `backend/schemas/song_map.schema.json` - Backend schema definition
- `backend/output/integration_test.song_map.json` - Real example
- `backend/output/b72e82dc.song_map.json` - Another example

### Frontend (You'll Create/Modify)
- `frontend/types.ts` - Add `BackendSongMap` interface
- `frontend/src/utils/songMapAdapter.ts` - **NEW** - The adapter
- `frontend/src/utils/songMapAdapter.test.ts` - **NEW** - Tests
- `frontend/components/TeleprompterView.tsx` - Use adapter

### Documentation (You'll Create)
- `docs/adr/001-song-map-adapter.md` - **NEW** - Architecture decision
- `.claude/sprint_status.md` - Daily updates

---

## 💡 Understanding the Transformation

### Backend Format (What We Get)
```json
{
  "id": "song_123",
  "duration_sec": 180,
  "sections": [
    {"start": 0, "end": 30, "label": "Verse 1"},
    {"start": 30, "end": 60, "label": "Chorus"}
  ],
  "lyrics": [
    {"start": 0.5, "end": 1.2, "text": "Hello"},
    {"start": 1.3, "end": 1.8, "text": "world"}
  ],
  "chords": [
    {"start": 0.0, "end": 2.0, "label": "C"},
    {"start": 2.0, "end": 4.0, "label": "G"}
  ]
}
```

### Frontend Format (What We Need)
```typescript
{
  title: "Song Title",
  artist: "Artist Name",
  key: "C",
  bpm: 120,
  sections: [
    {
      name: "Verse 1",
      lines: [
        {
          syllables: [
            { text: "Hello", startTime: 0.5, duration: 0.7, chord: "C" },
            { text: "world", startTime: 1.3, duration: 0.5, chord: "C" }
          ]
        }
      ]
    }
  ]
}
```

### Transformation Algorithm (Conceptual)
1. **Group lyrics by sections:** Use section timing boundaries
2. **Split into lines:** Detect line breaks or timing gaps >1s
3. **Create syllables:** Each lyric becomes a syllable
4. **Map chords:** Find chord active during syllable time
5. **Extract metadata:** Pull title, artist, BPM from backend

---

## ✅ Definition of Done

Sprint 2 is complete when:

1. ✅ Adapter code exists in `frontend/src/utils/songMapAdapter.ts`
2. ✅ Unit tests pass with >90% coverage
3. ✅ E2E test passes (backend JSON → adapter → display)
4. ✅ Transformation completes in <50ms for typical song
5. ✅ Zero schema-related errors in console
6. ✅ ADR-001 document exists and explains decision
7. ✅ Demo video shows end-to-end flow
8. ✅ Sprint review presentation prepared

---

## 🚀 Getting Started RIGHT NOW

### Option 1: Invoke Agent for Story 1
```
"Act as the frontend-dev agent working on Sprint 2, Story 1:
Analyze Backend Song Map Structure.

Read these files:
- backend/schemas/song_map.schema.json
- backend/output/integration_test.song_map.json
- backend/output/b72e82dc.song_map.json

Create a detailed analysis document explaining:
1. Backend schema structure
2. Example data from real Song Maps
3. Key fields we need to transform
4. Initial thoughts on transformation approach

Save the analysis as docs/sprint2_analysis.md"
```

### Option 2: Manual First Step
1. Open `backend/schemas/song_map.schema.json`
2. Open `backend/output/integration_test.song_map.json`
3. Compare backend structure to frontend types in `frontend/types.ts`
4. Sketch transformation algorithm on paper

### Option 3: Review Roadmap First
1. Read `SPRINT_ROADMAP.md` (full details of all 5 sprints)
2. Read `.claude/sprint_status.md` (daily tracking template)
3. Review `RESTORATION_REPORT.md` (what led us here)

---

## 📞 Need Help?

### Stuck on Transformation Logic?
- Review real Song Map examples in `backend/output/`
- Check how TeleprompterView currently uses sections/lines/syllables
- Ask: "What's the simplest transformation that could work?"

### Tests Failing?
- Check test coverage: `npm test -- --coverage`
- Review fixtures: Are they realistic?
- Edge cases: Empty sections? Missing chords? Single syllable?

### Performance Issues?
- Profile with Chrome DevTools
- Check: Are you creating too many objects?
- Optimize: Memoize expensive transformations

---

## 🎯 Success Looks Like

**End of Week:**
- ✅ Upload audio file in frontend
- ✅ Backend processes it → Song Map JSON
- ✅ Adapter transforms → frontend format
- ✅ Living Chart displays perfectly
- ✅ Chords overlay at correct times
- ✅ Syllables highlight in real-time
- ✅ Zero errors in console
- ✅ Performance <50ms

**You'll Know You're Done When:**
The entire pipeline works seamlessly and you can upload ANY audio file and see it in the Living Chart within 30 seconds.

---

## 📈 What Comes After Sprint 2

**Sprint 3 (Oct 8-21):** Performance optimization
- Hit <10ms audio latency target
- Achieve stable 60fps Living Chart
- Add accessibility improvements

**Sprint 4 (Oct 22 - Nov 4):** Production deployment
- CI/CD automation
- Monitoring & observability
- Full documentation

**Sprint 5 (Nov 5-18):** Advanced features
- Voice control integration
- AI accompaniment preview
- Enhanced Blueprint editor

---

**Ready? Let's build the adapter that makes Performia's full vision possible! 🚀**

---

*Quick Start Guide - Sprint 2*
*Created: October 1, 2024*
*Next Update: End of Sprint (Oct 7)*
