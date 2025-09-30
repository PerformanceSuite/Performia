# Performia SuperCollider Environment

This directory contains SuperCollider code for Performia's real-time audio processing.

## Structure

- `synthdefs/` - Synthesizer definitions
- `effects/` - Audio effects (reverb, delay, etc.)
- `instruments/` - Instrument configurations
- `classes/` - Custom SuperCollider classes

## Usage

1. Start SuperCollider
2. Load `startup.scd`
3. The environment will automatically:
   - Load all synthdefs
   - Configure audio settings
   - Initialize effects
   - Boot the server

## Development

Add new components in their respective directories:
- New synths in `synthdefs/`
- New effects in `effects/`
- New instruments in `instruments/`
