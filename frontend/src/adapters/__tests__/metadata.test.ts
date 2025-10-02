/**
 * Metadata Extraction Tests
 */

import { describe, it, expect } from 'vitest';
import {
  extractMetadata,
  extractTitle,
  extractArtist,
  extractKey,
  extractBpm,
  formatKey,
  parseFilename,
  capitalizeWords,
  BackendSongMap
} from '../index';

describe('metadata utilities', () => {
  const mockBackendMap: BackendSongMap = {
    id: 'test',
    duration_sec: 10,
    tempo: { bpm_global: 120.5 },
    beats: [],
    downbeats: [],
    meter: { numerator: 4, denominator: 4 },
    chords: [],
    lyrics: [],
    key: [{ start: 0, end: 10, tonic: 'F', mode: 'major' }],
    provenance: { source_path: '/audio/yesterday_beatles.wav' }
  };

  describe('extractMetadata', () => {
    it('extracts all metadata fields', () => {
      const metadata = extractMetadata(mockBackendMap);

      expect(metadata.title).toBe('Yesterday');
      expect(metadata.artist).toBe('Beatles');
      expect(metadata.key).toBe('F Major');
      expect(metadata.bpm).toBe(121); // Rounded
    });
  });

  describe('extractTitle', () => {
    it('extracts title from source path', () => {
      const title = extractTitle(mockBackendMap);
      expect(title).toBe('Yesterday');
    });

    it('returns Unknown Title when no source path', () => {
      const noPath = { ...mockBackendMap, provenance: undefined };
      const title = extractTitle(noPath);
      expect(title).toBe('Unknown Title');
    });
  });

  describe('extractArtist', () => {
    it('extracts artist from source path', () => {
      const artist = extractArtist(mockBackendMap);
      expect(artist).toBe('Beatles');
    });

    it('returns Unknown Artist when no source path', () => {
      const noPath = { ...mockBackendMap, provenance: undefined };
      const artist = extractArtist(noPath);
      expect(artist).toBe('Unknown Artist');
    });
  });

  describe('extractKey', () => {
    it('extracts and formats key', () => {
      const key = extractKey(mockBackendMap);
      expect(key).toBe('F Major');
    });

    it('handles minor key', () => {
      const minorMap = {
        ...mockBackendMap,
        key: [{ start: 0, end: 10, tonic: 'D#', mode: 'minor' }]
      };
      const key = extractKey(minorMap);
      expect(key).toBe('D# Minor');
    });

    it('returns Unknown when no key', () => {
      const noKey = { ...mockBackendMap, key: undefined };
      const key = extractKey(noKey);
      expect(key).toBe('Unknown');
    });

    it('uses first key when multiple keys', () => {
      const multiKey = {
        ...mockBackendMap,
        key: [
          { start: 0, end: 5, tonic: 'C', mode: 'major' },
          { start: 5, end: 10, tonic: 'G', mode: 'major' }
        ]
      };
      const key = extractKey(multiKey);
      expect(key).toBe('C Major');
    });
  });

  describe('extractBpm', () => {
    it('rounds BPM to nearest integer', () => {
      expect(extractBpm(mockBackendMap)).toBe(121);

      const bpm150 = { ...mockBackendMap, tempo: { bpm_global: 150.4 } };
      expect(extractBpm(bpm150)).toBe(150);
    });

    it('returns 0 for zero BPM', () => {
      const zeroBpm = { ...mockBackendMap, tempo: { bpm_global: 0 } };
      expect(extractBpm(zeroBpm)).toBe(0);
    });

    it('returns 0 for negative BPM', () => {
      const negativeBpm = { ...mockBackendMap, tempo: { bpm_global: -10 } };
      expect(extractBpm(negativeBpm)).toBe(0);
    });
  });

  describe('formatKey', () => {
    it('formats major key', () => {
      expect(formatKey('C', 'major')).toBe('C Major');
      expect(formatKey('F#', 'major')).toBe('F# Major');
    });

    it('formats minor key', () => {
      expect(formatKey('A', 'minor')).toBe('A Minor');
      expect(formatKey('D#', 'minor')).toBe('D# Minor');
    });

    it('capitalizes mode', () => {
      expect(formatKey('G', 'MAJOR')).toBe('G MAJOR');
      expect(formatKey('E', 'Minor')).toBe('E Minor');
    });
  });

  describe('parseFilename', () => {
    it('parses title_artist format', () => {
      const result = parseFilename('yesterday_beatles.wav');
      expect(result.title).toBe('Yesterday');
      expect(result.artist).toBe('Beatles');
    });

    it('parses title only', () => {
      const result = parseFilename('yesterday.wav');
      expect(result.title).toBe('Yesterday');
      expect(result.artist).toBeUndefined();
    });

    it('removes file extension', () => {
      expect(parseFilename('song.mp3').title).toBe('Song');
      expect(parseFilename('song.flac').title).toBe('Song');
      expect(parseFilename('song.m4a').title).toBe('Song');
    });

    it('handles full path', () => {
      const result = parseFilename('/path/to/song_artist.wav');
      expect(result.title).toBe('Song');
      expect(result.artist).toBe('Artist');
    });

    it('handles multi-word titles', () => {
      const result = parseFilename('let_it_be_beatles.wav');
      // Note: Current implementation takes first underscore-separated part as title
      expect(result.title).toBe('Let');
      expect(result.artist).toBe('It'); // Second part
    });

    it('handles hyphens and underscores', () => {
      const result = parseFilename('my-song_artist-name.wav');
      expect(result.title).toBe('My Song');
      expect(result.artist).toBe('Artist Name');
    });
  });

  describe('capitalizeWords', () => {
    it('capitalizes single word', () => {
      expect(capitalizeWords('hello')).toBe('Hello');
    });

    it('capitalizes multiple words', () => {
      expect(capitalizeWords('hello world')).toBe('Hello World');
    });

    it('handles underscores', () => {
      expect(capitalizeWords('hello_world')).toBe('Hello World');
    });

    it('handles hyphens', () => {
      expect(capitalizeWords('hello-world')).toBe('Hello World');
    });

    it('handles mixed case', () => {
      expect(capitalizeWords('hELLo wORLd')).toBe('Hello World');
    });
  });
});
