# Real-Time Audio DSP Techniques (C++ Low-Latency 2025)

**Purpose:** Modern C++ techniques for ultra-low-latency audio processing in Performia

**Last Updated:** October 4, 2025

---

## ⚡ Latency Requirements & Targets

### Industry Standards
- **< 10ms:** Required for real-time musical applications (no perceived delay)
- **< 5ms:** Professional studio monitoring
- **< 3ms:** Live performance (guitar amp simulators, vocal effects)
- **< 1ms:** Critical applications (drum triggers, DJ software)

### Buffer Size vs Latency

| Sample Rate | Buffer Size | Latency    | Use Case                |
|-------------|-------------|------------|-------------------------|
| 48kHz       | 64 samples  | **1.3ms**  | Ultra-low (best case)   |
| 48kHz       | 128 samples | **2.7ms**  | Pro audio standard      |
| 48kHz       | 256 samples | **5.3ms**  | Balanced performance    |
| 48kHz       | 512 samples | **10.7ms** | Safe for most systems   |
| 44.1kHz     | 256 samples | **5.8ms**  | Consumer audio standard |

**Formula:** `Latency (ms) = (Buffer Size / Sample Rate) × 1000`

**Total System Latency = ADC + Processing + DAC + Driver Overhead**

---

## 🏗️ Modern C++ Low-Latency Architecture

### C++20/C++23 Features for Audio (2025)

#### 1. **Concepts for Type Safety**
```cpp
template<typename T>
concept AudioSample = std::is_floating_point_v<T>;

template<AudioSample T>
class AudioBuffer {
    std::vector<T> data;
    // Compile-time guarantee: only float/double allowed
};
```

#### 2. **constexpr for Compile-Time Computation**
```cpp
constexpr float calculateGain(float db) {
    return std::pow(10.0f, db / 20.0f);
}

// Computed at compile time - zero runtime cost!
constexpr float gain_6dB = calculateGain(6.0f);
```

#### 3. **std::span for Zero-Copy Views**
```cpp
void processAudio(std::span<float> samples) {
    // No allocation, no copy - just a view
    for (auto& sample : samples) {
        sample *= 0.5f;  // Reduce volume
    }
}
```

#### 4. **std::atomic for Lock-Free State**
```cpp
std::atomic<float> currentGain { 1.0f };

// Audio thread (real-time)
void processBlock(float* buffer, int numSamples) {
    float gain = currentGain.load(std::memory_order_relaxed);
    for (int i = 0; i < numSamples; ++i)
        buffer[i] *= gain;
}

// UI thread (non-real-time)
void setGain(float newGain) {
    currentGain.store(newGain, std::memory_order_release);
}
```

---

## 🚀 SIMD Optimization (2025 Best Practices)

### SIMD = Single Instruction, Multiple Data
Process 4-8 samples simultaneously (SSE/AVX/NEON)

### JUCE 7 SIMD Classes
```cpp
#include <juce_dsp/juce_dsp.h>

void processWithSIMD(float* buffer, int numSamples, float gain)
{
    using SIMDFloat = juce::dsp::SIMDRegister<float>;

    int numSIMDOps = numSamples / SIMDFloat::size();

    auto* simdBuffer = reinterpret_cast<SIMDFloat*>(buffer);

    for (int i = 0; i < numSIMDOps; ++i)
    {
        simdBuffer[i] *= gain;  // Process 4-8 samples at once!
    }

    // Handle remaining samples (scalar)
    for (int i = numSIMDOps * SIMDFloat::size(); i < numSamples; ++i)
    {
        buffer[i] *= gain;
    }
}
```

### Platform-Specific SIMD

**SSE (Intel x86):**
```cpp
#include <xmmintrin.h>  // SSE

void processSSE(float* buffer, int numSamples, float gain)
{
    __m128 gainVec = _mm_set1_ps(gain);  // Load gain into all 4 lanes

    for (int i = 0; i < numSamples; i += 4)
    {
        __m128 samples = _mm_loadu_ps(&buffer[i]);     // Load 4 samples
        samples = _mm_mul_ps(samples, gainVec);        // Multiply
        _mm_storeu_ps(&buffer[i], samples);            // Store back
    }
}
```

**NEON (ARM - iOS/Android):**
```cpp
#include <arm_neon.h>

void processNEON(float* buffer, int numSamples, float gain)
{
    float32x4_t gainVec = vdupq_n_f32(gain);

    for (int i = 0; i < numSamples; i += 4)
    {
        float32x4_t samples = vld1q_f32(&buffer[i]);
        samples = vmulq_f32(samples, gainVec);
        vst1q_f32(&buffer[i], samples);
    }
}
```

