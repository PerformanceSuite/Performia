// Performia startup file
(
// Load synthdefs
(thisProcess.nowExecutingPath.dirname +/+ "synthdefs/main.scd").load;

// Load effects
(thisProcess.nowExecutingPath.dirname +/+ "effects/reverb.scd").load;
(thisProcess.nowExecutingPath.dirname +/+ "effects/delay.scd").load;

// Load instruments
(thisProcess.nowExecutingPath.dirname +/+ "instruments/voice.scd").load;

// Initialize server configuration
Server.local.options.numInputBusChannels = 2;
Server.local.options.numOutputBusChannels = 2;
Server.local.options.sampleRate = 48000;
Server.local.options.blockSize = 64;
Server.local.options.memSize = 8192 * 16;

// Boot server
Server.local.waitForBoot({
    "Performia SuperCollider environment initialized.".postln;
});
)
