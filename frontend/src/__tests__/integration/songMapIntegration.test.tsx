/**
 * Integration Tests - Song Map Adapter with Frontend Components
 *
 * Tests the complete flow from backend Song Map to rendered UI components.
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import {
  adaptBackendToFrontend,
  BackendSongMap,
  FrontendSongMap
} from '../../adapters';
import TeleprompterView from '../../../components/TeleprompterView';

// Import test fixtures
import simpleBackendMap from '../../adapters/__tests__/fixtures/simpleBackendMap.json';
import backendMap32193cf0 from '../../adapters/__tests__/fixtures/32193cf0.song_map.json';
import backendMapb72e82dc from '../../adapters/__tests__/fixtures/b72e82dc.song_map.json';

describe('Song Map Integration Tests', () => {
  describe('Backend → Adapter → Frontend Pipeline', () => {
    it('transforms simple backend map successfully', () => {
      const startTime = performance.now();
      const frontendMap = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        title: 'Test Song',
        artist: 'Test Artist'
      });
      const endTime = performance.now();

      // Verify transformation completed quickly
      expect(endTime - startTime).toBeLessThan(100); // <100ms

      // Verify structure
      expect(frontendMap.title).toBe('Test Song');
      expect(frontendMap.artist).toBe('Test Artist');
      expect(frontendMap.sections).toHaveLength(1);
      expect(frontendMap.sections[0].lines).toHaveLength(2);
    });

    it('transforms 32193cf0 backend map (instrumental)', () => {
      const frontendMap = adaptBackendToFrontend(backendMap32193cf0 as BackendSongMap);

      expect(frontendMap.title).toBeTruthy();
      expect(frontendMap.artist).toBeTruthy();
      expect(frontendMap.key).toBe('D# Minor');
      expect(frontendMap.bpm).toBeCloseTo(117.45, 0); // Round to whole number
    });

    it('transforms b72e82dc backend map with sections', () => {
      const frontendMap = adaptBackendToFrontend(backendMapb72e82dc as BackendSongMap);

      expect(frontendMap.sections.length).toBeGreaterThan(0);
      // Should have intro, chorus, outro sections
      const sectionNames = frontendMap.sections.map(s => s.name.toLowerCase());
      expect(sectionNames.some(n => n.includes('intro'))).toBe(true);
      expect(sectionNames.some(n => n.includes('chorus'))).toBe(true);
      expect(sectionNames.some(n => n.includes('outro'))).toBe(true);
    });
  });

  describe('Frontend Song Map Rendering', () => {
    let frontendMap: FrontendSongMap;

    beforeEach(() => {
      frontendMap = adaptBackendToFrontend(simpleBackendMap as BackendSongMap, {
        title: 'Test Song',
        artist: 'Test Artist'
      });
    });

    it('renders TeleprompterView with transformed data', () => {
      const { container } = render(
        <TeleprompterView
          songMap={frontendMap}
          transpose={0}
          capo={0}
          chordDisplay="names"
          diagramVisibility={{}}
          onToggleDiagram={() => {}}
        />
      );

      // Verify teleprompter view is rendered
      const teleprompter = container.querySelector('#teleprompter-view');
      expect(teleprompter).toBeTruthy();

      // Verify lyrics are rendered
      const lyrics = container.querySelectorAll('.syllable');
      expect(lyrics.length).toBeGreaterThan(0);
    });

    it('renders syllables with correct text', () => {
      const { container } = render(
        <TeleprompterView
          songMap={frontendMap}
          transpose={0}
          capo={0}
          chordDisplay="names"
          diagramVisibility={{}}
          onToggleDiagram={() => {}}
        />
      );

      // Check that syllables contain expected text from simpleBackendMap
      const syllables = container.querySelectorAll('.syllable');
      const syllableTexts = Array.from(syllables).map(s => s.textContent);

      expect(syllableTexts.some(t => t?.includes('Hel'))).toBe(true);
      expect(syllableTexts.some(t => t?.includes('lo'))).toBe(true);
      expect(syllableTexts.some(t => t?.includes('world'))).toBe(true);
    });

    it('renders chords when chord display is enabled', () => {
      const { container } = render(
        <TeleprompterView
          songMap={frontendMap}
          transpose={0}
          capo={0}
          chordDisplay="names"
          diagramVisibility={{}}
          onToggleDiagram={() => {}}
        />
      );

      // Check for chord elements
      const chords = container.querySelectorAll('.chord');
      expect(chords.length).toBeGreaterThan(0);
    });
  });

  describe('Performance Tests', () => {
    it('transforms and renders in under 100ms total', () => {
      const startTransform = performance.now();
      const frontendMap = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);
      const endTransform = performance.now();

      const startRender = performance.now();
      render(
        <TeleprompterView
          songMap={frontendMap}
          transpose={0}
          capo={0}
          chordDisplay="names"
          diagramVisibility={{}}
          onToggleDiagram={() => {}}
        />
      );
      const endRender = performance.now();

      const transformTime = endTransform - startTransform;
      const renderTime = endRender - startRender;
      const totalTime = transformTime + renderTime;

      console.log(`Transform: ${transformTime.toFixed(2)}ms, Render: ${renderTime.toFixed(2)}ms, Total: ${totalTime.toFixed(2)}ms`);

      expect(totalTime).toBeLessThan(100);
    });
  });

  describe('Error Handling', () => {
    it('handles empty lyrics gracefully', () => {
      const instrumentalMap: BackendSongMap = {
        ...backendMap32193cf0 as BackendSongMap,
        lyrics: []
      };

      const frontendMap = adaptBackendToFrontend(instrumentalMap);

      expect(() => {
        render(
          <TeleprompterView
            songMap={frontendMap}
            transpose={0}
            capo={0}
            chordDisplay="names"
            diagramVisibility={{}}
            onToggleDiagram={() => {}}
          />
        );
      }).not.toThrow();
    });

    it('handles missing sections gracefully', () => {
      const noSectionsMap: BackendSongMap = {
        ...simpleBackendMap as BackendSongMap,
        sections: undefined
      };

      const frontendMap = adaptBackendToFrontend(noSectionsMap);

      expect(() => {
        render(
          <TeleprompterView
            songMap={frontendMap}
            transpose={0}
            capo={0}
            chordDisplay="names"
            diagramVisibility={{}}
            onToggleDiagram={() => {}}
          />
        );
      }).not.toThrow();
    });
  });

  describe('Data Integrity', () => {
    it('preserves timing information through transformation', () => {
      const frontendMap = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);

      // Get all syllables
      const allSyllables = frontendMap.sections.flatMap(section =>
        section.lines.flatMap(line => line.syllables)
      );

      // Verify all syllables have valid timing
      allSyllables.forEach(syllable => {
        expect(syllable.startTime).toBeGreaterThanOrEqual(0);
        expect(syllable.duration).toBeGreaterThan(0);
      });

      // Verify syllables are in chronological order
      for (let i = 1; i < allSyllables.length; i++) {
        expect(allSyllables[i].startTime).toBeGreaterThanOrEqual(
          allSyllables[i - 1].startTime
        );
      }
    });

    it('maps chords correctly to syllables', () => {
      const frontendMap = adaptBackendToFrontend(simpleBackendMap as BackendSongMap);

      const allSyllables = frontendMap.sections.flatMap(section =>
        section.lines.flatMap(line => line.syllables)
      );

      // Count syllables with chords
      const syllablesWithChords = allSyllables.filter(s => s.chord);

      // We expect some syllables to have chords based on simpleBackendMap
      expect(syllablesWithChords.length).toBeGreaterThan(0);

      // Verify chord labels are simplified (A:maj → A)
      syllablesWithChords.forEach(syllable => {
        expect(syllable.chord).toBeTruthy();
        // Should not contain ":maj" or ":min" after simplification
        expect(syllable.chord).not.toMatch(/:[a-z]+/);
      });
    });
  });
});