**Recommendation:** Use JUCE's abstraction for cross-platform compatibility!

---

## 🔒 Lock-Free Programming for Audio

### Rule: NEVER use locks in audio thread

### Lock-Free Data Structures

#### 1. **Single-Producer Single-Consumer (SPSC) Queue**
```cpp
#include <juce_core/juce_core.h>

class AudioToUIQueue
{
public:
    AudioToUIQueue(int size) : fifo(size), buffer(size) {}

    // Called by audio thread
    void push(const Event& event)
    {
        int start1, size1, start2, size2;
        fifo.prepareToWrite(1, start1, size1, start2, size2);

        if (size1 > 0) {
            buffer[start1] = event;
            fifo.finishedWrite(size1);
        }
        // If full, drop event (acceptable for real-time)
    }

    // Called by UI thread
    bool pop(Event& event)
    {
        int start1, size1, start2, size2;
        fifo.prepareToRead(1, start1, size1, start2, size2);

        if (size1 > 0) {
            event = buffer[start1];
            fifo.finishedRead(size1);
            return true;
        }
        return false;
    }

private:
    juce::AbstractFifo fifo;
    std::vector<Event> buffer;
};
```

#### 2. **Lock-Free Parameter Updates**
```cpp
struct AudioParameters
{
    std::atomic<float> gain { 1.0f };
    std::atomic<float> pan { 0.0f };
    std::atomic<int> filterType { 0 };
};

// Audio thread reads with relaxed ordering (fastest)
float currentGain = params.gain.load(std::memory_order_relaxed);

// UI thread writes with release ordering
params.gain.store(newGain, std::memory_order_release);
```

---

## 🧠 Memory Management for Real-Time

### Pre-Allocation Strategy

```cpp
class RealTimeAudioProcessor
{
public:
    void prepare(double sampleRate, int maxBlockSize)
    {
        // Pre-allocate ALL buffers during prepare phase
        tempBuffer.resize(maxBlockSize);
        fftBuffer.resize(2048);
        delayLine.resize(sampleRate * 2);  // 2 seconds

        // Initialize DSP objects
        filter.prepare(sampleRate);
    }

    void process(float* buffer, int numSamples)
    {
        // NO allocations here! Use pre-allocated buffers
        std::copy(buffer, buffer + numSamples, tempBuffer.data());

        filter.process(tempBuffer.data(), numSamples);

        std::copy(tempBuffer.data(), tempBuffer.data() + numSamples, buffer);
    }

private:
    std::vector<float> tempBuffer;     // Pre-allocated
    std::vector<float> fftBuffer;
    std::vector<float> delayLine;
    BiquadFilter filter;
};
```

### Stack Allocation for Small Buffers
```cpp
void processBlock(float* input, int numSamples)
{
    // Stack allocation - very fast, no heap
    float stackBuffer[256];  // Fixed size

    if (numSamples <= 256) {
        // Use stack buffer
        std::copy(input, input + numSamples, stackBuffer);
        applyGain(stackBuffer, numSamples, 0.5f);
    } else {
        // Fallback to pre-allocated heap buffer
        applyGain(tempBuffer.data(), numSamples, 0.5f);
    }
}
```

---

## 🎛️ DSP Algorithm Optimization

### 1. Biquad Filter (Efficient Implementation)

```cpp
class BiquadFilter
{
public:
    void setLowPass(float sampleRate, float frequency, float Q)
    {
        float w0 = 2.0f * M_PI * frequency / sampleRate;
        float alpha = std::sin(w0) / (2.0f * Q);

        b0 = (1.0f - std::cos(w0)) / 2.0f;
        b1 = 1.0f - std::cos(w0);
        b2 = b0;
        a0 = 1.0f + alpha;
        a1 = -2.0f * std::cos(w0);
        a2 = 1.0f - alpha;

        // Normalize coefficients
        b0 /= a0; b1 /= a0; b2 /= a0;
        a1 /= a0; a2 /= a0;
    }

    float process(float input)
    {
        float output = b0 * input + b1 * x1 + b2 * x2
                                  - a1 * y1 - a2 * y2;

        x2 = x1; x1 = input;
        y2 = y1; y1 = output;

        return output;
    }

private:
    float b0 = 1, b1 = 0, b2 = 0;
    float a0 = 1, a1 = 0, a2 = 0;
    float x1 = 0, x2 = 0, y1 = 0, y2 = 0;  // State variables
};
```

