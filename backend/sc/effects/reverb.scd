// Reverb effect
(
SynthDef(\performiaReverb, {
    arg in=0, out=0, mix=0.3, room=0.5, damp=0.5;
    var sig;
    
    sig = In.ar(in, 2);
    sig = FreeVerb2.ar(sig[0], sig[1], mix, room, damp);
    
    Out.ar(out, sig);
}).add;
)
