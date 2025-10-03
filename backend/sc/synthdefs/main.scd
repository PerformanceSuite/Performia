// Main SynthDef file
(
SynthDef(\performiaVoice, {
    arg out=0, freq=440, amp=0.5, gate=1;
    var sig, env;
    
    env = EnvGen.kr(Env.adsr(0.01, 0.3, 0.5, 0.1), gate, doneAction: 2);
    sig = SinOsc.ar(freq) * env * amp;
    
    Out.ar(out, sig);
}).add;

SynthDef(\performiaBass, {
    arg out=0, freq=440, amp=0.5, gate=1;
    var sig, env;
    
    env = EnvGen.kr(Env.adsr(0.01, 0.1, 0.8, 0.1), gate, doneAction: 2);
    sig = LPF.ar(Saw.ar(freq), freq * 2) * env * amp;
    
    Out.ar(out, sig);
}).add;
)
