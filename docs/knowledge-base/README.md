# Performia Knowledge Base

**Purpose:** RAG-enabled documentation repository for enhanced AI agent precision during development.

## Architecture

```
Documentation Sources (PDFs/HTML)
  ↓
Docling Processing (parsing + structure extraction)
  ↓
Markdown + JSON (human-readable intermediate)
  ↓
Text Chunking (1000 chars, 200 overlap)
  ↓
Embeddings (sentence-transformers/all-MiniLM-L6-v2)
  ↓
ChromaDB Vector Store (local, persistent)
  ↓
RAG Retrieval (similarity search)
  ↓
Claude Context Enhancement
```

## Directory Structure

```
docs/knowledge-base/
├── supercollider/       # SuperCollider audio synthesis documentation
├── juce/                # JUCE C++ framework documentation
├── audio-dsp/           # Audio DSP theory and algorithms
├── music-theory/        # Music theory, harmony, rhythm
├── research/            # Academic papers (SongPrep, Whisper, etc.)
├── processed/           # Docling-processed markdown output
│   ├── supercollider/
│   ├── juce/
│   └── ...
└── chromadb/            # Vector database (auto-generated)
```

## Quick Start

### 1. Install Dependencies

Already installed in virtual environment:
```bash
source tools/knowledge-base/venv/bin/activate
# Dependencies: docling, chromadb, langchain
```

### 2. Add Documentation

Place PDFs, HTML, or other documents in category directories:
```bash
# Example: SuperCollider documentation
curl -o docs/knowledge-base/supercollider/sc-book.pdf \
  https://example.com/supercollider-book.pdf
```

### 3. Process Documents

```bash
# Process single file
python tools/knowledge-base/process_docs.py \
  --input docs/knowledge-base/supercollider/sc-book.pdf \
  --category supercollider

# Process entire directory
python tools/knowledge-base/process_docs.py \
  --input docs/knowledge-base/juce/ \
  --category juce
```

### 4. Query Knowledge Base

```bash
# Example query
python tools/knowledge-base/process_docs.py \
  --query "How do I implement real-time audio processing in JUCE?" \
  --category juce

# Returns top 5 relevant chunks with sources
```

## Categories

### SuperCollider
- Audio synthesis patterns
- Live coding techniques
- Server architecture
- UGen documentation

### JUCE
- AudioProcessor implementation
- Real-time audio threading
- Plugin development
- UI components

### Audio DSP
- FFT algorithms
- Digital filters
- Beat detection
- Pitch tracking
- Spectral analysis

### Music Theory
- Chord progressions
- Key detection
- Harmonic analysis
- Rhythm patterns

### Research Papers
- SongPrep (song structure parsing)
- Whisper (speech recognition)
- Demucs (source separation)
- CREMA (chord recognition)
- Relevant music AI papers

## Integration with Claude

### Manual Context Injection
```bash
# Get relevant context for task
python tools/knowledge-base/process_docs.py \
  --query "JUCE AudioProcessor threading model" \
  > context.txt

# Paste into Claude prompt
```

### Future: Automated RAG
- MCP (Model Context Protocol) integration
- Automatic context retrieval based on conversation
- Dynamic knowledge base updates
- Agent-triggered queries

## Adding New Documentation

### Supported Formats
- PDF (✅ Best support via Docling)
- HTML/Web pages
- DOCX/Word documents
- Markdown (direct passthrough)
- Plain text

### Best Practices
1. **Use descriptive filenames**: `juce_audio_processor_threading.pdf`
2. **Organize by category**: Correct category improves retrieval
3. **Include metadata**: Publication date, author, version
4. **Quality over quantity**: Curate authoritative sources
5. **Regular updates**: Re-process when docs change

## Performance

### Processing Speed
- PDF (100 pages): ~30-60 seconds
- HTML page: ~5-10 seconds
- Entire directory: Parallel processing planned

### Storage
- Raw PDFs: ~100MB (example)
- Processed markdown: ~10MB (10:1 compression)
- ChromaDB vectors: ~50MB (depends on chunk count)

### Query Speed
- Similarity search: <100ms for top-5 results
- Local embeddings: No API latency

## Maintenance

### Update Documentation
```bash
# Re-process updated files (overwrites existing)
python tools/knowledge-base/process_docs.py \
  --input docs/knowledge-base/juce/updated_guide.pdf \
  --category juce
```

### Backup Vector Database
```bash
# ChromaDB is file-based, just copy directory
tar -czf chromadb_backup.tar.gz docs/knowledge-base/chromadb/
```

### Clear Database
```bash
# Delete and rebuild from scratch
rm -rf docs/knowledge-base/chromadb/
# Then re-process all docs
```

## Roadmap

### Phase 1: Manual Usage (Current)
- ✅ Docling installation
- ✅ ChromaDB setup
- ✅ Processing script
- 🔄 Initial documentation downloads
- ⏳ Testing and validation

### Phase 2: Integration (Sprint 4-5)
- MCP server for automatic context retrieval
- Agent-triggered queries during development
- Context window optimization
- Performance benchmarking

### Phase 3: Automation (Post-MVP)
- Web scraping for latest docs
- Automatic updates (e.g., JUCE release notes)
- Multi-language support
- Custom fine-tuned embeddings

## Examples

### Example 1: JUCE Audio Processing
```bash
# Query
python tools/knowledge-base/process_docs.py \
  --query "How do I implement processBlock in JUCE AudioProcessor?"

# Output
Result 1 (score: 0.8234)
Category: juce
Source: docs/knowledge-base/juce/audio_processor_guide.pdf
Content:
The processBlock() method is called by the host to process audio...
[Full context returned]
```

### Example 2: SuperCollider Synthesis
```bash
# Query
python tools/knowledge-base/process_docs.py \
  --query "SuperCollider SinOsc frequency modulation"

# Output
Result 1 (score: 0.9012)
Category: supercollider
Source: docs/knowledge-base/supercollider/sc-book.pdf
Content:
SinOsc.ar(freq: 440, phase: 0, mul: 1, add: 0)...
[Relevant UGen documentation]
```

## Troubleshooting

### Issue: "No module named 'docling'"
**Solution:** Activate virtual environment first
```bash
source tools/knowledge-base/venv/bin/activate
```

### Issue: Slow processing
**Solution:** Use GPU acceleration (PyTorch with CUDA)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: Out of memory
**Solution:** Reduce chunk size in `process_docs.py`
```python
chunk_size=500,  # Reduce from 1000
```

## License & Attribution

Documentation sources retain their original licenses. This knowledge base system is for internal Performia development only.

**Attribution Requirements:**
- SuperCollider: GPL v3
- JUCE: GPL v3 / Commercial (check license)
- Research papers: Cite authors per paper licenses

---

**Last Updated:** October 2, 2025
**Maintainer:** Performia Development Team
**Status:** Phase 1 - Initial Setup
