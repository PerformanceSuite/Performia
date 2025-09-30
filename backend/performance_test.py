#!/usr/bin/env python3
"""Performance benchmarking for Song Map pipeline"""

import json
import time
from pathlib import Path

# Test data from complete_test run
test_results = {
    "audio_duration": 8.0,  # seconds
    "total_time": 4.34,     # seconds
    "service_times": {
        "separation": 0.022,
        "beats_key": 1.119,
        "asr": 1.663,
        "chords": 0.953,
        "melody_bass": 1.147,
        "structure": 1.035,
        "packager": 0.525
    }
}

def extrapolate_performance(test_duration, test_time, target_duration):
    """Extrapolate performance to longer audio"""
    # Most services scale linearly with audio duration
    # Packager is O(1) - doesn't depend on audio length
    
    ratio = target_duration / test_duration
    return test_time * ratio

def analyze_performance():
    """Analyze and report performance metrics"""
    
    print("=" * 70)
    print("PERFORMIA BACKEND PIPELINE - PERFORMANCE ANALYSIS")
    print("=" * 70)
    print()
    
    # Current performance
    print("Current Test Results (8-second audio):")
    print(f"  Audio Duration: {test_results['audio_duration']:.1f}s")
    print(f"  Total Pipeline: {test_results['total_time']:.2f}s")
    print(f"  Real-time Ratio: {test_results['total_time'] / test_results['audio_duration']:.2f}x")
    print()
    
    # Service breakdown
    print("Service Breakdown:")
    total_service_time = sum(test_results['service_times'].values())
    for service, duration in sorted(test_results['service_times'].items(), 
                                   key=lambda x: x[1], reverse=True):
        pct = (duration / total_service_time) * 100
        print(f"  {service:12s}: {duration:.3f}s ({pct:5.1f}%)")
    print()
    
    # Extrapolate to 3-minute song (180 seconds)
    target_duration = 180.0
    
    print(f"Extrapolated Performance ({target_duration:.0f}-second / 3-minute song):")
    print()
    
    # Linear scaling services (most services)
    linear_services = ["separation", "beats_key", "asr", "chords", 
                      "melody_bass", "structure"]
    
    # Constant time services
    constant_services = ["packager"]
    
    extrapolated_times = {}
    
    for service in linear_services:
        original = test_results['service_times'][service]
        extrapolated = extrapolate_performance(
            test_results['audio_duration'], 
            original, 
            target_duration
        )
        extrapolated_times[service] = extrapolated
        print(f"  {service:12s}: {original:.2f}s → {extrapolated:.2f}s")
    
    print()
    for service in constant_services:
        original = test_results['service_times'][service]
        extrapolated_times[service] = original
        print(f"  {service:12s}: {original:.2f}s → {original:.2f}s (constant)")
    
    print()
    
    # Calculate total with parallelization
    # Phase 1: separation + beats_key (parallel)
    phase1 = max(extrapolated_times['separation'], extrapolated_times['beats_key'])
    
    # Phase 2: asr + chords + melody_bass (parallel)
    phase2 = max(extrapolated_times['asr'], 
                 extrapolated_times['chords'],
                 extrapolated_times['melody_bass'])
    
    # Phase 3: structure (sequential)
    phase3 = extrapolated_times['structure']
    
    # Phase 4: packager (sequential)
    phase4 = extrapolated_times['packager']
    
    total_extrapolated = phase1 + phase2 + phase3 + phase4
    
    print("Pipeline Phases (with parallelization):")
    print(f"  Phase 1 (parallel): max(separation, beats_key) = {phase1:.2f}s")
    print(f"  Phase 2 (parallel): max(asr, chords, melody_bass) = {phase2:.2f}s")
    print(f"  Phase 3: structure = {phase3:.2f}s")
    print(f"  Phase 4: packager = {phase4:.2f}s")
    print(f"  {'─' * 50}")
    print(f"  Total Estimated Time: {total_extrapolated:.2f}s")
    print()
    
    # Performance targets
    target = 30.0
    status = "✅ PASS" if total_extrapolated <= target else "❌ FAIL"
    
    print("=" * 70)
    print("PERFORMANCE TARGET ASSESSMENT")
    print("=" * 70)
    print(f"  Target: <{target:.0f}s for 3-minute song")
    print(f"  Estimated: {total_extrapolated:.2f}s")
    print(f"  Margin: {target - total_extrapolated:.2f}s")
    print(f"  Status: {status}")
    print()
    
    if total_extrapolated <= target:
        print("  🎉 Target ACHIEVED!")
        print(f"  We're {target - total_extrapolated:.1f}s under budget.")
    else:
        print("  ⚠️  Target MISSED")
        print(f"  We're {total_extrapolated - target:.1f}s over budget.")
        print()
        print("  Optimization opportunities:")
        
        # Find bottlenecks
        bottlenecks = []
        for service in linear_services:
            if extrapolated_times[service] > 5.0:
                bottlenecks.append((service, extrapolated_times[service]))
        
        for service, time in sorted(bottlenecks, key=lambda x: x[1], reverse=True):
            print(f"    - {service}: {time:.2f}s")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    analyze_performance()
