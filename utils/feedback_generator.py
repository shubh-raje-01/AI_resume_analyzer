from typing import List, Dict


def generate_ats_feedback(
        ats_score: int,
        missing_core: List[str],
        missing_optional: List[str],
        missing_sections: List[str]
) -> List[str]:
    """
    Generate ATS-specific feedback.
    """
    feedback = []

    # Overall ATS assessment
    if ats_score >= 80:
        feedback.append("✅ Excellent ATS compatibility! Your resume is well-optimized.")
    elif ats_score >= 60:
        feedback.append("✓ Good ATS compatibility with room for improvement.")
    elif ats_score >= 40:
        feedback.append("⚠ Fair ATS compatibility. Several improvements needed.")
    else:
        feedback.append("❌ Low ATS compatibility. Significant revisions required.")

    # Core skills feedback
    if missing_core:
        feedback.append(
            f"🎯 High Priority: Add these critical skills - {', '.join(missing_core[:5])}"
        )

    # Optional skills feedback
    if missing_optional:
        feedback.append(
            f"💡 Recommended: Consider adding - {', '.join(missing_optional[:3])}"
        )

    # Section feedback
    if missing_sections:
        feedback.append(
            f"📋 Missing Sections: {', '.join(missing_sections)}"
        )

    return feedback


def generate_skill_feedback(
        total_skills: int,
        missing_skills: List[str],
        skill_strength: str
) -> List[str]:
    """Generate skill-related feedback."""
    feedback = []

    if skill_strength == "Strong":
        feedback.append(f"💪 Strong skill set with {total_skills} skills identified")
    elif skill_strength == "Good":
        feedback.append(f"👍 Good skill coverage with {total_skills} skills")
    else:
        feedback.append(f"📚 Expand your skill set (currently {total_skills} skills)")

    if missing_skills:
        feedback.append(f"Add these in-demand skills: {', '.join(missing_skills[:5])}")

    return feedback


def generate_content_feedback(
        quality_score: float,
        weaknesses: List[str]
) -> List[str]:
    """Generate content quality feedback."""
    feedback = []

    if quality_score >= 80:
        feedback.append("✨ Excellent content quality!")
    elif quality_score >= 60:
        feedback.append("Good content with minor improvements needed")
    else:
        feedback.append("Content needs improvement")

    for weakness in weaknesses:
        feedback.append(f"⚠ {weakness}")

    return feedback


def generate_comprehensive_feedback(analysis_results: Dict) -> Dict[str, List[str]]:
    """
    Generate comprehensive feedback from all analysis results.
    """
    return {
        'strengths': extract_strengths(analysis_results),
        'improvements': extract_improvements(analysis_results),
        'priority_actions': extract_priority_actions(analysis_results),
        'tips': extract_tips(analysis_results)
    }


def extract_strengths(results: Dict) -> List[str]:
    """Extract strengths from analysis."""
    strengths = []

    if results.get('ats_score', 0) >= 70:
        strengths.append("Strong ATS compatibility")

    if results.get('skills_count', 0) >= 10:
        strengths.append("Good skill coverage")

    if results.get('content_quality', 0) >= 70:
        strengths.append("High-quality content")

    return strengths


def extract_improvements(results: Dict) -> List[str]:
    """Extract improvement areas."""
    improvements = []

    if results.get('ats_score', 0) < 60:
        improvements.append("Improve ATS optimization")

    if results.get('skills_count', 0) < 8:
        improvements.append("Add more relevant skills")

    return improvements


def extract_priority_actions(results: Dict) -> List[str]:
    """Extract priority actions."""
    actions = []

    missing_core = results.get('missing_core_skills', [])
    if missing_core:
        actions.append(f"Add: {', '.join(missing_core[:3])}")

    if results.get('ats_score', 0) < 50:
        actions.append("Revise for ATS compatibility")

    return actions[:5]


def extract_tips(results: Dict) -> List[str]:
    """Extract helpful tips."""
    return [
        "Use action verbs to start bullet points",
        "Quantify achievements with numbers",
        "Tailor resume to job description",
        "Keep formatting simple and clean",
        "Proofread for errors"
    ]