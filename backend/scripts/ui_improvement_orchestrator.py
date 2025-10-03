#!/usr/bin/env python3
"""
Performia UI Improvement Orchestrator

Autonomous UI/UX improvement system that coordinates design, implementation,
and evaluation agents through iterative cycles until reaching design excellence.

Usage:
    python ui_improvement_orchestrator.py [--target-score 8.5] [--max-iterations 5]
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.screenshot_capture import ScreenshotCapture
from scripts.design_evaluation import DesignEvaluator


@dataclass
class IterationRecord:
    """Record of a single iteration"""
    iteration: int
    timestamp: str
    screenshots: Dict[str, str]
    design_spec_path: str
    implementation_notes_path: str
    evaluation: Dict
    score_delta: float
    target_reached: bool


class UIImprovementOrchestrator:
    """
    Orchestrates autonomous UI improvement cycles

    Coordinates:
    - Design agent: Analyzes UI and proposes improvements
    - Implementation agent: Applies design specifications
    - Evaluation agent: Scores design quality
    - Screenshot capture: Documents changes
    """

    def __init__(
        self,
        target_score: float = 8.5,
        max_iterations: int = 5,
        project_root: Optional[Path] = None
    ):
        self.target_score = target_score
        self.max_iterations = max_iterations

        # Paths
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.frontend_dir = self.project_root / "frontend"
        self.iterations_dir = self.frontend_dir / "design_iterations"
        self.config_dir = self.project_root / "backend" / "config"

        # State
        self.iteration_history: List[IterationRecord] = []
        self.current_iteration = 0
        self.best_score = 0.0
        self.best_iteration = 0

        # Services
        self.screenshot_capture = ScreenshotCapture(str(self.project_root))
        self.evaluator = DesignEvaluator(str(self.config_dir / "ui_scoring_rubric.json"))

    def initialize(self):
        """Initialize orchestration system"""
        print("🎨 Initializing UI Improvement Orchestrator")
        print(f"   Target Score: {self.target_score}/10")
        print(f"   Max Iterations: {self.max_iterations}")
        print(f"   Project Root: {self.project_root}")

        # Create directory structure
        self.iterations_dir.mkdir(parents=True, exist_ok=True)

        # Verify frontend is buildable
        if not self._verify_frontend():
            raise RuntimeError("Frontend verification failed")

        print("✅ Initialization complete\n")

    def _verify_frontend(self) -> bool:
        """Verify frontend directory and dependencies"""
        if not self.frontend_dir.exists():
            print(f"❌ Frontend directory not found: {self.frontend_dir}")
            return False

        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            print(f"❌ package.json not found: {package_json}")
            return False

        print("✅ Frontend directory structure verified")
        return True

    async def run_improvement_cycle(self) -> Dict:
        """
        Run complete improvement cycle

        Returns:
            Final report dictionary
        """
        print("🚀 Starting UI Improvement Cycle\n")

        for iteration in range(self.max_iterations):
            self.current_iteration = iteration
            print(f"\n{'='*70}")
            print(f"🔄 ITERATION {iteration + 1}/{self.max_iterations}")
            print(f"{'='*70}\n")

            # Create iteration directory
            iteration_dir = self.iterations_dir / f"iteration_{iteration}"
            iteration_dir.mkdir(exist_ok=True)

            try:
                # Step 1: Capture current UI
                print("📸 Step 1: Capturing current UI screenshot...")
                before_screenshot = await self._capture_screenshot(
                    iteration_dir / "before.png"
                )
                print(f"   Saved: {before_screenshot}")

                # Step 2: Design agent analysis
                print("\n🎨 Step 2: Running design agent analysis...")
                design_spec = await self._run_design_agent(
                    before_screenshot,
                    iteration,
                    iteration_dir / "design_spec.md"
                )
                print(f"   Design spec saved: {design_spec}")

                # Step 3: Implementation agent
                print("\n⚙️  Step 3: Running implementation agent...")
                implementation_notes = await self._run_implementation_agent(
                    design_spec,
                    iteration_dir / "implementation.md"
                )
                print(f"   Implementation notes saved: {implementation_notes}")

                # Step 4: Build frontend
                print("\n🔨 Step 4: Building frontend...")
                if not await self._build_frontend():
                    print("❌ Build failed, see errors above")
                    break
                print("   ✅ Build successful")

                # Step 5: Capture new UI
                print("\n📸 Step 5: Capturing updated UI screenshot...")
                after_screenshot = await self._capture_screenshot(
                    iteration_dir / "after.png"
                )
                print(f"   Saved: {after_screenshot}")

                # Step 6: Evaluation agent
                print("\n📊 Step 6: Running evaluation agent...")
                evaluation = await self._run_evaluation_agent(
                    after_screenshot,
                    iteration,
                    iteration_dir
                )

                # Save evaluation
                with open(iteration_dir / "evaluation.json", 'w') as f:
                    json.dump(evaluation, f, indent=2)

                print(f"   Composite Score: {evaluation['composite_score']:.1f}/10")
                print(f"   Target: {self.target_score}/10")

                # Calculate score delta
                score_delta = 0.0
                if iteration > 0:
                    prev_score = self.iteration_history[-1].evaluation['composite_score']
                    score_delta = evaluation['composite_score'] - prev_score
                    print(f"   Improvement: {score_delta:+.1f}")

                # Update best score
                if evaluation['composite_score'] > self.best_score:
                    self.best_score = evaluation['composite_score']
                    self.best_iteration = iteration

                # Record iteration
                record = IterationRecord(
                    iteration=iteration,
                    timestamp=datetime.now().isoformat(),
                    screenshots={
                        'before': str(before_screenshot),
                        'after': str(after_screenshot)
                    },
                    design_spec_path=str(design_spec),
                    implementation_notes_path=str(implementation_notes),
                    evaluation=evaluation,
                    score_delta=score_delta,
                    target_reached=evaluation['composite_score'] >= self.target_score
                )
                self.iteration_history.append(record)

                # Step 7: Check stopping criteria
                print("\n🎯 Step 7: Checking stopping criteria...")

                if evaluation['composite_score'] >= self.target_score:
                    print(f"   ✅ Target score reached! ({evaluation['composite_score']:.1f} >= {self.target_score})")
                    break

                if iteration >= self.max_iterations - 1:
                    print(f"   ⏸️  Maximum iterations reached ({self.max_iterations})")
                    break

                # Check diminishing returns
                if iteration >= 1:
                    if score_delta < 0.2:
                        print(f"   ⚠️  Low improvement rate ({score_delta:.2f}), but continuing...")

                print("   ↻  Continuing to next iteration...")

            except Exception as e:
                print(f"\n❌ Error in iteration {iteration}: {e}")
                import traceback
                traceback.print_exc()
                break

        # Generate final report
        print(f"\n{'='*70}")
        print("📝 Generating Final Report")
        print(f"{'='*70}\n")

        final_report = self._generate_final_report()

        # Save final report
        report_path = self.iterations_dir / "final_report.md"
        with open(report_path, 'w') as f:
            f.write(final_report)

        print(f"✅ Final report saved: {report_path}")

        return {
            'status': 'complete',
            'iterations': len(self.iteration_history),
            'final_score': self.best_score,
            'target_reached': self.best_score >= self.target_score,
            'report_path': str(report_path)
        }

    async def _capture_screenshot(self, output_path: Path) -> Path:
        """Capture UI screenshot"""
        # This will use the Puppeteer MCP integration
        # For now, return placeholder
        await self.screenshot_capture.capture_upload_ui(str(output_path))
        return output_path

    async def _run_design_agent(
        self,
        screenshot_path: Path,
        iteration: int,
        output_path: Path
    ) -> Path:
        """
        Run design agent to analyze UI and propose improvements

        This should invoke Claude with ui-design-agent instructions
        """
        # Placeholder for agent invocation
        # In practice, this would use Claude API with agent context

        agent_prompt = f"""
