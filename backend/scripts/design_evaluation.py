#!/usr/bin/env python3
"""
Design Evaluation Module

Automated and manual evaluation of UI design quality across multiple dimensions.
Implements the scoring rubric defined for the autonomous UI improvement system.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DimensionScore:
    """Score for a single design dimension"""
    name: str
    score: float
    weight: float
    weighted_score: float
    rationale: str
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]


class DesignEvaluator:
    """Evaluates UI design quality"""

    def __init__(self, rubric_path: str):
        self.rubric_path = Path(rubric_path)
        self.rubric = self._load_rubric()

    def _load_rubric(self) -> Dict:
        """Load scoring rubric"""
        if not self.rubric_path.exists():
            # Return default rubric if file doesn't exist
            return self._get_default_rubric()

        with open(self.rubric_path, 'r') as f:
            return json.load(f)

    def _get_default_rubric(self) -> Dict:
        """Get default scoring rubric"""
        return {
            "visual_hierarchy": {
                "weight": 1.2,
                "criteria": [
                    "Clear primary/secondary/tertiary elements",
                    "Appropriate size scaling",
                    "Effective use of contrast",
                    "Logical flow and grouping"
                ]
            },
            "typography": {
                "weight": 1.0,
                "criteria": [
                    "Readable font sizes (16px+ for body)",
                    "Consistent type scale",
                    "Appropriate line height (1.5-1.8)",
                    "Font weight hierarchy"
                ]
            },
            "color_contrast": {
                "weight": 1.0,
                "criteria": [
                    "WCAG 2.1 AA compliance (4.5:1 normal, 3:1 large)",
                    "Color harmony and balance",
                    "Brand consistency",
                    "Semantic color usage"
                ]
            },
            "spacing_layout": {
                "weight": 1.1,
                "criteria": [
                    "Consistent spacing scale (8px grid)",
                    "Adequate breathing room",
                    "Proper alignment",
                    "Responsive padding"
                ]
            },
            "component_design": {
                "weight": 1.0,
                "criteria": [
                    "Button hierarchy clear",
                    "Interactive states defined",
                    "Touch targets adequate (44x44px)",
                    "Consistent styling"
                ]
            },
            "animation_interaction": {
                "weight": 0.9,
                "criteria": [
                    "Smooth transitions (60fps)",
                    "Appropriate durations (200-300ms)",
                    "Natural easing",
                    "Purposeful motion"
                ]
            },
            "accessibility": {
                "weight": 1.3,
                "criteria": [
                    "WCAG 2.1 AA compliance",
                    "Keyboard navigation",
                    "Focus indicators visible",
                    "Screen reader compatible"
                ]
            },
            "overall_aesthetic": {
                "weight": 1.0,
                "criteria": [
                    "Professional appearance",
                    "Modern feel",
                    "Cohesive design language",
                    "Brand alignment"
                ]
            }
        }

    async def evaluate_screenshot(self, screenshot_path: str) -> Dict:
        """
        Evaluate design from screenshot

        In production, this would use AI vision or manual evaluation.
        For now, returns structured evaluation format.

        Args:
            screenshot_path: Path to screenshot

        Returns:
            Evaluation dictionary with scores and feedback
        """
        # Placeholder scores for demonstration
        # In production, this would analyze the actual screenshot
        dimension_scores = {
            "visual_hierarchy": 6.5,
            "typography": 6.0,
            "color_contrast": 7.0,
            "spacing_layout": 5.5,
            "component_design": 6.5,
            "animation_interaction": 7.0,
            "accessibility": 5.0,
            "overall_aesthetic": 6.0
        }

        # Calculate weighted scores
        weighted_scores = {}
        total_weight = 0
        weighted_sum = 0

        for dimension, score in dimension_scores.items():
            weight = self.rubric[dimension]["weight"]
            weighted_score = score * weight
            weighted_scores[dimension] = weighted_score
            weighted_sum += weighted_score
            total_weight += weight

        # Calculate composite score
        composite_score = weighted_sum / total_weight

        # Generate evaluation
        evaluation = {
            "screenshot_path": screenshot_path,
            "composite_score": composite_score,
            "target_score": 8.5,
            "target_reached": composite_score >= 8.5,
            "scores": dimension_scores,
            "weighted_scores": weighted_scores,
            "dimensions": self._generate_dimension_details(dimension_scores),
            "summary": self._generate_summary(composite_score, dimension_scores),
            "priority_improvements": self._identify_priority_improvements(dimension_scores),
            "strengths": self._identify_strengths(dimension_scores),
            "weaknesses": self._identify_weaknesses(dimension_scores)
        }

        return evaluation

    def _generate_dimension_details(self, scores: Dict[str, float]) -> Dict:
        """Generate detailed analysis for each dimension"""
        details = {}

        for dimension, score in scores.items():
            details[dimension] = {
                "score": score,
                "weight": self.rubric[dimension]["weight"],
                "criteria": self.rubric[dimension]["criteria"],
                "assessment": self._assess_score(score),
                "recommendations": self._get_recommendations(dimension, score)
            }

        return details

    def _assess_score(self, score: float) -> str:
        """Assess score level"""
        if score >= 9.0:
            return "Exceptional"
        elif score >= 8.0:
            return "Excellent"
        elif score >= 7.0:
            return "Good"
        elif score >= 6.0:
            return "Fair"
        elif score >= 4.0:
            return "Needs Improvement"
        else:
            return "Critical Issues"

    def _get_recommendations(self, dimension: str, score: float) -> List[str]:
        """Get recommendations based on dimension and score"""
        recommendations = {
            "visual_hierarchy": [
                "Increase size difference between primary and secondary elements",
                "Use color contrast to establish clear hierarchy",
                "Group related elements with consistent spacing",
                "Create clear visual flow from top to bottom"
            ],
            "typography": [
                "Increase body text to 16px minimum",
                "Establish consistent type scale (e.g., 1.25 ratio)",
                "Set line height to 1.5-1.8 for body text",
                "Use 3-4 font weights maximum for clear hierarchy"
            ],
            "color_contrast": [
                "Ensure 4.5:1 contrast ratio for normal text",
                "Ensure 3:1 contrast ratio for large text",
                "Use color consistently for semantic meaning",
                "Maintain brand color harmony"
            ],
            "spacing_layout": [
                "Implement 8px grid spacing system",
                "Increase padding for better breathing room",
                "Align elements to consistent grid",
                "Use responsive spacing values"
            ],
            "component_design": [
                "Define clear button hierarchy (primary, secondary, tertiary)",
                "Add hover, active, and focus states",
                "Ensure 44x44px minimum touch targets",
                "Maintain consistent border radius and shadows"
            ],
            "animation_interaction": [
                "Add smooth transitions (200-300ms)",
                "Use ease-out easing for natural feel",
                "Implement loading state animations",
                "Ensure 60fps performance"
            ],
            "accessibility": [
                "Ensure WCAG 2.1 AA compliance",
                "Add visible focus indicators",
                "Implement keyboard navigation",
                "Add ARIA labels where needed"
            ],
            "overall_aesthetic": [
                "Refine visual details for polish",
                "Ensure consistent design language",
                "Add subtle micro-interactions",
                "Maintain professional appearance"
            ]
        }

        return recommendations.get(dimension, [])

    def _generate_summary(self, composite_score: float, scores: Dict) -> str:
        """Generate evaluation summary"""
        assessment = self._assess_score(composite_score)

        summary = f"Overall design quality: {assessment} ({composite_score:.1f}/10)\n\n"

        # Identify strong areas
        strong_areas = [dim for dim, score in scores.items() if score >= 7.0]
        if strong_areas:
            summary += "Strong areas: " + ", ".join(strong_areas) + "\n\n"

        # Identify weak areas
        weak_areas = [dim for dim, score in scores.items() if score < 6.0]
        if weak_areas:
            summary += "Areas needing improvement: " + ", ".join(weak_areas) + "\n\n"

        # Target gap
        if composite_score < 8.5:
            gap = 8.5 - composite_score
            summary += f"Gap to target: {gap:.1f} points\n"

        return summary

    def _identify_priority_improvements(self, scores: Dict) -> List[Dict]:
        """Identify highest priority improvements"""
        # Calculate impact of improving each dimension
        improvements = []

        for dimension, score in scores.items():
            if score < 8.5:
                weight = self.rubric[dimension]["weight"]
                potential_gain = (8.5 - score) * weight
                improvements.append({
                    "dimension": dimension,
                    "current_score": score,
                    "potential_gain": potential_gain,
                    "priority": "Critical" if score < 6.0 else "Important" if score < 7.5 else "Enhancement"
                })

        # Sort by potential gain
        improvements.sort(key=lambda x: x["potential_gain"], reverse=True)

        return improvements[:5]  # Top 5

    def _identify_strengths(self, scores: Dict) -> List[str]:
        """Identify design strengths"""
        strengths = []

        for dimension, score in scores.items():
            if score >= 7.0:
                strengths.append(f"{dimension.replace('_', ' ').title()}: {score:.1f}/10")

        return strengths

    def _identify_weaknesses(self, scores: Dict) -> List[str]:
        """Identify design weaknesses"""
        weaknesses = []

        for dimension, score in scores.items():
            if score < 6.0:
                weaknesses.append(f"{dimension.replace('_', ' ').title()}: {score:.1f}/10")

        return weaknesses

    def calculate_composite_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted composite score"""
        weighted_sum = 0
        total_weight = 0

        for dimension, score in scores.items():
            weight = self.rubric[dimension]["weight"]
            weighted_sum += score * weight
            total_weight += weight

        return weighted_sum / total_weight

    def format_evaluation_report(self, evaluation: Dict) -> str:
        """Format evaluation as markdown report"""
        report = f"""# UI Design Evaluation Report

## Composite Score: {evaluation['composite_score']:.1f}/10

**Target:** {evaluation['target_score']}/10
**Status:** {'✅ Target Reached' if evaluation['target_reached'] else '❌ Continue Iterations'}

## Score Summary

"""

        # Dimension scores table
        report += "| Dimension | Score | Weight | Assessment |\n"
        report += "|-----------|-------|--------|------------|\n"

        for dimension, details in evaluation['dimensions'].items():
            report += f"| {dimension.replace('_', ' ').title()} | "
            report += f"{details['score']:.1f} | "
            report += f"{details['weight']}x | "
            report += f"{details['assessment']} |\n"

        # Summary
        report += f"\n## Summary\n\n{evaluation['summary']}\n"

        # Strengths
        if evaluation['strengths']:
            report += "\n## Strengths\n\n"
            for strength in evaluation['strengths']:
                report += f"- {strength}\n"

        # Weaknesses
        if evaluation['weaknesses']:
            report += "\n## Weaknesses\n\n"
            for weakness in evaluation['weaknesses']:
                report += f"- {weakness}\n"

        # Priority improvements
        report += "\n## Priority Improvements\n\n"
        for improvement in evaluation['priority_improvements']:
            report += f"### {improvement['dimension'].replace('_', ' ').title()} "
            report += f"({improvement['priority']})\n\n"
            report += f"Current Score: {improvement['current_score']:.1f}/10\n"
            report += f"Potential Gain: {improvement['potential_gain']:.2f} weighted points\n\n"

        return report


# Example usage
async def main():
    """Example evaluation"""
    evaluator = DesignEvaluator("./config/ui_scoring_rubric.json")

    evaluation = await evaluator.evaluate_screenshot("./screenshots/upload.png")

    print(evaluator.format_evaluation_report(evaluation))


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
