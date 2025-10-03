import { SongMap } from '../types';

export const initialSongMap: SongMap = {
    title: "Yesterday",
    artist: "The Beatles",
    key: "F Major",
    bpm: 72,
    sections: [
        { 
            name: "Verse 1", 
            lines: [
                { syllables: [ { chord: 'Fmaj7', text: 'All', startTime: 2.8, duration: 0.25 }, { text: 'my', startTime: 3.05, duration: 0.2 }, { text: 'trou', startTime: 3.45, duration: 0.3 }, { text: 'bles', startTime: 3.75, duration: 0.5 }, { text: 'seemed', startTime: 4.4, duration: 0.3 }, { text: 'so', startTime: 4.7, duration: 0.25 }, { text: 'far', startTime: 5.1, duration: 0.3 }, { text: 'a', startTime: 5.4, duration: 0.2 }, { text: 'way', startTime: 5.6, duration: 1.2 } ] },
                { syllables: [ { chord: 'Em7', text: 'Now', startTime: 8.0, duration: 0.25 }, { text: 'it', startTime: 8.25, duration: 0.2 }, { text: 'looks', startTime: 8.55, duration: 0.25 }, { text: 'as', startTime: 8.8, duration: 0.2 }, { text: 'though', startTime: 9.0, duration: 0.3 }, { text: "they're", startTime: 9.4, duration: 0.3 }, { chord: 'A7', text: 'here', startTime: 9.8, duration: 0.3 }, { text: 'to', startTime: 10.1, duration: 0.2 }, { chord: 'Dm', text: 'stay', startTime: 10.4, duration: 1.5 } ] },
                { syllables: [ { text: 'Oh,', startTime: 13.0, duration: 0.3 }, { text: 'I', startTime: 13.6, duration: 0.2 }, { text: 'be', startTime: 13.8, duration: 0.2 }, { chord: 'C', text: 'lieve', startTime: 14.0, duration: 0.5 }, { text: 'in', startTime: 14.8, duration: 0.3 }, { chord: 'Bb', text: 'yes', startTime: 15.3, duration: 0.4 }, { text: 'ter', startTime: 15.7, duration: 0.3 }, { chord: 'F', text: 'day', startTime: 16.0, duration: 1.5 } ] }
            ]
        }
    ]
};
