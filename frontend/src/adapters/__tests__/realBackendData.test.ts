/**
 * Real Backend Data Tests
 *
 * Test adapter with actual backend Song Map outputs from the pipeline.
 * Validates transformation and measures performance.
 */

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import {
  adaptBackendToFrontend,
  BackendSongMap,
  validateFrontendSongMap
} from '../index';

// Helper to load backend Song Maps
function loadBackendMap(filename: string): BackendSongMap {
  // Load from fixtures directory
  const path = resolve(__dirname, 'fixtures', filename);
  const content = readFileSync(path, 'utf-8');
  return JSON.parse(content);
}

describe('real backend data', () => {
  describe('32193cf0.song_map.json (Instrumental)', () => {
    const backendMap = loadBackendMap('32193cf0.song_map.json');

    it('transforms successfully', () => {
      const result = adaptBackendToFrontend(backendMap, {
        title: 'Instrumental Test',
        artist: 'Test Artist'
      });

      expect(result).toBeDefined();
      expect(result.title).toBe('Instrumental Test');
      expect(result.artist).toBe('Test Artist');
    });

    it('handles instrumental (empty lyrics)', () => {
      const result = adaptBackendToFrontend(backendMap);

      // Backend may have duplicate sections - check that at least one exists
      expect(result.sections.length).toBeGreaterThanOrEqual(1);
      expect(result.sections[0].name).toBe('Intro');
      // All sections should have no lyrics (instrumental)
      result.sections.forEach(section => {
        expect(section.lines).toHaveLength(0);
      });
    });

    it('extracts metadata correctly', () => {
      const result = adaptBackendToFrontend(backendMap);

      expect(result.key).toBe('D# Minor');
      expect(result.bpm).toBe(117); // Rounded from 117.45
    });

    it('validates output structure', () => {
      const result = adaptBackendToFrontend(backendMap);
      expect(validateFrontendSongMap(result)).toBe(true);
    });

    it('transforms in under 50ms', () => {
      const start = performance.now();
      adaptBackendToFrontend(backendMap);
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(50);
      console.log(`32193cf0 transformation time: ${duration.toFixed(2)}ms`);
    });
  });

  describe('b72e82dc.song_map.json (Multi-section)', () => {
    const backendMap = loadBackendMap('b72e82dc.song_map.json');

    it('transforms successfully', () => {
      const result = adaptBackendToFrontend(backendMap, {
        title: 'Multi-Section Test',
        artist: 'Test Artist'
      });

      expect(result).toBeDefined();
      expect(result.sections.length).toBeGreaterThan(0);
    });

    it('handles multiple sections', () => {
      const result = adaptBackendToFrontend(backendMap);

      // Backend has duplicate sections, should be deduplicated or kept
      expect(result.sections.length).toBeGreaterThanOrEqual(4);

      // Check section names are capitalized
      result.sections.forEach(section => {
        expect(section.name).toMatch(/^[A-Z]/); // Starts with capital
      });
    });

    it('handles zero BPM', () => {
      const result = adaptBackendToFrontend(backendMap);
      expect(result.bpm).toBe(0);
    });

    it('validates output structure', () => {
      const result = adaptBackendToFrontend(backendMap);
      expect(validateFrontendSongMap(result)).toBe(true);
    });

    it('transforms in under 50ms', () => {
      const start = performance.now();
      adaptBackendToFrontend(backendMap);
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(50);
      console.log(`b72e82dc transformation time: ${duration.toFixed(2)}ms`);
    });
  });

  describe('integration_test.song_map.json (Minimal)', () => {
    const backendMap = loadBackendMap('integration_test.song_map.json');

    it('transforms successfully', () => {
      const result = adaptBackendToFrontend(backendMap, {
        title: 'Integration Test',
        artist: 'Test Artist'
      });

      expect(result).toBeDefined();
    });

    it('handles minimal data (all arrays empty)', () => {
      const result = adaptBackendToFrontend(backendMap);

      expect(result.sections).toHaveLength(1);
      expect(result.sections[0].name).toBe('Song'); // Default section
      expect(result.sections[0].lines).toHaveLength(0);
    });

    it('handles empty beats array', () => {
      const result = adaptBackendToFrontend(backendMap);
      expect(result).toBeDefined();
    });

    it('validates output structure', () => {
      const result = adaptBackendToFrontend(backendMap);
      expect(validateFrontendSongMap(result)).toBe(true);
    });

    it('transforms in under 50ms', () => {
      const start = performance.now();
      adaptBackendToFrontend(backendMap);
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(50);
      console.log(`integration_test transformation time: ${duration.toFixed(2)}ms`);
    });
  });

  describe('performance benchmarks', () => {
    it('transforms all backend examples in total under 150ms', () => {
      const maps = [
        loadBackendMap('32193cf0.song_map.json'),
        loadBackendMap('b72e82dc.song_map.json'),
        loadBackendMap('integration_test.song_map.json')
      ];

      const start = performance.now();
      maps.forEach(map => adaptBackendToFrontend(map));
      const duration = performance.now() - start;

      expect(duration).toBeLessThan(150);
      console.log(`Total transformation time for 3 songs: ${duration.toFixed(2)}ms`);
      console.log(`Average per song: ${(duration / 3).toFixed(2)}ms`);
    });

    it('handles repeated transformations efficiently', () => {
      const backendMap = loadBackendMap('32193cf0.song_map.json');

      const start = performance.now();
      for (let i = 0; i < 100; i++) {
        adaptBackendToFrontend(backendMap);
      }
      const duration = performance.now() - start;

      const avgPerTransform = duration / 100;
      expect(avgPerTransform).toBeLessThan(50);
      console.log(`100 transformations completed in ${duration.toFixed(2)}ms`);
      console.log(`Average: ${avgPerTransform.toFixed(2)}ms per transformation`);
    });
  });
});
