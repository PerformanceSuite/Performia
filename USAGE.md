# Usage Guide

Complete guide to using Performia for music performance, song management, and audio analysis.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Adding Your First Song](#adding-your-first-song)
- [Living Chart Interface](#living-chart-interface)
- [Blueprint View](#blueprint-view)
- [Library Management](#library-management)
- [Settings and Customization](#settings-and-customization)
- [Performance Tips](#performance-tips)
- [Advanced Features](#advanced-features)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [FAQ](#faq)

---

## Getting Started

### Launching Performia

1. **Start Backend Server**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Windows: venv\Scripts\activate

   # Start backend
   python backend/src/services/api/main.py
   ```

2. **Start Frontend**:
   ```bash
   # In a new terminal
   cd frontend
   npm run dev
   ```

3. **Open Browser**:
   Navigate to `http://localhost:5001`

### First Launch

On first launch, Performia loads a demo song ("Yesterday" by The Beatles) to help you explore features.

**Demo Song Features**:
- Pre-analyzed Song Map with timing
- Syllable-level highlighting
- Chord progressions
- Section structure

Try these actions with the demo:
1. Click **Play** to see real-time syllable highlighting
2. Click **Settings** (gear icon) to adjust font size
3. Try **Fullscreen** mode for performance view
4. Explore **Blueprint View** to see song structure

---

## Adding Your First Song

### Supported Audio Formats

- **MP3** (.mp3)
- **WAV** (.wav)
- **M4A** (.m4a)
- **FLAC** (.flac)
- **OGG** (.ogg)

### Upload Process

#### Method 1: Drag and Drop

1. Locate your audio file in file manager
2. Drag the file onto the Performia window
3. Drop when the upload area highlights
4. Wait for processing to complete (~30 seconds)

#### Method 2: File Browser

1. Click **Upload Song** button
2. Browse to your audio file
3. Click **Open**
4. Wait for processing to complete

### Processing Pipeline

When you upload a song, Performia runs through several analysis stages:

```
Upload → ASR → Beat Detection → Chord Analysis → Melody Extraction → Song Map Generation
  ⏱️      5s        3s              8s               7s                  5s
```

**Total time**: ~30 seconds for a 3-minute song

### Processing Status

Monitor processing progress:

1. **Uploading** - File upload in progress
2. **Queued** - Waiting for analysis
3. **Processing** - Running audio analysis pipeline
   - Progress bar shows completion percentage
4. **Complete** - Song Map ready, song added to library
5. **Error** - Something went wrong (check error message)

### What Performia Extracts

During processing, Performia analyzes:

- **Lyrics** - Transcribed using OpenAI Whisper
- **Timing** - Syllable-level start times and durations
- **Chords** - Chord progressions throughout the song
- **Key** - Overall key and key changes
- **Tempo** - BPM and tempo changes
- **Structure** - Sections (verse, chorus, bridge, etc.)
- **Melody** - Pitch contours and melodic patterns
- **Stems** (optional) - Separated vocals, bass, drums, other

### After Processing

Once complete, your song:
- Appears in the Library
- Opens in Living Chart view
- Is ready for performance
- Can be edited in Blueprint View

---

## Living Chart Interface

The Living Chart is Performia's real-time performance view.

### Layout

```
┌──────────────────────────────────────────────┐
│  [Settings] [Library] [Fullscreen] [Play]    │ ← Controls
├──────────────────────────────────────────────┤
│                                              │
│  Verse 1                                     │ ← Section Label
│                                              │
│  [C]                     [Am]                │ ← Chord Markers
│  Yesterday, all my troubles seemed so        │
│  far away                                    │ ← Lyrics
│                                              │
│  [F]                     [G7]                │
│  Now it looks as though they're here to stay │
│                                              │
│  Chorus                                      │
│  ...                                         │
│                                              │
└──────────────────────────────────────────────┘
```

### Real-Time Following

When you play audio (or perform live):

1. **Current syllable** highlights in color
2. **Next syllable** shows subtle preview
3. **Auto-scroll** keeps current line centered
4. **Chord changes** highlight at the right moment

### Controls

**Top Bar**:
- **Settings** (⚙️) - Font size, transpose, colors
- **Library** (📚) - Return to song library
- **Blueprint** (📄) - Switch to edit mode
- **Fullscreen** (⛶) - Hide controls for performance
- **Play/Pause** (▶️/⏸️) - Control playback

**During Performance**:
- All controls auto-hide in fullscreen
- Tap/click screen to show controls temporarily
- Controls fade after 3 seconds of inactivity

### Display Modes

**1. Practice Mode** (default)
- Shows all sections
- Displays chord symbols
- Section labels visible
- Scroll freely

**2. Performance Mode** (fullscreen)
- Maximized text size
- Auto-scroll only
- Minimal UI
- Focus on current section

**3. Teleprompter Mode**
- Continuous scrolling
- Large fonts (readable from 6ft)
- No distractions
- Professional presentation

### Customization

Adjust display in **Settings**:

- **Font Size**: 12px - 120px
- **Font Family**: Sans-serif, Serif, Monospace
- **Transpose**: -12 to +12 semitones
- **Color Theme**: Light, Dark, High Contrast
- **Line Spacing**: Compact, Normal, Relaxed
- **Syllable Highlighting**: Color and intensity

---

## Blueprint View

Blueprint View is for editing and reviewing song structure.

### Switching to Blueprint

1. Click **Blueprint** button (📄) in top bar
2. Or press `B` keyboard shortcut

### Layout

```
┌──────────────────────────────────────────────┐
│  Song: Yesterday         Artist: The Beatles │ ← Header
├──────────────────────────────────────────────┤
│  [Add Section] [Import Lyrics] [Export]      │ ← Actions
├──────────────────────────────────────────────┤
│                                              │
│  ┌─ Verse 1 ─────────────────────────────┐  │
│  │ [C]                     [Am]           │  │
│  │ Yesterday, all my troubles seemed so   │  │
│  │ far away                               │  │
│  │                                        │  │
│  │ [Edit] [Delete] [Move Up] [Move Down]  │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ Chorus ──────────────────────────────┐  │
│  │ ...                                    │  │
│  └────────────────────────────────────────┘  │
│                                              │
└──────────────────────────────────────────────┘
```

### Editing Song Structure

**Add Section**:
1. Click **Add Section**
2. Choose section type (Verse, Chorus, Bridge, etc.)
3. Enter lyrics
4. Add chord markers

**Edit Section**:
1. Click **Edit** on section
2. Modify lyrics or chords
3. Click **Save**

**Reorder Sections**:
- Click **Move Up** / **Move Down**
- Or drag section handles

**Delete Section**:
1. Click **Delete**
2. Confirm deletion

### Editing Chords

**Add Chord**:
1. Click between words where chord changes
2. Type chord name (e.g., "C", "Am7", "Fmaj7")
3. Press Enter

**Edit Chord**:
1. Click on chord marker
2. Type new chord
3. Press Enter

**Delete Chord**:
1. Click on chord marker
2. Press Backspace/Delete

### Editing Lyrics

**Edit Text**:
1. Click on lyric line
2. Edit text inline
3. Press Enter to save

**Import Lyrics**:
1. Click **Import Lyrics**
2. Paste lyrics from clipboard
3. Performia auto-structures into lines
4. Review and adjust

**Export Lyrics**:
1. Click **Export**
2. Choose format (Plain Text, ChordPro, PDF)
3. Download file

### Timing Adjustments

**Adjust Syllable Timing**:
1. Enter **Timing Mode** (advanced)
2. Click on syllable
3. Drag to adjust start time
4. Adjust duration with handles

**Synchronize Section**:
1. Click **Sync** on section
2. Play audio
3. Tap space bar at each syllable
4. Performia records timing

---

## Library Management

Manage your song collection in the Library view.

### Library Layout

```
┌──────────────────────────────────────────────┐
│  🔍 Search songs...           [Upload] [+]   │ ← Search & Actions
├──────────────────────────────────────────────┤
│  Sort: [Recent] ▼  Filter: [All] ▼           │ ← Sorting & Filters
├──────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐    │
│  │ 🎵 Yesterday                         │    │
│  │    The Beatles • 2:05 • Key: F      │    │
│  │    Tags: ballad, classic rock       │    │
│  │    [Open] [Edit] [Delete]           │    │
│  └──────────────────────────────────────┘    │
│  ┌──────────────────────────────────────┐    │
│  │ 🎵 Let It Be                         │    │
│  │    The Beatles • 3:50 • Key: C      │    │
│  │    [Open] [Edit] [Delete]           │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

### Search

**Search by**:
- Song title
- Artist name
- Album
- Tags
- Lyrics content

**Search tips**:
- Use quotes for exact phrases: `"hey jude"`
- Multiple words search all fields
- Case-insensitive

### Sort and Filter

**Sort Options**:
- **Recent** - Recently added or modified
- **Title** - Alphabetically by song title
- **Artist** - Alphabetically by artist
- **Duration** - Song length
- **Key** - Musical key

**Filter Options**:
- **All Songs**
- **Favorites** - Starred songs
- **Recent** - Added in last 7 days
- **By Tag** - Filter by custom tags
- **By Key** - Filter by musical key

### Song Actions

**Open**:
- Opens song in Living Chart view
- Ready for performance

**Edit**:
- Opens song in Blueprint View
- Edit structure, chords, lyrics

**Delete**:
- Removes song from library
- Deletes Song Map and audio files
- Requires confirmation

**Favorite**:
- Click star icon to favorite
- Access quickly from Favorites filter

### Tagging Songs

Add custom tags for organization:

1. Click **Edit** on song
2. Click **Add Tag**
3. Type tag name (e.g., "wedding", "upbeat", "slow")
4. Press Enter
5. Tags appear in song card and are searchable

**Suggested Tag Categories**:
- **Mood**: upbeat, sad, energetic, calm
- **Genre**: rock, jazz, pop, country
- **Occasion**: wedding, party, church, karaoke
- **Difficulty**: easy, medium, hard
- **Status**: learning, ready, favorite

---

## Settings and Customization

Access Settings via gear icon (⚙️) in top bar.

### Display Settings

**Font Size**:
- Range: 12px - 120px
- Use slider or type value
- Default: 24px
- Performance mode: 48px+

**Font Family**:
- Sans-serif (clean, modern)
- Serif (traditional, classic)
- Monospace (technical, aligned)

**Line Spacing**:
- Compact (more lines visible)
- Normal (balanced)
- Relaxed (easier reading)

### Musical Settings

**Transpose**:
- Range: -12 to +12 semitones
- Adjusts all chords automatically
- Useful for different vocal ranges
- Example: Transpose +2 moves C → D

**Capo Position**:
- Virtual capo for guitar
- Shows capo chords vs actual chords
- Example: Capo 2, playing C = actual D

**Key Detection**:
- Auto-detected during analysis
- Can override manually
- Affects chord suggestions

### Performance Settings

**Auto-scroll**:
- Enable/disable auto-scrolling
- Adjust scroll speed
- Lead time (scroll ahead by X seconds)

**Highlighting**:
- Current syllable color
- Next syllable preview
- Chord highlight color
- Intensity (subtle to bold)

**Metronome** (coming soon):
- Enable click track
- Adjust volume
- Visual metronome

### System Settings

**Audio Input** (coming soon):
- Select microphone
- Input gain
- Monitoring

**MIDI** (coming soon):
- MIDI controller mapping
- Foot pedal support
- Page turn controls

---

## Performance Tips

### Before Your Performance

**1. Prepare Songs**:
- Upload and analyze all songs beforehand
- Review each Song Map for accuracy
- Make any needed edits in Blueprint View
- Test timing with playback

**2. Optimize Display**:
- Set font size readable from your distance
- Choose high-contrast theme
- Test fullscreen mode
- Adjust lead time for auto-scroll

**3. Create Setlist** (coming soon):
- Order songs in performance sequence
- Add notes/cues between songs
- Set transition times

**4. Test Equipment**:
- Check monitor visibility
- Test with performance lighting
- Verify audio routing
- Test backup laptop/tablet

### During Performance

**1. Use Fullscreen Mode**:
- Minimizes distractions
- Maximizes text size
- Auto-hides controls

**2. Trust the System**:
- Don't look ahead excessively
- Follow the highlighting
- System accounts for tempo variations

**3. Recovery from Mistakes**:
- If you skip a line, system catches up
- Tap/click to show controls
- Use scroll to navigate
- System re-syncs automatically

**4. Manual Control**:
- Space bar: Play/Pause
- Arrow keys: Scroll
- Escape: Exit fullscreen
- Click/tap: Show controls

### After Performance

**1. Review**:
- Check any timing issues
- Note sections that need editing
- Save performance notes

**2. Improve**:
- Adjust timing in Blueprint View
- Fine-tune chord positions
- Update tags or setlist order

---

## Advanced Features

### Voice Control (Coming Soon)

Control Performia with voice commands:

- "Next song"
- "Previous section"
- "Transpose up 2"
- "Repeat chorus"

### Live Performance Tracking (In Development)

Performia follows your live performance:

1. Connect microphone
2. Enable live tracking
3. Sing/play
4. Performia follows in real-time

### Stem Separation

Access separated audio tracks:

1. Open song in Living Chart
2. Click **Stems** button
3. Toggle individual stems:
   - Vocals
   - Bass
   - Drums
   - Other instruments

**Use Cases**:
- Practice with backing tracks
- Learn individual parts
- Karaoke (vocals removed)

### AI Accompaniment (Roadmap)

Future feature: AI-generated accompaniment that follows your performance.

---

## Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| `Space` | Play/Pause |
| `F` | Toggle Fullscreen |
| `S` | Open Settings |
| `L` | Go to Library |
| `B` | Blueprint View |
| `Esc` | Exit Fullscreen/Close Modal |

### Living Chart

| Shortcut | Action |
|----------|--------|
| `↑` `↓` | Scroll up/down |
| `Page Up` `Page Down` | Scroll page |
| `Home` | Go to song start |
| `End` | Go to song end |
| `+` `-` | Increase/Decrease font size |

### Blueprint View

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + S` | Save changes |
| `Cmd/Ctrl + Z` | Undo |
| `Cmd/Ctrl + Y` | Redo |
| `Cmd/Ctrl + F` | Find in lyrics |
| `Cmd/Ctrl + N` | New section |
| `Cmd/Ctrl + E` | Edit section |

### Library

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + F` | Focus search |
| `Enter` | Open selected song |
| `Delete` | Delete selected song |
| `Cmd/Ctrl + U` | Upload new song |
| `↑` `↓` | Navigate songs |

---

## FAQ

### General Questions

**Q: How accurate is the automatic transcription?**

A: Whisper achieves 90-95% accuracy on clear vocals. Accuracy depends on:
- Audio quality (studio recordings work best)
- Pronunciation clarity
- Background noise levels
- Language (English works best)

Edit any mistakes in Blueprint View.

**Q: Can I use Performia offline?**

A: Partially. You need internet for:
- Initial song upload and analysis (uses OpenAI/Anthropic APIs)
- Knowledge base features

Once analyzed, songs work offline.

**Q: What audio quality should I use?**

A: Recommendations:
- **Minimum**: 128kbps MP3
- **Recommended**: 320kbps MP3 or lossless (FLAC/WAV)
- Higher quality = better analysis accuracy

**Q: Can I import existing chord sheets?**

A: Yes, via Blueprint View:
1. Click Import Lyrics
2. Paste ChordPro format or plain text
3. Performia parses chords and lyrics
4. Review and adjust

**Q: How many songs can I store?**

A: Limited by storage space:
- Each song: ~50MB (audio + analysis data)
- 1TB storage = ~20,000 songs
- Use SQLite (default) or PostgreSQL

### Technical Questions

**Q: Why does processing take 30 seconds?**

A: The audio pipeline runs multiple models:
- Whisper (ASR): ~5s
- Demucs (stems): ~10s (optional)
- Beat detection: ~3s
- Chord analysis: ~8s
- Melody extraction: ~7s

Future: GPU acceleration will reduce this to ~10s.

**Q: Can I use my own API keys?**

A: Yes, required. Add to `.env`:
```bash
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

**Q: Does Performia work with MIDI controllers?**

A: Coming soon. Planned support for:
- Foot pedals (page turn)
- Expression pedals (tempo control)
- MIDI keyboards (pitch detection)

**Q: Can multiple people use the same instance?**

A: Yes, but:
- SQLite (default) supports light concurrent use
- Use PostgreSQL for heavy multi-user loads
- Each user can have separate library (coming soon)

### Troubleshooting

**Q: Song processing failed, what do I do?**

A: Check:
1. Audio file format is supported
2. File isn't corrupted (try playing in media player)
3. File size isn't too large (max 100MB recommended)
4. Backend logs for specific error
5. API keys are valid

**Q: Syllable timing is off, how to fix?**

A: Two options:
1. **Re-analyze**: Delete and re-upload with better quality audio
2. **Manual adjustment**: Use Blueprint View timing mode to adjust

**Q: Chords are wrong, can I fix them?**

A: Yes, in Blueprint View:
1. Click on chord marker
2. Edit chord name
3. Save changes

Chord detection is ~80% accurate. Always review.

**Q: Can I undo changes?**

A: Yes:
- Blueprint View has full undo/redo
- Changes saved automatically
- Can revert to last saved version

---

## Next Steps

Now that you know how to use Performia:

1. **Upload Your Songs**: Build your library
2. **Customize Settings**: Optimize for your setup
3. **Practice**: Try performance mode
4. **Explore Advanced Features**: Stems, timing adjustments
5. **Contribute**: Report bugs, suggest features

For technical details, see:
- [Architecture](./ARCHITECTURE.md)
- [API Reference](./API.md)
- [Contributing Guide](./CONTRIBUTING.md)

---

*For questions or issues, see the [FAQ](#faq) or open an issue on [GitHub](https://github.com/PerformanceSuite/Performia/issues).*
