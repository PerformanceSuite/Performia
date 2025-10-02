# Chord Layout System Documentation

**Created:** October 2, 2025
**Purpose:** Ensure chords never overlap with lyrics and maintain consistent alignment

---

## Problem Statement

The original Teleprompter had chord/lyric overlap issues:
- Chords used `position: absolute` causing overlaps
- Fixed `min-height: 180px` didn't scale with font size
- Inconsistent vertical alignment between syllables with/without chords

---

## Solution: Flexbox Column Layout

### Core Principles

1. **No Absolute Positioning** - Chords are in the normal document flow
2. **Consistent Spacing** - Every syllable reserves vertical space for chords
3. **Dynamic Scaling** - All dimensions scale with `--base-font-size`
4. **Alignment Guarantees** - Flexbox ensures proper vertical alignment

---

## CSS Architecture

### Container Structure

```
.lyric-line (flex, center)
└── .syllables-wrapper (flex, baseline)
    └── .syllable-container (inline-flex, column, flex-end)
        ├── .chord (static position, min-height)
        │   ├── .chord-name (text)
        │   └── .chord-diagram-wrapper (optional)
        └── .syllable (text with highlight effects)
```

### Key CSS Properties

#### `.lyric-line`
```css
min-height: calc(var(--base-font-size) * 4);
```
- Scales with font size changes
- Ensures vertical space for chords + lyrics

#### `.syllables-wrapper`
```css
align-items: baseline;
```
- Aligns syllable baselines for consistent lyric line
- Changed from `flex-end` for better text alignment

#### `.syllable-container`
```css
display: inline-flex;
flex-direction: column;
align-items: center;
justify-content: flex-end;
min-height: calc(var(--base-font-size) * 2);
```
- **`inline-flex`**: Allows horizontal flow of syllables
- **`flex-direction: column`**: Stacks chord above lyric
- **`align-items: center`**: Centers chord above syllable
- **`justify-content: flex-end`**: Aligns syllables to bottom
- **`min-height`**: Reserves space for chord

#### `.chord`
```css
position: static;
transform: none;
min-height: calc(var(--base-font-size) * 0.75 + 1rem);
margin-bottom: 0.5rem;
```
- **`position: static`**: No absolute positioning = no overlaps
- **`min-height`**: Prevents layout shift when chords appear/disappear
- **Dynamic scaling**: All dimensions use `calc()` with base font size

#### `.chord-spacer`
```css
visibility: hidden;
```
- Invisible placeholder for syllables without chords
- Maintains consistent vertical alignment across entire line

---

## React Component Integration

### TeleprompterView.tsx Changes

**Before:**
```tsx
{syllable.chord && displayedChord && (
    <div className="chord">...</div>
)}
```

**After:**
```tsx
{syllable.chord && displayedChord ? (
    <div className="chord">
        <span className="chord-name">{displayedChord}</span>
        ...
    </div>
) : (
    <div className="chord chord-spacer" aria-hidden="true">
        {/* Empty spacer for alignment */}
    </div>
)}
```

**Why:**
- Always renders chord container (visible or spacer)
- Ensures consistent height across all syllables
- `aria-hidden="true"` prevents screen readers from announcing empty spacers

---

## Scaling Behavior

All dimensions scale proportionally with `--base-font-size`:

| Element | Size Formula | Example (3rem base) |
|---------|--------------|---------------------|
| Lyric line min-height | `base * 4` | 12rem (192px) |
| Syllable container min-height | `base * 2` | 6rem (96px) |
| Chord name font size | `base * 0.75` | 2.25rem (36px) |
| Chord min-height | `base * 0.75 + 1rem` | 3.25rem (52px) |
| Diagram size | `base * 1.5` × `base * 1.8` | 4.5rem × 5.4rem |

### Font Size Adjustment Example

**50% scale** (`--base-font-size: 1.5rem`):
- Lyric line: 6rem (96px)
- Chord: 1.125rem (18px)

**150% scale** (`--base-font-size: 4.5rem`):
- Lyric line: 18rem (288px)
- Chord: 3.375rem (54px)

---

## Responsive Breakpoints

### Tablet (< 768px)
```css
.lyric-line { padding: 0 2rem; }
.chord-name { font-size: calc(var(--base-font-size) * 0.7); }
```

### Mobile (< 480px)
```css
.lyric-line { padding: 0 1rem; }
.syllable-container { margin-right: 0.3ch; }
```

