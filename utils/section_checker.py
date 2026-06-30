from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

# Standard resume sections
STANDARD_SECTIONS = {
    'contact': ['contact', 'email', 'phone', 'address'],
    'summary': ['summary', 'objective', 'profile', 'about'],
    'experience': ['experience', 'work history', 'employment', 'professional experience'],
    'education': ['education', 'academic', 'degree', 'university', 'college'],
    'skills': ['skills', 'technical skills', 'competencies', 'proficiencies'],
    'projects': ['projects', 'personal projects', 'portfolio'],
    'certifications': ['certifications', 'certificates', 'credentials'],
    'awards': ['awards', 'honors', 'achievements', 'recognition']
}

CRITICAL_SECTIONS = ['contact', 'experience', 'education', 'skills']
RECOMMENDED_SECTIONS = ['summary', 'projects']


def check_resume_sections(text: str) -> Dict[str, bool]:
    """
    Check which standard sections are present in resume.
    """
    if not text:
        return {section: False for section in STANDARD_SECTIONS.keys()}

    text_lower = text.lower()
    sections_found = {}

    for section_name, keywords in STANDARD_SECTIONS.items():
        # Check if any keyword for this section is present
        found = any(keyword in text_lower for keyword in keywords)
        sections_found[section_name] = found

        if found:
            logger.debug(f"Found section: {section_name}")

    return sections_found


def get_missing_sections(text: str) -> List[str]:
    """
    Get list of missing sections from resume.
    """
    sections = check_resume_sections(text)
    return [section for section, present in sections.items() if not present]


def get_missing_critical_sections(text: str) -> List[str]:
    """
    Get list of missing critical sections.
    """
    sections = check_resume_sections(text)
    return [
        section for section in CRITICAL_SECTIONS
        if not sections.get(section, False)
    ]


def calculate_section_score(text: str) -> Dict[str, any]:
    """
    Calculate section completeness score.
    """
    sections = check_resume_sections(text)

    # Count present sections
    total_sections = len(STANDARD_SECTIONS)
    present_sections = sum(1 for present in sections.values() if present)

    # Check critical sections
    critical_present = sum(
        1 for section in CRITICAL_SECTIONS
        if sections.get(section, False)
    )
    critical_total = len(CRITICAL_SECTIONS)

    # Calculate scores
    overall_score = (present_sections / total_sections * 100) if total_sections > 0 else 0
    critical_score = (critical_present / critical_total * 100) if critical_total > 0 else 0

    # Get missing sections
    missing_critical = get_missing_critical_sections(text)
    missing_recommended = [
        section for section in RECOMMENDED_SECTIONS
        if not sections.get(section, False)
    ]

    return {
        'overall_score': round(overall_score, 2),
        'critical_score': round(critical_score, 2),
        'sections_present': [s for s, present in sections.items() if present],
        'sections_missing': [s for s, present in sections.items() if not present],
        'critical_missing': missing_critical,
        'recommended_missing': missing_recommended,
        'total_sections': total_sections,
        'present_count': present_sections,
        'is_complete': len(missing_critical) == 0,
        'recommendation': get_section_recommendation(missing_critical, missing_recommended)
    }


def get_section_recommendation(
        missing_critical: List[str],
        missing_recommended: List[str]
) -> str:
    """
    Generate recommendation based on missing sections.
    """
    if missing_critical:
        return f"Add critical sections: {', '.join(missing_critical)}"
    elif missing_recommended:
        return f"Consider adding: {', '.join(missing_recommended)}"
    else:
        return "All important sections present"


def analyze_section_content(text: str) -> Dict[str, any]:
    """
    Analyze content within each section.
    """
    sections = check_resume_sections(text)
    analysis = {}

    # Rough word count for each section
    text_lower = text.lower()

    for section_name, keywords in STANDARD_SECTIONS.items():
        if sections.get(section_name, False):
            # Find section content (very rough approximation)
            for keyword in keywords:
                if keyword in text_lower:
                    # Get approximate content after keyword
                    start_idx = text_lower.index(keyword)
                    # Take next 500 characters as section content
                    section_text = text[start_idx:start_idx + 500]
                    word_count = len(section_text.split())

                    analysis[section_name] = {
                        'present': True,
                        'estimated_words': word_count,
                        'sufficient_content': word_count >= 20
                    }
                    break
        else:
            analysis[section_name] = {
                'present': False,
                'estimated_words': 0,
                'sufficient_content': False
            }

    return analysis


class SectionChecker:
    """Class-based section checker for advanced usage."""

    def __init__(self):
        """Initialize section checker."""
        self.standard_sections = STANDARD_SECTIONS
        self.critical_sections = CRITICAL_SECTIONS

    def check(self, text: str) -> Dict[str, bool]:
        """Check which sections are present."""
        return check_resume_sections(text)

    def get_missing(self, text: str) -> List[str]:
        """Get missing sections."""
        return get_missing_sections(text)

    def calculate_score(self, text: str) -> Dict[str, any]:
        """Calculate section score."""
        return calculate_section_score(text)

    def analyze_content(self, text: str) -> Dict[str, any]:
        """Analyze section content."""
        return analyze_section_content(text)