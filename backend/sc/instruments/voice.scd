// Voice instrument
(
~voice = {
    arg freq=440, amp=0.5;
    Synth(\performiaVoice, [
        \freq, freq,
        \amp, amp
    ]);
};
)
