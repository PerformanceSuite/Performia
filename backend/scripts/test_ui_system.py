#!/usr/bin/env python3
"""
Test script for UI Improvement System

Verifies that all components are properly configured and can be instantiated.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_project_structure():
    """Test that all required files exist"""
    print("🔍 Testing Project Structure...")

    project_root = Path(__file__).parent.parent.parent
    required_files = [
        ".claude/agents/ui-design-agent.md",
        ".claude/agents/ui-implementation-agent.md",
        ".claude/agents/ui-evaluation-agent.md",
        ".claude/agents/ui-orchestrator-agent.md",
        "backend/scripts/ui_improvement_orchestrator.py",
        "backend/scripts/screenshot_capture.py",
        "backend/scripts/design_evaluation.py",
        "backend/config/ui_scoring_rubric.json",
        "frontend/App.tsx",
    ]

    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NOT FOUND")
            all_exist = False

    return all_exist


def test_rubric_loading():
    """Test that scoring rubric can be loaded"""
    print("\n🔍 Testing Scoring Rubric...")

    try:
        from scripts.design_evaluation import DesignEvaluator

        project_root = Path(__file__).parent.parent.parent
        rubric_path = project_root / "backend/config/ui_scoring_rubric.json"

        evaluator = DesignEvaluator(str(rubric_path))

        # Check dimensions
        expected_dimensions = [
            "visual_hierarchy",
            "typography",
            "color_contrast",
            "spacing_layout",
            "component_design",
            "animation_interaction",
            "accessibility",
            "overall_aesthetic"
        ]

        all_present = True
        for dimension in expected_dimensions:
            if dimension in evaluator.rubric:
                print(f"   ✅ {dimension} (weight: {evaluator.rubric[dimension]['weight']}x)")
            else:
                print(f"   ❌ {dimension} - NOT FOUND")
                all_present = False

        return all_present

    except Exception as e:
        print(f"   ❌ Error loading rubric: {e}")
        return False


def test_orchestrator_instantiation():
    """Test that orchestrator can be instantiated"""
    print("\n🔍 Testing Orchestrator Instantiation...")

    try:
        from scripts.ui_improvement_orchestrator import UIImprovementOrchestrator

        project_root = Path(__file__).parent.parent.parent
        orchestrator = UIImprovementOrchestrator(
            target_score=8.5,
            max_iterations=5,
            project_root=project_root
        )

        print(f"   ✅ Orchestrator created")
        print(f"   ✅ Target score: {orchestrator.target_score}")
        print(f"   ✅ Max iterations: {orchestrator.max_iterations}")
        print(f"   ✅ Project root: {orchestrator.project_root}")

        return True

    except Exception as e:
        print(f"   ❌ Error instantiating orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_screenshot_capture():
    """Test screenshot capture module"""
    print("\n🔍 Testing Screenshot Capture...")

    try:
        from scripts.screenshot_capture import ScreenshotCapture

        project_root = Path(__file__).parent.parent.parent
        capture = ScreenshotCapture(str(project_root))

        print(f"   ✅ ScreenshotCapture created")
        print(f"   ✅ Frontend URL: {capture.frontend_url}")
        print(f"   ✅ Upload URL: {capture.upload_url}")

        return True

    except Exception as e:
        print(f"   ❌ Error with screenshot capture: {e}")
        return False


def test_evaluation_logic():
    """Test evaluation logic"""
    print("\n🔍 Testing Evaluation Logic...")

    try:
        from scripts.design_evaluation import DesignEvaluator
        import asyncio

        project_root = Path(__file__).parent.parent.parent
        rubric_path = project_root / "backend/config/ui_scoring_rubric.json"

        evaluator = DesignEvaluator(str(rubric_path))

        # Test composite score calculation
        test_scores = {
            "visual_hierarchy": 7.0,
            "typography": 7.5,
            "color_contrast": 8.0,
            "spacing_layout": 6.5,
            "component_design": 7.0,
            "animation_interaction": 7.5,
            "accessibility": 6.0,
            "overall_aesthetic": 7.0
        }

        composite = evaluator.calculate_composite_score(test_scores)
        print(f"   ✅ Composite score calculation: {composite:.2f}/10")

        # Test evaluation (async)
        async def test_eval():
            evaluation = await evaluator.evaluate_screenshot("test.png")
            return evaluation

        evaluation = asyncio.run(test_eval())
        print(f"   ✅ Evaluation structure: {list(evaluation.keys())}")
        print(f"   ✅ Includes composite_score: {evaluation['composite_score']:.2f}")

        return True

    except Exception as e:
        print(f"   ❌ Error with evaluation logic: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_specifications():
    """Test that agent specifications are comprehensive"""
    print("\n🔍 Testing Agent Specifications...")

    project_root = Path(__file__).parent.parent.parent
    agents = [
        "ui-design-agent.md",
        "ui-implementation-agent.md",
        "ui-evaluation-agent.md",
        "ui-orchestrator-agent.md"
    ]

    all_valid = True
    for agent in agents:
        agent_path = project_root / ".claude/agents" / agent
        if agent_path.exists():
            content = agent_path.read_text()
            word_count = len(content.split())
            print(f"   ✅ {agent} ({word_count} words)")

            # Check for key sections
            key_sections = ["Role", "Responsibilities", "Process"]
            missing_sections = [s for s in key_sections if s not in content]
            if missing_sections:
                print(f"      ⚠️  Missing sections: {missing_sections}")
        else:
            print(f"   ❌ {agent} - NOT FOUND")
            all_valid = False

    return all_valid


def main():
    """Run all tests"""
    print("="*70)
    print("UI IMPROVEMENT SYSTEM - TEST SUITE")
    print("="*70)

    tests = [
        ("Project Structure", test_project_structure),
        ("Scoring Rubric", test_rubric_loading),
        ("Orchestrator", test_orchestrator_instantiation),
        ("Screenshot Capture", test_screenshot_capture),
        ("Evaluation Logic", test_evaluation_logic),
        ("Agent Specifications", test_agent_specifications),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} FAILED with exception: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Start frontend dev server: cd frontend && npm run dev")
        print("2. Run orchestrator: python ui_improvement_orchestrator.py")
        print("3. Review output in: frontend/design_iterations/")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before running system.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
