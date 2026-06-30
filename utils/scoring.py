from typing import Dict
import logging

logger = logging.getLogger(__name__)


def calculate_resume_score(
        skills: list,
        cleaned_text: str,
        has_experience: bool = True,
        has_education: bool = True
) -> int:
    """
    Calculate overall resume score (0-100).
    """
    score = 0

    # 1. Skill Coverage (max 40 points)
    skill_score = min(len(skills) * 3, 40)
    score += skill_score

    # 2. Resume Length Quality (max 20 points)
    word_count = len(cleaned_text.split())
    if 300 <= word_count <= 1500:
        score += 20
    elif 200 <= word_count < 300 or 1500 < word_count <= 2000:
        score += 15
    elif 150 <= word_count < 200 or 2000 < word_count <= 2500:
        score += 10
    else:
        score += 5

    # 3. Experience Indicators (max 20 points)
    if has_experience:
        experience_keywords = [
            'experience', 'project', 'worked', 'developed',
            'implemented', 'managed', 'led', 'created'
        ]
        exp_hits = sum(1 for k in experience_keywords if k in cleaned_text.lower())
        score += min(exp_hits * 3, 20)

    # 4. Education (max 10 points)
    if has_education:
        score += 10

    # 5. Professional Keywords (max 10 points)
    professional_keywords = [
        'achievement', 'certification', 'certified', 'award',
        'accomplishment', 'leadership', 'teamwork'
    ]
    prof_hits = sum(1 for k in professional_keywords if k in cleaned_text.lower())
    score += min(prof_hits * 2, 10)

    return min(score, 100)


def calculate_category_scores(
        skills_count: int,
        ats_score: int,
        content_quality: float,
        format_score: int
) -> Dict[str, int]:
    """
    Calculate scores for different resume categories.
    """
    return {
        'skills': min(skills_count * 5, 100),
        'ats_compatibility': ats_score,
        'content_quality': int(content_quality),
        'format': format_score,
        'overall': int((
                min(skills_count * 5, 100) * 0.25 +
                ats_score * 0.35 +
                content_quality * 0.25 +
                format_score * 0.15
        ))
    }


def get_score_interpretation(score: int) -> Dict[str, str]:
    """
    Get interpretation of resume score.
    """
    if score >= 90:
        level = "Exceptional"
        description = "Outstanding resume with excellent optimization"
        action = "Ready to apply with confidence"
    elif score >= 80:
        level = "Excellent"
        description = "Very strong resume with minor room for improvement"
        action = "Make minor tweaks and apply"
    elif score >= 70:
        level = "Good"
        description = "Solid resume that should perform well"
        action = "Consider a few improvements before applying"
    elif score >= 60:
        level = "Fair"
        description = "Acceptable resume with improvement needed"
        action = "Work on key areas before applying"
    elif score >= 50:
        level = "Below Average"
        description = "Resume needs significant improvements"
        action = "Revise thoroughly before applying"
    else:
        level = "Poor"
        description = "Resume requires major overhaul"
        action = "Substantial revision needed"

    return {
        'level': level,
        'description': description,
        'action': action,
        'score': score
    }


def calculate_competitive_score(
        ats_score: int,
        skills_count: int,
        years_experience: int = None
) -> Dict[str, any]:
    """
    Calculate how competitive the resume is.
    """
    # Base competitiveness on ATS and skills
    base_score = (ats_score * 0.6 + min(skills_count * 5, 100) * 0.4)

    # Adjust for experience
    if years_experience is not None:
        if years_experience >= 10:
            base_score = min(base_score * 1.2, 100)
        elif years_experience >= 5:
            base_score = min(base_score * 1.1, 100)
        elif years_experience < 2:
            base_score = base_score * 0.9

    competitive_level = (
        "Highly Competitive" if base_score >= 85 else
        "Competitive" if base_score >= 70 else
        "Moderately Competitive" if base_score >= 55 else
        "Below Competitive"
    )

    return {
        'competitive_score': round(base_score, 2),
        'competitive_level': competitive_level,
        'market_readiness': base_score >= 70,
        'recommendation': (
            "Excellent position to compete for top roles" if base_score >= 85 else
            "Well-positioned for most opportunities" if base_score >= 70 else
            "May face challenges in competitive markets" if base_score >= 55 else
            "Needs strengthening before applying"
        )
    }


def generate_score_summary(scores: Dict[str, any]) -> str:
    """
    Generate human-readable score summary.
    """
    overall = scores.get('overall', 0)
    interpretation = get_score_interpretation(overall)

    summary = f"Resume Score: {overall}/100 - {interpretation['level']}\n"
    summary += f"{interpretation['description']}\n"
    summary += f"Action: {interpretation['action']}\n\n"

    # Add component scores
    if 'ats_score' in scores:
        summary += f"• ATS Compatibility: {scores['ats_score']}/100\n"
    if 'skills_count' in scores:
        summary += f"• Skills Coverage: {min(scores['skills_count'] * 5, 100)}/100\n"
    if 'content_quality' in scores:
        summary += f"• Content Quality: {scores['content_quality']}/100\n"

    return summary


class ResumeScorer:
    """Class-based resume scorer."""

    def __init__(self):
        """Initialize resume scorer."""
        pass

    def calculate_score(
            self,
            skills: list,
            cleaned_text: str,
            has_experience: bool = True,
            has_education: bool = True
    ) -> int:
        """Calculate overall resume score."""
        return calculate_resume_score(
            skills,
            cleaned_text,
            has_experience,
            has_education
        )

    def get_interpretation(self, score: int) -> Dict[str, str]:
        """Get score interpretation."""
        return get_score_interpretation(score)

    def calculate_competitive_score(
            self,
            ats_score: int,
            skills_count: int,
            years_experience: int = None
    ) -> Dict[str, any]:
        """Calculate competitive score."""
        return calculate_competitive_score(
            ats_score,
            skills_count,
            years_experience
        )