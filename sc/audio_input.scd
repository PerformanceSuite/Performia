// Performia System - Audio Input Processing for Guitar
// Optimized for Presonus Quantum 2626

(
// Server configuration for ultra-low latency
s.options.inDevice_("Presonus Quantum 2626");
s.options.outDevice_("Presonus Quantum 2626");  
s.options.sampleRate = 48000;
s.options.blockSize = 64;  // 1.33ms @ 48kHz
s.options.hardwareBufferSize = 128;
s.options.numInputBusChannels = 2;  // Stereo input for guitar
s.options.numOutputBusChannels = 8;  // Multiple outputs for agents
s.options.memSize = 65536 * 2;  // Increased memory
s.reboot;

s.waitForBoot({
    
    // Global variables
    ~inputAnalyzer = nil;
    ~isListening = false;
    ~pythonAddr = NetAddr("127.0.0.1", 57120);  // Python OSC receiver
    
    // Analysis synth for guitar input
    SynthDef(\guitarAnalyzer, {
        arg inbus=0, 
            analysisRate=60,  // 60Hz analysis rate for low latency
            pitchConfidence=0.5,
            onsetThreshold=0.3,
            gate=1;
            
        var input, mono, amp, freq, hasFreq, onset, chain;
        var fftBuf = LocalBuf(1024);
        
        // Get stereo input and convert to mono
        input = SoundIn.ar([inbus, inbus+1]);
        mono = Mix(input) * 0.5;
        
        // Amplitude tracking (instant)
        amp = Amplitude.kr(mono, 0.001, 0.01);
        
        // Pitch detection with very low latency settings
        # freq, hasFreq = Pitch.kr(mono,
            initFreq: 440.0,
            minFreq: 60.0,      // Low E on guitar
            maxFreq: 4000.0,    // High notes
            execFreq: 200.0,    // 200Hz tracking rate (5ms)
            maxBinsPerOctave: 64,
            median: 1,
            ampThreshold: 0.01,
            peakThreshold: 0.5,
            downSample: 1
        );
        
        // Onset detection
        chain = FFT(fftBuf, mono);
        onset = Onsets.kr(chain, onsetThreshold, \power);
        
        // Send analysis data to Python via OSC
        SendReply.kr(Impulse.kr(analysisRate), '/guitar_analysis',
            [amp, freq, hasFreq, onset]
        );
        
        // Pass through audio (optional monitoring)
        // Out.ar(0, mono * 0.1 * gate);  // Quiet monitoring
        
        // Free on gate release
        FreeSelf.kr(1 - gate);
    }).add;
    
    // Chord detection synth using chromagram
    SynthDef(\chordAnalyzer, {
        arg inbus=0, analysisRate=30;
        
        var input, mono, chain, chroma;
        var fftBuf = LocalBuf(2048);
        
        input = SoundIn.ar([inbus, inbus+1]);
        mono = Mix(input) * 0.5;
        
        chain = FFT(fftBuf, mono);
        chroma = Chromagram.kr(chain, 2048, 12);
        
        // Send chromagram to Python for chord detection
        SendReply.kr(Impulse.kr(analysisRate), '/chromagram',
            chroma  // 12 values representing pitch classes
        );
    }).add;
    
    // Enhanced pitch tracker for melodic analysis
    SynthDef(\melodicAnalyzer, {
        arg inbus=0, analysisRate=100;
        
        var input, mono, freq, hasFreq, amp, centroid, flatness;
        var chain, fftBuf = LocalBuf(2048);
        
        input = SoundIn.ar([inbus, inbus+1]);
        mono = Mix(input) * 0.5;
        
        // Multiple pitch detection algorithms for accuracy
        # freq, hasFreq = Pitch.kr(mono, 
            initFreq: 440.0,
            minFreq: 60.0,
            maxFreq: 2000.0,
            execFreq: 200.0
        );
        
        // Spectral features
        chain = FFT(fftBuf, mono);
        centroid = SpecCentroid.kr(chain);
        flatness = SpecFlatness.kr(chain);
        amp = Amplitude.kr(mono);
        
        SendReply.kr(Impulse.kr(analysisRate), '/melodic_analysis',
            [freq, hasFreq, amp, centroid, flatness]
        );
    }).add;
    
    // Rhythm detection synth
    SynthDef(\rhythmAnalyzer, {
        arg inbus=0;
        
        var input, mono, onsets, tempo, chain;
        var fftBuf = LocalBuf(512);  // Smaller for rhythm
        
        input = SoundIn.ar([inbus, inbus+1]);
        mono = Mix(input) * 0.5;
        
        chain = FFT(fftBuf, mono);
        
        // Multiple onset detectors for accuracy
        onsets = Onsets.kr(chain, 0.5, \power);
        
        // BeatTrack for tempo detection
        # tempo = BeatTrack.kr(chain);
        
        SendReply.kr(onsets, '/onset_detected', 1);
        SendReply.kr(Impulse.kr(2), '/tempo_estimate', tempo);
    }).add;
    
    // MIDI setup for pedal control
    MIDIIn.connectAll;
    
    // MIDI responder for sustain pedal
    MIDIFunc.cc({ |val, cc, chan, src|
        if(cc == 64, {  // Sustain pedal
            if(val > 63, {
                // Start listening
                if(~isListening.not, {
                    "Starting guitar analysis...".postln;
                    ~inputAnalyzer = Synth(\guitarAnalyzer);
                    ~chordAnalyzer = Synth(\chordAnalyzer);
                    ~isListening = true;
                    ~pythonAddr.sendMsg("/listening/start", 1);
                });
            }, {
                // Stop listening
                if(~isListening, {
                    "Stopping guitar analysis...".postln;
                    ~inputAnalyzer.set(\gate, 0);
                    ~chordAnalyzer.free;
                    ~isListening = false;
                    ~pythonAddr.sendMsg("/listening/stop", 0);
                });
            });
        });
        
        // Mode change pedal (CC 65)
        if(cc == 65 and: (val > 63), {
            ~pythonAddr.sendMsg("/mode/change", 1);
        });
        
        // Expression pedal (CC 11)
        if(cc == 11, {
            ~pythonAddr.sendMsg("/expression", val / 127.0);
        });
        
        // Tap tempo (CC 80)
        if(cc == 80 and: (val > 63), {
            ~pythonAddr.sendMsg("/tap", 1);
        });
    });
    
    // OSC responder for Python commands
    OSCFunc({ |msg|
        var cmd = msg[1];
        case
        { cmd == \startAnalysis } {
            if(~isListening.not, {
                ~inputAnalyzer = Synth(\guitarAnalyzer);
                ~isListening = true;
            });
        }
        { cmd == \stopAnalysis } {
            if(~isListening, {
                ~inputAnalyzer.set(\gate, 0);
                ~isListening = false;
            });
        }
        { cmd == \setParam } {
            var param = msg[2];
            var value = msg[3];
            if(~inputAnalyzer.notNil, {
                ~inputAnalyzer.set(param, value);
            });
        };
    }, '/control');
    
    // Test signal generator (for debugging without guitar)
    SynthDef(\testSignal, {
        arg freq=440, amp=0.1, out=0;
        var sig = SinOsc.ar(freq) * amp;
        Out.ar(out, sig ! 2);
    }).add;
    
    // Startup message
    "Performia Audio Input System Ready".postln;
    "Waiting for MIDI pedal input on CC 64 (sustain)...".postln;
    
    // Optional: Create a test GUI
    if(false, {  // Set to true to show GUI
        Window.closeAll;
        w = Window("Performia Input Monitor", Rect(100, 100, 400, 300));
        
        ~ampSlider = EZSlider(w, Rect(20, 20, 360, 20), "Input Level", 
            [0, 1], unitWidth: 30);
        ~freqText = StaticText(w, Rect(20, 50, 360, 20))
            .string_("Pitch: --");
        ~chordText = StaticText(w, Rect(20, 80, 360, 20))
            .string_("Chord: --");
        ~statusText = StaticText(w, Rect(20, 110, 360, 20))
            .string_("Status: Not listening");
            
        w.front;
        
        // Update GUI from analysis
        OSCFunc({ |msg|
            var amp = msg[3];
            var freq = msg[4];
            var hasFreq = msg[5];
            
            {
                ~ampSlider.value = amp;
                if(hasFreq > 0.5, {
                    ~freqText.string = "Pitch: " ++ freq.round(0.1) ++ " Hz";
                });
            }.defer;
        }, '/guitar_analysis');
    });
});
)

// Utility functions for testing

// Test with a sine wave
(
~testInput = { |freq=440|
    x = Synth(\testSignal, [\freq, freq, \amp, 0.1]);
    "Test signal at " ++ freq ++ "Hz - press Cmd+. to stop".postln;
};
)

// Manual start/stop
(
~startListening = {
    if(~isListening.not, {
        ~inputAnalyzer = Synth(\guitarAnalyzer);
        ~chordAnalyzer = Synth(\chordAnalyzer);
        ~isListening = true;
        "Started listening".postln;
    });
};

~stopListening = {
    if(~isListening, {
        ~inputAnalyzer.set(\gate, 0);
        ~chordAnalyzer.free;
        ~isListening = false;
        "Stopped listening".postln;
    });
};
)