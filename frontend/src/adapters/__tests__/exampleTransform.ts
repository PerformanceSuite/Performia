/**
 * Example transformation demonstration
 *
 * Run with: npm test -- exampleTransform
 */

import { adaptBackendToFrontend } from '../index';
import simpleBackendMap from './fixtures/simpleBackendMap.json';

// Transform the simple backend map
const frontendMap = adaptBackendToFrontend(simpleBackendMap as any, {
  title: 'Test Song',
  artist: 'Test Artist'
});

// Output the result
console.log('\n=== EXAMPLE TRANSFORMATION ===\n');
console.log('Input (Backend Format):');
console.log('- ID:', simpleBackendMap.id);
console.log('- Duration:', simpleBackendMap.duration_sec, 'seconds');
console.log('- BPM:', simpleBackendMap.tempo.bpm_global);
console.log('- Lyrics:', simpleBackendMap.lyrics.length, 'entries');
console.log('- Chords:', simpleBackendMap.chords.length, 'entries');
console.log('- Sections:', simpleBackendMap.sections?.length || 0, 'entries');

console.log('\nOutput (Frontend Format):');
console.log('- Title:', frontendMap.title);
console.log('- Artist:', frontendMap.artist);
console.log('- Key:', frontendMap.key);
console.log('- BPM:', frontendMap.bpm);
console.log('- Sections:', frontendMap.sections.length);

frontendMap.sections.forEach((section, i) => {
  console.log(`\n  Section ${i + 1}: ${section.name}`);
  console.log(`  - Lines: ${section.lines.length}`);
  section.lines.forEach((line, j) => {
    console.log(`    Line ${j + 1}: ${line.syllables.length} syllables`);
    const text = line.syllables.map(s => s.text).join(' ');
    const chords = line.syllables.filter(s => s.chord).map(s => s.chord);
    console.log(`      Text: "${text}"`);
    if (chords.length > 0) {
      console.log(`      Chords: [${chords.join(', ')}]`);
    }
  });
});

console.log('\n=== COMPLETE FRONTEND OUTPUT ===\n');
console.log(JSON.stringify(frontendMap, null, 2));
