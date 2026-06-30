from typing import List, Dict


def generate_improvement_tips(
        ats_score: int,
        missing_core: List[str],
        missing_optional: List[str],
        missing_sections: List[str]
) -> List[str]:
    """
    Generate actionable improvement tips.
    """
    tips = []

    # ATS-related tips
    if ats_score < 60:
        tips.append(
            "💡 Increase ATS score by incorporating keywords from job descriptions"
        )
        tips.append(
            "🔍 Use exact terminology from job postings in your experience descriptions"
        )

    # Skill tips
    if missing_core:
        tips.append(
            f"🎯 Priority: Add these high-demand skills - {', '.join(missing_core[:3])}"
        )

    if missing_optional:
        tips.append(
            f"✨ Stand out by adding: {', '.join(missing_optional[:2])}"
        )

    # Section tips
    if missing_sections:
        tips.append(
            f"📋 Complete your resume: Add {', '.join(missing_sections)} section(s)"
        )

    # General best practices
    tips.extend([
        "📊 Quantify achievements (e.g., 'Increased sales by 25%')",
        "💪 Start bullet points with strong action verbs",
        "🎨 Keep formatting clean and ATS-friendly (avoid tables, columns)",
        "✏️ Tailor your resume for each specific job application"
    ])

    return tips[:8]  # Return top 8 tips


def get_role_specific_tips(job_role: str) -> List[str]:
    """Get tips specific to job role."""
    tips_by_role = {
        "Data Analyst": [
            "Highlight experience with SQL and data visualization tools",
            "Showcase data-driven projects and insights",
            "Mention statistical analysis skills",
            "Include experience with Excel, Tableau, or Power BI"
        ],
        "ML Engineer": [
            "Emphasize ML frameworks (TensorFlow, PyTorch)",
            "Showcase deployed ML models and their impact",
            "Highlight feature engineering experience",
            "Mention experience with MLOps and model deployment"
        ],
        "Software Engineer": [
            "Demonstrate strong data structures & algorithms knowledge",
            "Highlight system design experience",
            "Showcase problem-solving through projects",
            "Mention experience with version control (Git)"
        ],
        "Backend Developer": [
            "Emphasize API development experience",
            "Highlight database design and optimization",
            "Showcase microservices architecture experience",
            "Mention cloud platform experience (AWS, Azure, GCP)"
        ],
        "Frontend Developer": [
            "Highlight modern framework experience (React, Vue, Angular)",
            "Showcase responsive design projects",
            "Emphasize UI/UX sensibility",
            "Mention performance optimization experience"
        ]
    }

    return tips_by_role.get(job_role, [
        "Highlight relevant technical skills",
        "Showcase projects related to the role",
        "Emphasize problem-solving abilities",
        "Quantify your achievements"
    ])


def get_experience_level_tips(years_experience: int = None) -> List[str]:
    """Get tips based on experience level."""
    if years_experience is None:
        return []

    if years_experience < 2:
        return [
            "Emphasize academic projects and coursework",
            "Highlight internships and part-time work",
            "Showcase relevant personal projects",
            "Include certifications and online courses"
        ]
    elif years_experience < 5:
        return [
            "Focus on measurable achievements in each role",
            "Highlight technologies and tools mastered",
            "Show progression and growing responsibilities",
            "Include both technical and leadership skills"
        ]
    else:
        return [
            "Emphasize leadership and mentorship experience",
            "Highlight strategic contributions and impact",
            "Focus on senior-level achievements",
            "Show expertise in specific domains"
        ]


def get_quick_wins(analysis: Dict) -> List[str]:
    """Get quick improvement wins."""
    quick_wins = []

    if analysis.get('first_person_count', 0) > 0:
        quick_wins.append("Remove first-person pronouns (I, me, my)")

    if analysis.get('passive_voice_count', 0) > 3:
        quick_wins.append("Convert passive voice to active voice")

    if analysis.get('weak_verbs_count', 0) > 3:
        quick_wins.append("Replace weak phrases with strong action verbs")

    if analysis.get('quantification_score', 0) < 30:
        quick_wins.append("Add numbers and metrics to achievements")

    return quick_wins


class TipsGenerator:
    """Class-based tips generator."""

    def __init__(self):
        """Initialize tips generator."""
        pass

    def generate_tips(
            self,
            ats_score: int,
            missing_core: List[str],
            missing_optional: List[str],
            missing_sections: List[str]
    ) -> List[str]:
        """Generate improvement tips."""
        return generate_improvement_tips(
            ats_score,
            missing_core,
            missing_optional,
            missing_sections
        )

    def get_role_tips(self, job_role: str) -> List[str]:
        """Get role-specific tips."""
        return get_role_specific_tips(job_role)

    def get_experience_tips(self, years: int) -> List[str]:
        """Get experience-level tips."""
        return get_experience_level_tips(years)

    def get_quick_wins(self, analysis: Dict) -> List[str]:
        """Get quick improvement wins."""
        return get_quick_wins(analysis)