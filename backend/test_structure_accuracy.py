#!/usr/bin/env python3
"""Comprehensive accuracy testing for structure detection service."""
import json
import sys
import os
import time
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.structure.structure_detection import detect_structure


# Ground truth data for test files
# Format: {"file": "path", "duration": float, "sections": [{"start": float, "end": float, "label": str}]}
GROUND_TRUTH = {
    "test_music.wav": {
        "duration": 8.0,
        "sections": [
            {"start": 0.0, "end": 8.0, "label": "intro"}
        ]
    },
    "test_3min.wav": {
        "duration": 180.0,
        "sections": [
            # Manual annotation based on listening to the file
            # This is a placeholder - ideally we'd have actual ground truth
            {"start": 0.0, "end": 20.0, "label": "intro"},
            {"start": 20.0, "end": 45.0, "label": "verse"},
            {"start": 45.0, "end": 60.0, "label": "chorus"},
            {"start": 60.0, "end": 75.0, "label": "verse"},
            {"start": 75.0, "end": 90.0, "label": "chorus"},
            {"start": 90.0, "end": 110.0, "label": "bridge"},
            {"start": 110.0, "end": 135.0, "label": "chorus"},
            {"start": 135.0, "end": 180.0, "label": "outro"}
        ]
    }
}


def compute_boundary_metrics(
    detected: List[Dict],
    ground_truth: List[Dict],
    tolerance: float = 2.0
) -> Tuple[float, float, float]:
    """
    Compute precision, recall, and F1 score for boundary detection.

    Args:
        detected: Detected sections
        ground_truth: Ground truth sections
        tolerance: Tolerance in seconds for matching boundaries

    Returns:
        Tuple of (precision, recall, f1)
    """
    # Extract boundaries (start times, excluding 0.0)
    detected_boundaries = sorted(set([s["start"] for s in detected if s["start"] > 0.1]))
    gt_boundaries = sorted(set([s["start"] for s in ground_truth if s["start"] > 0.1]))

    if len(detected_boundaries) == 0 or len(gt_boundaries) == 0:
        return 0.0, 0.0, 0.0

    # True positives: detected boundaries within tolerance of GT
    true_positives = 0
    for det_b in detected_boundaries:
        if any(abs(det_b - gt_b) <= tolerance for gt_b in gt_boundaries):
            true_positives += 1

    # False positives: detected boundaries with no nearby GT
    false_positives = len(detected_boundaries) - true_positives

    # False negatives: GT boundaries with no nearby detection
    false_negatives = 0
    for gt_b in gt_boundaries:
        if not any(abs(det_b - gt_b) <= tolerance for det_b in detected_boundaries):
            false_negatives += 1

    # Compute metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


def compute_label_accuracy(
    detected: List[Dict],
    ground_truth: List[Dict],
    tolerance: float = 2.0
) -> float:
    """
    Compute section label classification accuracy.

    For each ground truth section, find overlapping detected section
    and check if labels match.

    Args:
        detected: Detected sections
        ground_truth: Ground truth sections
        tolerance: Tolerance for matching sections

    Returns:
        Accuracy (0.0 to 1.0)
    """
    if len(ground_truth) == 0:
        return 0.0

    correct = 0
    total = len(ground_truth)

    for gt_section in ground_truth:
        gt_start = gt_section["start"]
        gt_end = gt_section["end"]
        gt_label = gt_section["label"]

        # Find overlapping detected section
        best_overlap = 0.0
        best_label = None

        for det_section in detected:
            det_start = det_section["start"]
            det_end = det_section["end"]

            # Compute overlap
            overlap_start = max(gt_start, det_start)
            overlap_end = min(gt_end, det_end)
            overlap = max(0, overlap_end - overlap_start)

            if overlap > best_overlap:
                best_overlap = overlap
                best_label = det_section["label"]

        # Check if label matches
        if best_label == gt_label:
            correct += 1

    return correct / total


def test_single_file(
    audio_path: str,
    ground_truth: Dict,
    tolerance: float = 2.0
) -> Dict:
    """Test structure detection on a single file."""
    print(f"\n{'='*60}")
    print(f"Testing: {audio_path}")
    print(f"{'='*60}")

    # Run detection
    start_time = time.time()
    detected = detect_structure(audio_path)
    elapsed = time.time() - start_time

    # Compute metrics
    precision, recall, f1 = compute_boundary_metrics(
        detected,
        ground_truth["sections"],
        tolerance
    )

    label_accuracy = compute_label_accuracy(
        detected,
        ground_truth["sections"],
        tolerance
    )

    # Print results
    print(f"\nDetected {len(detected)} sections in {elapsed:.3f}s")
    print(f"\nDetected sections:")
    for i, section in enumerate(detected):
        print(f"  {i+1}. {section['start']:6.2f}s - {section['end']:6.2f}s  {section['label']:8s}  (conf: {section.get('confidence', 0.0):.2f})")

    print(f"\nGround truth sections:")
    for i, section in enumerate(ground_truth["sections"]):
        print(f"  {i+1}. {section['start']:6.2f}s - {section['end']:6.2f}s  {section['label']:8s}")

    print(f"\nBoundary Detection (tolerance={tolerance}s):")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall:    {recall:.3f}")
    print(f"  F1 Score:  {f1:.3f}")

    print(f"\nSection Label Accuracy: {label_accuracy:.3f}")

    # Determine pass/fail
    boundary_pass = f1 >= 0.70
    label_pass = label_accuracy >= 0.60
    perf_pass = elapsed < 15.0  # <15s for 3-minute song

    print(f"\nResults:")
    print(f"  Boundary Detection: {'PASS' if boundary_pass else 'FAIL'} (F1 >= 0.70: {f1:.3f})")
    print(f"  Label Accuracy:     {'PASS' if label_pass else 'FAIL'} (>= 0.60: {label_accuracy:.3f})")
    print(f"  Performance:        {'PASS' if perf_pass else 'FAIL'} (<15s: {elapsed:.3f}s)")

    return {
        "file": audio_path,
        "elapsed": elapsed,
        "boundary_precision": precision,
        "boundary_recall": recall,
        "boundary_f1": f1,
        "label_accuracy": label_accuracy,
        "detected_sections": len(detected),
        "gt_sections": len(ground_truth["sections"]),
        "boundary_pass": boundary_pass,
        "label_pass": label_pass,
        "performance_pass": perf_pass
    }


