# Knowledge Management & Learning System Plan

**Created**: October 4, 2025
**Status**: Pending Implementation
**Purpose**: Prevent recurring AI mistakes through proper knowledge management

---

## Problem Statement

Current memory.md approach is insufficient for preventing repeated errors:

### Recurring Mistakes Observed
1. **Directory confusion**: Searched `~/.config/claude/commands/` instead of correct `~/.claude/commands/`
2. **Incomplete execution**: Created cleanup script but didn't run it during `/end-session`
3. **Pattern**: Same mistakes repeat across sessions despite documentation

### Root Cause
- Memory is linear and hard to search
- No authoritative reference for Claude Code internals
- Technical domain knowledge (audio/music) scattered across files
- No RAG system for contextual retrieval

---

## Proposed Solution: Docling-Powered Knowledge Base

### What is Docling?
- Document ingestion and RAG system
- Enables AI agents to query knowledge base
- Provides authoritative answers from ingested docs
- Already explored in VIZTRTR project

### What to Ingest

#### 1. Claude Code Official Documentation
**Priority: CRITICAL**
- Correct file paths (`~/.claude/` vs `~/.config/claude/`)
- Custom slash command system
- Hook system and event triggers
- Session management workflows
- Project structure conventions

**Source**: Official Claude Code docs (need to locate)

#### 2. Audio/Music Domain Knowledge
**Priority: HIGH**
- **Librosa**: Best practices, optimal parameters, common pitfalls
- **Essentia**: When to use vs Librosa, specific use cases
- **Music21**: Music theory validation, symbolic music processing
- **Madmom**: Advanced beat tracking techniques
- **Audio DSP**: STFT, CQT, HPSS, spectral analysis fundamentals

**Sources**:
- Official library documentation
- Tutorial repositories (e.g., Marktechpost/AI-Tutorial-Codes-Included)
- Research papers on MIR (Music Information Retrieval)
- Our existing `.claude/MUSIC_AUDIO_KNOWLEDGE.md`

#### 3. Project-Specific Patterns
**Priority: MEDIUM**
- Performia architecture and conventions
- Song Map schema and transformations
- Testing patterns and best practices
- Common code patterns and anti-patterns

**Sources**:
- `.claude/CLAUDE.md`
- `.claude/memory.md`
- Code documentation
- Commit history patterns

#### 4. Common Mistakes Database
**Priority: HIGH**
- `~/.claude/COMMON_MISTAKES.md`
- Session summaries with "lessons learned"
- Debugging patterns and solutions
- Configuration gotchas

---

## Implementation Plan

### Phase 1: Setup Docling (Week 1)
1. Install/configure docling in Performia project
2. Test basic ingestion with sample documents
3. Verify RAG queries work correctly
4. Document setup process

### Phase 2: Ingest Core Knowledge (Week 1-2)
1. **Day 1**: Locate and ingest Claude Code official docs
2. **Day 2-3**: Ingest Librosa/audio DSP documentation
3. **Day 4**: Ingest project-specific docs (CLAUDE.md, memory.md)
4. **Day 5**: Ingest common mistakes and patterns

### Phase 3: Integration & Testing (Week 2)
1. Update AI agent prompts to query docling first
2. Test with known failure cases (directory paths, etc.)
3. Verify correct answers from knowledge base
4. Document query patterns

### Phase 4: Maintenance (Ongoing)
1. Add new learnings after each session
2. Update knowledge base with resolved issues
3. Refine ingestion based on query patterns
4. Expand to other libraries/tools as needed

---

## Knowledge Base Structure

```
knowledge-base/
├── claude-code/           # Official Claude Code docs
│   ├── paths.md          # File system structure
│   ├── commands.md       # Slash commands
│   └── hooks.md          # Event hooks
├── audio-dsp/            # Audio domain knowledge
│   ├── librosa/          # Librosa docs and tutorials
│   ├── essentia/         # Essentia docs
│   ├── music21/          # Music21 docs
│   └── fundamentals/     # DSP basics
├── project/              # Performia-specific
│   ├── architecture.md   # System design
│   ├── songmap.md        # Data format
│   └── patterns.md       # Code patterns
└── mistakes/             # Learning from errors
    ├── common-errors.md  # Recurring issues
    └── solutions.md      # How to fix them
```

---

## Success Criteria

### Immediate (Phase 1-2)
- ✅ Docling installed and working
- ✅ Claude Code paths documented and queryable
- ✅ Audio domain knowledge accessible
- ✅ No directory confusion in future sessions

### Medium-term (Phase 3-4)
- ✅ All AI agents use docling for technical questions
- ✅ Zero repeated mistakes from previous sessions
- ✅ Audio pipeline code uses optimal parameters
- ✅ Knowledge base grows with each session

### Long-term
- ✅ Self-improving system (learns from mistakes)
- ✅ Shareable across projects
- ✅ Exportable for team collaboration
- ✅ Foundation for voice-controlled development

---

## Open Questions

1. **Where are official Claude Code docs?**
   - Need to locate and verify authoritative source
   - May need to extract from CLI help or online resources

2. **Docling configuration?**
   - How to structure ingestion?
   - What format works best (markdown, JSON, etc.)?
   - How to handle updates?

3. **Integration approach?**
   - Should agents query docling automatically?
   - Explicit query step in workflows?
   - Fallback strategy if docling unavailable?

4. **External resources?**
   - Clone Marktechpost repo for tutorials?
   - Link to online docs vs local copies?
   - Copyright/licensing considerations?

---

## Next Steps (For Review)

1. **User verifies `/start-session` and `/end-session` working properly**
2. Review this plan and provide feedback
3. Prioritize what to ingest first
4. Decide on docling setup approach
5. Begin Phase 1 implementation

---

## References

- `~/.claude/COMMON_MISTAKES.md` - Documented errors
- `.claude/MUSIC_AUDIO_KNOWLEDGE.md` - Audio domain expertise
- `.claude/memory.md` - Project memory and status
- https://github.com/Marktechpost/AI-Tutorial-Codes-Included - Learning resources
- VIZTRTR project - Docling exploration (if being used)

---

*This is a living document - update as implementation progresses*