### 2. Efficient Interpolation (Resampling/Pitch Shifting)

```cpp
// Linear interpolation (fast, acceptable quality)
float linearInterpolate(const float* buffer, float position)
{
    int index = static_cast<int>(position);
    float frac = position - index;

    return buffer[index] * (1.0f - frac) + buffer[index + 1] * frac;
}

// Cubic interpolation (slower, better quality)
float cubicInterpolate(const float* buffer, float position)
{
    int index = static_cast<int>(position);
    float frac = position - index;

    float y0 = buffer[index - 1];
    float y1 = buffer[index];
    float y2 = buffer[index + 1];
    float y3 = buffer[index + 2];

    float a0 = y3 - y2 - y0 + y1;
    float a1 = y0 - y1 - a0;
    float a2 = y2 - y0;
    float a3 = y1;

    return a0 * frac * frac * frac + a1 * frac * frac + a2 * frac + a3;
}
```

---

## 📊 Performance Profiling & Optimization

### Measuring Audio Thread Performance

```cpp
class PerformanceMonitor
{
public:
    void startMeasurement()
    {
        startTime = std::chrono::high_resolution_clock::now();
    }

    double stopMeasurement()
    {
        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
            endTime - startTime
        );
        return duration.count() / 1000.0;  // Convert to milliseconds
    }

private:
    std::chrono::high_resolution_clock::time_point startTime;
};

// Usage in processBlock
void processBlock(float* buffer, int numSamples)
{
    static PerformanceMonitor monitor;
    monitor.startMeasurement();

    // ... DSP code ...

    double elapsedMs = monitor.stopMeasurement();

    // Log if processing took too long
    if (elapsedMs > 1.0)  // > 1ms warning threshold
    {
        // Send to non-real-time thread for logging
        logWarning("Audio processing took " + std::to_string(elapsedMs) + "ms");
    }
}
```

### CPU Usage Targets
- **< 20%:** Single core usage at minimum buffer size (128 samples)
- **< 50%:** Headroom for system overhead
- **< 80%:** Maximum safe usage (leaves room for spikes)

---

## 🔧 Platform-Specific Optimizations

### macOS: CoreAudio Best Practices

```cpp
#include <CoreAudio/CoreAudio.h>

// Set thread priority to real-time
void setRealtimePriority()
{
    thread_time_constraint_policy_data_t policy;
    policy.period = 2902; // Audio buffer period (e.g., 128 samples @ 44.1kHz)
    policy.computation = 1451; // 50% of period
    policy.constraint = 2902;
    policy.preemptible = true;

    thread_policy_set(pthread_mach_thread_np(pthread_self()),
                      THREAD_TIME_CONSTRAINT_POLICY,
                      (thread_policy_t)&policy,
                      THREAD_TIME_CONSTRAINT_POLICY_COUNT);
}
```

### Windows: ASIO & WASAPI

**ASIO** (Steinberg - lowest latency)
- Direct hardware access
- Bypass Windows audio mixing
- Download SDK: https://www.steinberg.net/en/company/developers.html

**WASAPI Exclusive Mode**
- Built into Windows 10/11
- Lower latency than shared mode
- Use with JUCE's `AudioDeviceManager`

### Linux: ALSA & JACK

**JACK** (Professional audio)
- System-wide low-latency routing
- Sample-accurate synchronization
- Connect multiple audio apps

```bash
# Install JACK
sudo apt-get install jackd2

# Start JACK server (128 sample buffer @ 48kHz)
jackd -d alsa -r 48000 -p 128
```

---

## 🎯 Performia-Specific DSP Requirements

### 1. Beat Tracking (Real-Time)

**Efficient Approach:**
```cpp
class RealtimeBeatTracker
{
public:
    void process(const float* audioBuffer, int numSamples)
    {
        // 1. Onset detection (energy-based)
        float energy = calculateEnergy(audioBuffer, numSamples);

        // 2. Adaptive threshold
        if (energy > threshold) {
            onsetDetected(getCurrentTime());
        }

        // 3. Update threshold (exponential smoothing)
        threshold = 0.95f * threshold + 0.05f * energy;
    }

private:
    float calculateEnergy(const float* buffer, int numSamples)
    {
        float sum = 0.0f;
        for (int i = 0; i < numSamples; ++i)
            sum += buffer[i] * buffer[i];

        return sum / numSamples;  // Mean squared energy
    }

    float threshold = 0.01f;
};
```

### 2. Pitch Detection (Low-Latency)