def test_edge_cases():
    """Test edge cases."""
    print(f"\n{'='*60}")
    print("Testing Edge Cases")
    print(f"{'='*60}")

    results = []

    # Test very short file
    print("\n1. Very short file (8s):")
    try:
        detected = detect_structure("test_music.wav")
        print(f"   SUCCESS: Detected {len(detected)} sections")
        results.append(("Short file", True, len(detected)))
    except Exception as e:
        print(f"   FAIL: {e}")
        results.append(("Short file", False, str(e)))

    # Test with invalid input
    print("\n2. Invalid file:")
    try:
        detected = detect_structure("nonexistent.wav")
        print(f"   FAIL: Should have raised exception")
        results.append(("Invalid file", False, "No exception raised"))
    except Exception as e:
        print(f"   SUCCESS: Correctly raised exception: {type(e).__name__}")
        results.append(("Invalid file", True, type(e).__name__))

    return results


def main():
    """Run comprehensive structure detection tests."""
    print("="*60)
    print("STRUCTURE DETECTION COMPREHENSIVE TEST SUITE")
    print("="*60)

    all_results = []

    # Test each file with ground truth
    for filename, gt_data in GROUND_TRUTH.items():
        filepath = os.path.join(os.path.dirname(__file__), filename)

        if not os.path.exists(filepath):
            print(f"\nWARNING: Test file not found: {filepath}")
            continue

        result = test_single_file(filepath, gt_data, tolerance=2.0)
        all_results.append(result)

    # Test edge cases
    edge_results = test_edge_cases()

    # Summary report
    print(f"\n{'='*60}")
    print("SUMMARY REPORT")
    print(f"{'='*60}")

    if len(all_results) > 0:
        avg_f1 = np.mean([r["boundary_f1"] for r in all_results])
        avg_accuracy = np.mean([r["label_accuracy"] for r in all_results])
        avg_time = np.mean([r["elapsed"] for r in all_results])

        boundary_pass_rate = sum([r["boundary_pass"] for r in all_results]) / len(all_results)
        label_pass_rate = sum([r["label_pass"] for r in all_results]) / len(all_results)
        perf_pass_rate = sum([r["performance_pass"] for r in all_results]) / len(all_results)

        print(f"\nAggregate Metrics:")
        print(f"  Average Boundary F1:       {avg_f1:.3f}")
        print(f"  Average Label Accuracy:    {avg_accuracy:.3f}")
        print(f"  Average Processing Time:   {avg_time:.3f}s")

        print(f"\nPass Rates:")
        print(f"  Boundary Detection: {boundary_pass_rate*100:.0f}% ({sum([r['boundary_pass'] for r in all_results])}/{len(all_results)})")
        print(f"  Label Accuracy:     {label_pass_rate*100:.0f}% ({sum([r['label_pass'] for r in all_results])}/{len(all_results)})")
        print(f"  Performance:        {perf_pass_rate*100:.0f}% ({sum([r['performance_pass'] for r in all_results])}/{len(all_results)})")

        print(f"\nEdge Cases:")
        for name, passed, info in edge_results:
            status = "PASS" if passed else "FAIL"
            print(f"  {name:20s} {status:4s}  ({info})")

        # Overall assessment
        overall_pass = (
            avg_f1 >= 0.70 and
            avg_accuracy >= 0.60 and
            perf_pass_rate >= 0.8
        )

        print(f"\n{'='*60}")
        print(f"OVERALL ASSESSMENT: {'PASS' if overall_pass else 'NEEDS IMPROVEMENT'}")
        print(f"{'='*60}")

        if overall_pass:
            print("\nProduction Readiness: READY")
            print("The structure detection service meets all acceptance criteria.")
        else:
            print("\nProduction Readiness: NOT READY")
            print("\nIssues to address:")
            if avg_f1 < 0.70:
                print(f"  - Boundary detection F1 ({avg_f1:.3f}) below target (0.70)")
            if avg_accuracy < 0.60:
                print(f"  - Label accuracy ({avg_accuracy:.3f}) below target (0.60)")
            if perf_pass_rate < 0.8:
                print(f"  - Performance issues on {(1-perf_pass_rate)*100:.0f}% of test cases")

        # Save detailed results
        output_file = "test_structure_accuracy_results.json"
        with open(output_file, 'w') as f:
            json.dump({
                "summary": {
                    "avg_boundary_f1": float(avg_f1),
                    "avg_label_accuracy": float(avg_accuracy),
                    "avg_processing_time": float(avg_time),
                    "boundary_pass_rate": float(boundary_pass_rate),
                    "label_pass_rate": float(label_pass_rate),
                    "performance_pass_rate": float(perf_pass_rate),
                    "overall_pass": bool(overall_pass)
                },
                "detailed_results": [{k: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for k, v in r.items()} for r in all_results],
                "edge_cases": [{"name": name, "passed": bool(passed), "info": str(info)} for name, passed, info in edge_results]
            }, f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")

        return 0 if overall_pass else 1
    else:
        print("No test files found!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