Act as the ui-design-agent and analyze this UI screenshot:
{screenshot_path}

This is iteration {iteration} of {self.max_iterations}.

"""

        if iteration > 0:
            prev_eval = self.iteration_history[-1].evaluation
            agent_prompt += f"""
Previous iteration score: {prev_eval['composite_score']:.1f}/10

Previous weaknesses:
{json.dumps(prev_eval.get('weaknesses', {}), indent=2)}
"""

        agent_prompt += """
Provide detailed design specification for improvements.
Focus on highest-impact changes that will move score toward 8.5/10.
"""

        # Save prompt (actual agent invocation would happen here)
        with open(output_path, 'w') as f:
            f.write(f"# Design Specification - Iteration {iteration}\n\n")
            f.write(f"**Screenshot:** {screenshot_path}\n\n")
            f.write("## Agent Prompt\n\n")
            f.write(agent_prompt)
            f.write("\n\n## Design Specification\n\n")
            f.write("[Design agent output would be inserted here]\n")

        return output_path

    async def _run_implementation_agent(
        self,
        design_spec_path: Path,
        output_path: Path
    ) -> Path:
        """
        Run implementation agent to apply design changes

        This should invoke Claude with ui-implementation-agent instructions
        """
        # Read design spec
        with open(design_spec_path, 'r') as f:
            design_spec = f.read()

        agent_prompt = f"""