---

## Chord Display Modes

### 1. Names Only (Default)
```css
.chord-name { display: block; }
.chord-diagram-wrapper { display: none; }
```

### 2. Diagrams Only
```css
.app-container.show-diagrams .chord-name { display: none; }
.app-container.show-diagrams .chord-diagram-wrapper { display: flex; }
```

**Height adjustment:**
```css
.syllable-container.show-diagram .chord {
    min-height: calc(var(--base-font-size) * 2.5);
}
```

### 3. Hidden
```css
.app-container.hide-chords .chord { display: none; }
```

---

## Testing Checklist

### ✅ Visual Tests
- [ ] No overlapping chords at 50%, 100%, 150% font size
- [ ] Consistent syllable baseline alignment
- [ ] Chords centered above syllables
- [ ] Proper spacing between chord and lyric (0.5rem margin)
- [ ] Diagrams display correctly when toggled

### ✅ Responsive Tests
- [ ] Layout works on desktop (1920×1080)
- [ ] Layout works on tablet (768×1024)
- [ ] Layout works on mobile (375×667)

### ✅ Functional Tests
- [ ] Chord highlighting works (amber → white → cyan)
- [ ] Chord transposition doesn't break layout
- [ ] Diagram toggle doesn't cause layout shift
- [ ] Long chord names don't overflow
- [ ] Multiple consecutive chords don't overlap

### ✅ Accessibility Tests
- [ ] Screen readers skip chord spacers (`aria-hidden="true"`)
- [ ] Chord/lyric relationship is clear
- [ ] Keyboard navigation works
- [ ] High contrast mode maintains visibility

---

## Performance Considerations

### Optimizations Applied
1. **Fixed min-heights** - Prevents layout thrashing
2. **CSS calc() instead of JS** - Browser-native scaling
3. **Visibility: hidden** vs display: none - Maintains layout without reflow
4. **Memoized components** - React.memo on TeleprompterView

### Expected Performance
- **60fps rendering** - No layout recalculation during playback
- **Instant font size changes** - CSS variables update immediately
- **Zero layout shift** - Min-heights prevent reflow

---

## Debugging Tips

### Check for Overlaps
```javascript
// Run in browser console
document.querySelectorAll('.chord').forEach(chord => {
    const rect = chord.getBoundingClientRect();
    const syllable = chord.nextElementSibling;
    const syllableRect = syllable?.getBoundingClientRect();

    if (syllableRect && rect.bottom > syllableRect.top) {
        console.warn('Overlap detected!', chord, syllable);
    }
});
```

### Visualize Layout Boxes
```css
/* Add to index.css temporarily */
.syllable-container { outline: 1px solid red; }
.chord { outline: 1px solid blue; }
.syllable { outline: 1px solid green; }
```

### Font Size Inspector
```javascript
// Check current base font size
const root = document.documentElement;
const fontSize = getComputedStyle(root).getPropertyValue('--base-font-size');
console.log('Base font size:', fontSize);
```

---

## Future Improvements

### Planned Enhancements
1. **Variable chord widths** - Adjust spacing based on chord complexity (e.g., Cmaj7 vs C)
2. **Chord collision detection** - Auto-adjust spacing when chords are very close
3. **Vertical rhythm system** - Ensure consistent spacing ratios throughout
4. **Custom font size per section** - Allow different scales for verse vs chorus

### Potential Optimizations
1. **Virtual scrolling** - Only render visible lines (Sprint 3)
2. **CSS containment** - Isolate layout calculations
3. **GPU acceleration** - Transform-based animations only

---

## References

**Related Files:**
- `frontend/src/index.css` - All layout styles
- `frontend/components/TeleprompterView.tsx` - Component implementation
- `PERFORMIA_MASTER_DOCS.md` - Complete project documentation

**Related Documentation:**
- [CSS Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS calc() Function](https://developer.mozilla.org/en-US/docs/Web/CSS/calc)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| Oct 2, 2025 | Initial implementation | Fix chord/lyric overlaps |
| Oct 2, 2025 | Added spacer divs | Ensure consistent alignment |
| Oct 2, 2025 | Dynamic min-heights | Scale with font size |
| Oct 2, 2025 | Responsive breakpoints | Mobile/tablet support |

---

**Maintained by:** Performia Development Team
**Last Updated:** October 2, 2025
**Version:** 1.0
