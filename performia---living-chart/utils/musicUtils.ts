const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

export const transposeChord = (chord: string | undefined, steps: number): string | undefined => {
    if (!chord) return chord;
    const regex = /^([A-G]#?b?)/;
    const match = chord.match(regex);
    if (!match) return chord;

    const root = match[1];
    const rest = chord.substring(root.length);
    
    let noteIndex = -1;
    if (root.includes('b')) {
        const sharpEquiv = notes.find(n => n.length > 1 && n.endsWith('#')) || '';
        const noteName = root.charAt(0);
        const noteIndexWithoutAccidental = notes.findIndex(n => n.startsWith(noteName));
        noteIndex = (noteIndexWithoutAccidental - 1 + 12) % 12;
    } else {
        noteIndex = notes.indexOf(root);
    }

    if (noteIndex === -1) return chord;
    
    const newIndex = (noteIndex + steps + 12) % 12;
    return notes[newIndex] + rest;
};