**YIN Algorithm** (Efficient, accurate)
```cpp
float detectPitch(const float* buffer, int numSamples, float sampleRate)
{
    const int minLag = sampleRate / 1000;  // ~1000 Hz max
    const int maxLag = sampleRate / 50;    // ~50 Hz min

    std::vector<float> diff(maxLag + 1);

    // Difference function
    for (int lag = minLag; lag <= maxLag; ++lag) {
        float sum = 0.0f;
        for (int i = 0; i < numSamples - lag; ++i) {
            float delta = buffer[i] - buffer[i + lag];
            sum += delta * delta;
        }
        diff[lag] = sum;
    }

    // Find first minimum
    for (int lag = minLag; lag <= maxLag; ++lag) {
        if (diff[lag] < 0.1f && diff[lag] < diff[lag - 1]) {
            return sampleRate / static_cast<float>(lag);
        }
    }

    return 0.0f;  // No pitch detected
}
```

### 3. Tempo Following (Adaptive)

**Sync to Song Map:**
```cpp
class TempoFollower
{
public:
    void setSongMapTempo(float bpm) {
        expectedBeatInterval = 60.0f / bpm;
    }

    void onBeatDetected(double currentTime)
    {
        if (lastBeatTime > 0.0) {
            float actualInterval = currentTime - lastBeatTime;

            // Measure deviation from expected
            float ratio = actualInterval / expectedBeatInterval;

            // Update tempo estimate (Kalman filter-like)
            estimatedTempo = 0.9f * estimatedTempo + 0.1f * (60.0f / actualInterval);
        }

        lastBeatTime = currentTime;
    }

    float getTempoRatio() const {
        return estimatedTempo / (60.0f / expectedBeatInterval);
    }

private:
    float expectedBeatInterval = 0.5f;  // 120 BPM default
    float estimatedTempo = 120.0f;
    double lastBeatTime = 0.0;
};
```

---

## 🚨 Common Pitfalls & Debugging

### Issue: Denormal Numbers (CPU Spike)

**Problem:** Very small floating-point numbers cause CPU slowdown

**Solution:**
```cpp
// Method 1: Set flush-to-zero (FTZ) mode
#include <xmmintrin.h>
_MM_SET_FLUSH_ZERO_MODE(_MM_FLUSH_ZERO_ON);

// Method 2: Add DC offset (JUCE)
juce::ScopedNoDenormals noDenormals;

// Method 3: Manual clamping
if (std::abs(value) < 1e-15f)
    value = 0.0f;
```

### Issue: Priority Inversion

**Problem:** High-priority audio thread blocked by low-priority thread

**Solution:**
```cpp
// Set audio thread to real-time priority
#include <pthread.h>

void setRealtimePriority()
{
    struct sched_param param;
    param.sched_priority = sched_get_priority_max(SCHED_FIFO);
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
}
```

---

## 📚 Essential Libraries & Tools

### DSP Libraries (C++)
1. **JUCE** - Best all-around, cross-platform
2. **PortAudio** - Low-level audio I/O
3. **SoundTouch** - Pitch/tempo shifting
4. **Rubber Band** - High-quality time-stretching

### Profiling Tools
- **Instruments** (macOS) - Xcode profiler
- **perf** (Linux) - CPU profiling
- **Tracy Profiler** - Real-time profiler for games/audio
- **Superluminal** (Windows) - Low-overhead profiler

### Testing
```cpp
// Unit test for latency
TEST(AudioProcessor, MeetsLatencyTarget)
{
    AudioProcessor proc;
    float buffer[128];

    auto start = std::chrono::high_resolution_clock::now();
    proc.processBlock(buffer, 128);
    auto end = std::chrono::high_resolution_clock::now();

    auto durationMs = std::chrono::duration_cast<std::chrono::microseconds>(
        end - start
    ).count() / 1000.0;

    EXPECT_LT(durationMs, 1.0);  // Must complete in < 1ms
}
```

---

## 🎯 Next Steps for Performia

1. **Implement JUCE audio engine** with < 10ms total latency
2. **Port Python beat tracking** to C++ (JUCE DSP)
3. **Build real-time tempo follower** (sync to Song Map)
4. **Profile and optimize** with Instruments/perf
5. **Test on target hardware** (Mac, Windows, Linux)

---

**Key References:**
- JUCE 7 Benchmarks (2025): https://markaicode.com/cpp-audio-processing-juce-7-benchmarks-2025/
- CppCon 2025: Contemporary C++ for Low-Latency Systems
- Ross Bencina's "Real-Time Audio Programming 101"