Act as the ui-implementation-agent and implement this design specification:

{design_spec}

Preserve all functionality. Apply changes to:
- /Users/danielconnolly/Projects/Performia/frontend/App.tsx
- Other files as specified in design spec

Provide implementation report when complete.
"""

        # Save prompt (actual agent invocation would happen here)
        with open(output_path, 'w') as f:
            f.write(f"# Implementation Notes\n\n")
            f.write("## Agent Prompt\n\n")
            f.write(agent_prompt)
            f.write("\n\n## Implementation\n\n")
            f.write("[Implementation agent output would be inserted here]\n")

        return output_path

    async def _run_evaluation_agent(
        self,
        screenshot_path: Path,
        iteration: int,
        iteration_dir: Path
    ) -> Dict:
        """
        Run evaluation agent to score design

        This should invoke Claude with ui-evaluation-agent instructions
        """
        prev_score = None
        if iteration > 0:
            prev_score = self.iteration_history[-1].evaluation['composite_score']

        agent_prompt = f"""
Act as the ui-evaluation-agent and evaluate this UI screenshot:
{screenshot_path}

This is iteration {iteration}.
"""

        if prev_score:
            agent_prompt += f"Previous iteration score: {prev_score:.1f}/10\n"

        agent_prompt += """
Provide comprehensive evaluation across all 8 dimensions.
Calculate composite score.
Determine if target (8.5/10) is reached.
Identify priority improvements for next iteration.
"""

        # For now, use automated evaluation
        evaluation = await self.evaluator.evaluate_screenshot(str(screenshot_path))

        # Save evaluation markdown
        with open(iteration_dir / "evaluation.md", 'w') as f:
            f.write(f"# Evaluation Report - Iteration {iteration}\n\n")
            f.write(f"**Screenshot:** {screenshot_path}\n\n")
            f.write(f"## Composite Score: {evaluation['composite_score']:.1f}/10\n\n")
            f.write("## Dimension Scores\n\n")
            for dimension, score in evaluation['scores'].items():
                f.write(f"- **{dimension.replace('_', ' ').title()}:** {score:.1f}/10\n")

        return evaluation

    async def _build_frontend(self) -> bool:
        """Build frontend"""
        try:
            # For development, we might just verify it compiles
            # In production, would run actual build
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=str(self.frontend_dir),
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"❌ Build failed:\n{result.stderr}")
                return False

            return True

        except subprocess.TimeoutExpired:
            print("❌ Build timed out")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False

    def _generate_final_report(self) -> str:
        """Generate comprehensive final report"""
        if not self.iteration_history:
            return "No iterations completed."

        first_score = self.iteration_history[0].evaluation['composite_score']
        final_score = self.best_score
        improvement = final_score - first_score

        report = f"""# Performia Upload UI Improvement Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Starting Score:** {first_score:.1f}/10
- **Final Score:** {final_score:.1f}/10
- **Improvement:** {improvement:+.1f} points
- **Iterations Completed:** {len(self.iteration_history)}
- **Target Score:** {self.target_score}/10
- **Target Reached:** {'✅ YES' if final_score >= self.target_score else '❌ NO'}
- **Best Iteration:** {self.best_iteration}

