import re
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


def extract_profile_info(text: str) -> Dict[str, str]:
    """
    Extract profile information from resume text.
    """
    profile = {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'linkedin': extract_linkedin(text),
        'github': extract_github(text)
    }

    logger.debug(f"Extracted profile: {profile}")
    return profile


def extract_name(text: str) -> str:
    """
    Extract name from resume (improved logic).
    """
    if not text:
        return "Not Found"

    lines = [line.strip() for line in text.split('\n')[:10] if line.strip()]

    for line in lines:
        # Skip lines with email, phone, or URLs
        if any(char in line for char in ['@', 'http', 'www.']):
            continue

        # Skip lines with numbers (likely phone or address)
        if re.search(r'\d{3}', line):
            continue

        # Check if line looks like a name (2-4 words, proper case)
        words = line.split()

        if 2 <= len(words) <= 4:
            # All words should start with capital
            if all(w[0].isupper() for w in words if w):
                # Words should be mostly alphabetic
                if all(w.replace('-', '').replace("'", '').isalpha() for w in words):
                    return line.title()

    return "Not Found"


def extract_email(text: str) -> str:
    """
    Extract email address from text.
    """
    if not text:
        return "Not Found"

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)

    if matches:
        # Return first valid email
        return matches[0].lower()

    return "Not Found"


def extract_phone(text: str) -> str:
    """
    Extract phone number from text.
    """
    if not text:
        return "Not Found"

    # Pattern for various phone formats
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-234-567-8900
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (234) 567-8900
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'  # 234-567-8900
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Filter out sequences that are too long or don't look like phone numbers
            for match in matches:
                digits = re.sub(r'\D', '', match)
                if 10 <= len(digits) <= 15:
                    return match.strip()

    return "Not Found"


def extract_linkedin(text: str) -> str:
    """
    Extract LinkedIn URL from text.
    """
    if not text:
        return "Not Found"

    pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        url = matches[0]
        # Ensure https://
        if not url.startswith('http'):
            url = 'https://' + url
        return url

    return "Not Found"


def extract_github(text: str) -> str:
    """
    Extract GitHub URL from text.
    """
    if not text:
        return "Not Found"

    pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        url = matches[0]
        # Ensure https://
        if not url.startswith('http'):
            url = 'https://' + url
        return url

    return "Not Found"


def extract_location(text: str) -> str:
    """
    Extract location from text.
    """
    # Common location patterns
    patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?,\s*[A-Z]{2})',  # City, ST
        r'([A-Z][a-z]+,\s*[A-Z][a-z]+)'  # City, Country
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]

    return "Not Found"


def validate_profile(profile: Dict[str, str]) -> Dict[str, bool]:
    """
    Validate extracted profile information.
    """
    validation = {}

    # Validate email
    validation['email_valid'] = (
            profile.get('email', 'Not Found') != 'Not Found' and
            '@' in profile.get('email', '')
    )

    # Validate phone
    phone = profile.get('phone', 'Not Found')
    validation['phone_valid'] = (
            phone != 'Not Found' and
            len(re.sub(r'\D', '', phone)) >= 10
    )

    # Validate name
    validation['name_valid'] = (
            profile.get('name', 'Not Found') != 'Not Found' and
            len(profile.get('name', '').split()) >= 2
    )

    # Validate LinkedIn
    validation['linkedin_valid'] = (
            'linkedin.com' in profile.get('linkedin', '').lower()
    )

    # Validate GitHub
    validation['github_valid'] = (
            'github.com' in profile.get('github', '').lower()
    )

    return validation


def get_profile_completeness(profile: Dict[str, str]) -> Dict[str, any]:
    """
    Calculate profile completeness score.
    """
    validation = validate_profile(profile)

    # Count valid fields
    valid_count = sum(1 for v in validation.values() if v)
    total_fields = len(validation)

    completeness = (valid_count / total_fields * 100) if total_fields > 0 else 0

    missing_fields = [
        field.replace('_valid', '')
        for field, is_valid in validation.items()
        if not is_valid
    ]

    return {
        'completeness_percentage': round(completeness, 2),
        'valid_fields': valid_count,
        'total_fields': total_fields,
        'validation': validation,
        'missing_fields': missing_fields,
        'recommendation': (
            'Profile is complete' if completeness >= 80 else
            'Add missing contact information' if completeness >= 60 else
            'Profile needs significant completion'
        )
    }


class ProfileExtractor:
    """Class-based profile extractor for advanced usage."""

    def __init__(self):
        """Initialize profile extractor."""
        pass

    def extract(self, text: str) -> Dict[str, str]:
        """Extract profile information."""
        return extract_profile_info(text)

    def extract_with_validation(self, text: str) -> Dict[str, any]:
        """Extract profile with validation."""
        profile = extract_profile_info(text)
        validation = validate_profile(profile)
        completeness = get_profile_completeness(profile)

        return {
            'profile': profile,
            'validation': validation,
            'completeness': completeness
        }