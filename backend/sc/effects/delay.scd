// Delay effect
(
SynthDef(\performiaDelay, {
    arg in=0, out=0, delaytime=0.5, decay=0.5, mix=0.3;
    var sig, delayed;
    
    sig = In.ar(in, 2);
    delayed = CombL.ar(sig, 2.0, delaytime, decay);
    
    Out.ar(out, (sig * (1 - mix)) + (delayed * mix));
}).add;
)