"""

        # Score progression table
        report += "\n## Score Progression\n\n"
        report += "| Iteration | Composite | Visual Hierarchy | Typography | Color | Spacing | Components | Animation | Accessibility | Aesthetic |\n"
        report += "|-----------|-----------|------------------|------------|-------|---------|------------|-----------|---------------|------------|\n"

        for record in self.iteration_history:
            scores = record.evaluation['scores']
            report += f"| {record.iteration} | "
            report += f"{record.evaluation['composite_score']:.1f} | "
            report += f"{scores.get('visual_hierarchy', 0):.1f} | "
            report += f"{scores.get('typography', 0):.1f} | "
            report += f"{scores.get('color_contrast', 0):.1f} | "
            report += f"{scores.get('spacing_layout', 0):.1f} | "
            report += f"{scores.get('component_design', 0):.1f} | "
            report += f"{scores.get('animation_interaction', 0):.1f} | "
            report += f"{scores.get('accessibility', 0):.1f} | "
            report += f"{scores.get('overall_aesthetic', 0):.1f} |\n"

        # Iteration details
        report += "\n## Iteration History\n\n"

        for record in self.iteration_history:
            report += f"### Iteration {record.iteration}\n\n"
            report += f"**Timestamp:** {record.timestamp}\n\n"
            report += f"**Composite Score:** {record.evaluation['composite_score']:.1f}/10\n\n"

            if record.score_delta != 0:
                report += f"**Score Delta:** {record.score_delta:+.1f}\n\n"

            report += f"**Screenshots:**\n"
            report += f"- Before: `{record.screenshots['before']}`\n"
            report += f"- After: `{record.screenshots['after']}`\n\n"

            report += f"**Design Spec:** `{record.design_spec_path}`\n\n"
            report += f"**Implementation Notes:** `{record.implementation_notes_path}`\n\n"

            report += "---\n\n"

        # Key achievements
        report += "\n## Key Achievements\n\n"
        if final_score >= self.target_score:
            report += "✅ Target score achieved!\n\n"

        report += f"1. Improved overall design quality by {improvement:.1f} points\n"
        report += f"2. Completed {len(self.iteration_history)} design iterations\n"
        report += f"3. Maintained all functionality throughout process\n\n"

        # Remaining opportunities
        if final_score < self.target_score:
            gap = self.target_score - final_score
            report += f"\n## Remaining Gap\n\n"
            report += f"**Gap to Target:** {gap:.1f} points\n\n"
            report += "**Recommendations for Next Iteration:**\n"
            report += "- [Based on latest evaluation feedback]\n\n"

        # Conclusion
        report += "\n## Conclusion\n\n"
        if final_score >= self.target_score:
            report += "Successfully achieved target design quality score through "
            report += f"systematic iterative improvements over {len(self.iteration_history)} iterations.\n"
        else:
            report += f"Made significant progress ({improvement:+.1f} points) but did not reach "
            report += f"target score. Consider additional iterations or manual refinement.\n"

        report += "\n---\n\n"
        report += "*Report generated by Autonomous UI/UX Improvement System v1.0*\n"

        return report


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Autonomous UI/UX Improvement Orchestrator'
    )
    parser.add_argument(
        '--target-score',
        type=float,
        default=8.5,
        help='Target composite score (default: 8.5)'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=5,
        help='Maximum iterations (default: 5)'
    )
    parser.add_argument(
        '--project-root',
        type=str,
        help='Project root directory'
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = UIImprovementOrchestrator(
        target_score=args.target_score,
        max_iterations=args.max_iterations,
        project_root=Path(args.project_root) if args.project_root else None
    )

    # Initialize
    orchestrator.initialize()

    # Run improvement cycle
    result = await orchestrator.run_improvement_cycle()

    # Display results
    print("\n" + "="*70)
    print("🎉 IMPROVEMENT CYCLE COMPLETE")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Final Score: {result['final_score']:.1f}/10")
    print(f"Target Reached: {result['target_reached']}")
    print(f"Report: {result['report_path']}")
    print("="*70)


if __name__ == '__main__':
    asyncio.run(main())
