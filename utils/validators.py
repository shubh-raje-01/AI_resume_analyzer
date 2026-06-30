from pathlib import Path
from typing import Tuple
import logging

from config import (
    MIN_RESUME_LENGTH,
    MAX_RESUME_LENGTH,
    MAX_FILE_SIZE_MB,
    SUPPORTED_RESUME_FORMATS
)

logger = logging.getLogger(__name__)


def validate_resume_text(text: str) -> Tuple[bool, str]:
    """
    Validate resume text.
    """
    if not text:
        return False, "Resume text is empty"

    if not isinstance(text, str):
        return False, "Resume text must be a string"

    text_length = len(text.strip())

    if text_length < MIN_RESUME_LENGTH:
        return False, f"Resume too short (minimum {MIN_RESUME_LENGTH} characters)"

    if text_length > MAX_RESUME_LENGTH:
        return False, f"Resume too long (maximum {MAX_RESUME_LENGTH} characters)"

    return True, "Valid"


def validate_file_size(file_path: Path) -> Tuple[bool, str]:
    """Validate file size."""
    if not file_path.exists():
        return False, "File does not exist"

    size_mb = file_path.stat().st_size / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f}MB, max {MAX_FILE_SIZE_MB}MB)"

    if size_mb == 0:
        return False, "File is empty"

    return True, "Valid"


def validate_file_format(filename: str) -> Tuple[bool, str]:
    """Validate file format."""
    extension = Path(filename).suffix.lower().replace('.', '')

    if extension not in SUPPORTED_RESUME_FORMATS:
        return False, f"Unsupported format. Use: {', '.join(SUPPORTED_RESUME_FORMATS)}"

    return True, "Valid"


def validate_job_role(job_role: str) -> Tuple[bool, str]:
    """Validate job role."""
    from ml.model_config import JOB_ROLES

    if not job_role:
        return False, "Job role is empty"

    if job_role not in JOB_ROLES:
        return False, f"Unsupported job role. Choose from: {', '.join(JOB_ROLES)}"

    return True, "Valid"


def validate_skills(skills: list) -> Tuple[bool, str]:
    """Validate skills list."""
    if not isinstance(skills, list):
        return False, "Skills must be a list"

    if len(skills) == 0:
        return False, "No skills found"

    # Check if all items are strings
    if not all(isinstance(s, str) for s in skills):
        return False, "All skills must be strings"

    return True, "Valid"


def validate_analysis_inputs(
        resume_text: str,
        resume_skills: list,
        job_role: str
) -> Tuple[bool, str]:
    """
    Validate all inputs for resume analysis.
    """
    # Validate text
    is_valid, message = validate_resume_text(resume_text)
    if not is_valid:
        return False, f"Text validation failed: {message}"

    # Validate skills
    is_valid, message = validate_skills(resume_skills)
    if not is_valid:
        return False, f"Skills validation failed: {message}"

    # Validate job role
    is_valid, message = validate_job_role(job_role)
    if not is_valid:
        return False, f"Job role validation failed: {message}"

    return True, "All inputs valid"


class InputValidator:
    """Class-based input validator."""

    def __init__(self):
        """Initialize validator."""
        pass

    def validate_text(self, text: str) -> Tuple[bool, str]:
        """Validate resume text."""
        return validate_resume_text(text)

    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """Validate file."""
        # Check format
        is_valid, message = validate_file_format(str(file_path))
        if not is_valid:
            return False, message

        # Check size
        return validate_file_size(file_path)

    def validate_inputs(
            self,
            resume_text: str,
            resume_skills: list,
            job_role: str
    ) -> Tuple[bool, str]:
        """Validate all analysis inputs."""
        return validate_analysis_inputs(resume_text, resume_skills, job_role)