/**
 * Chord label simplification utilities.
 *
 * Converts backend chord notation (e.g., "A:maj", "D:min7") to
 * simplified frontend notation (e.g., "A", "Dm7").
 */

/**
 * Simplify chord label from backend format to frontend format.
 *
 * Transformations:
 * - "A:maj" → "A"
 * - "D:min" → "Dm"
 * - "D:min7" → "Dm7"
 * - "F:maj7" → "Fmaj7"
 * - "C:maj6/9" → "Cmaj6/9"
 * - "G:sus4" → "Gsus4"
 * - "B:dim" → "Bdim"
 * - "E:aug" → "Eaug"
 *
 * @param label - Backend chord label (colon-separated format)
 * @returns Simplified chord label
 */
export function simplifyChordLabel(label: string): string {
  // Handle empty or invalid input
  if (!label || typeof label !== 'string') {
    return '';
  }

  // Split on colon to separate root from quality
  const parts = label.split(':');

  if (parts.length === 1) {
    // No colon, return as-is (already in simple format)
    return label;
  }

  const root = parts[0]; // e.g., "A", "D", "F#", "Bb"
  const quality = parts[1]; // e.g., "maj", "min7", "maj6/9"

  // Simplify major chords (maj → nothing)
  if (quality === 'maj') {
    return root;
  }

  // Handle minor chords
  if (quality.startsWith('min')) {
    const extensions = quality.slice(3); // Get everything after "min"
    return `${root}m${extensions}`;
  }

  // Handle major with extensions (maj7, maj9, etc.)
  if (quality.startsWith('maj')) {
    const extensions = quality.slice(3); // Get everything after "maj"
    return `${root}maj${extensions}`;
  }

  // Handle other qualities (sus, dim, aug, etc.)
  // These are typically already in readable format
  return `${root}${quality}`;
}

/**
 * Batch simplify multiple chord labels.
 *
 * @param labels - Array of backend chord labels
 * @returns Array of simplified chord labels
 */
export function simplifyChordLabels(labels: string[]): string[] {
  return labels.map(simplifyChordLabel);
}

/**
 * Check if a chord label is already in simplified format.
 *
 * @param label - Chord label to check
 * @returns True if label is already simplified (no colon)
 */
export function isSimplified(label: string): boolean {
  return !label.includes(':');
}
