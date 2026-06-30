from pathlib import Path
from typing import Optional
import shutil
import logging

logger = logging.getLogger(__name__)


def ensure_directory(directory: Path) -> None:
    """Ensure directory exists."""
    directory.mkdir(parents=True, exist_ok=True)


def safe_file_write(filepath: Path, content: str) -> bool:
    """
    Safely write content to file.
    """
    try:
        ensure_directory(filepath.parent)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error writing to {filepath}: {str(e)}")
        return False


def safe_file_read(filepath: Path) -> Optional[str]:
    """
    Safely read file content.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {str(e)}")
        return None


def copy_file(source: Path, destination: Path) -> bool:
    """Copy file safely."""
    try:
        ensure_directory(destination.parent)
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        logger.error(f"Error copying file: {str(e)}")
        return False


def get_file_info(filepath: Path) -> dict:
    """Get file information."""
    if not filepath.exists():
        return {'exists': False}

    stat = filepath.stat()

    return {
        'exists': True,
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'extension': filepath.suffix,
        'name': filepath.name,
        'is_file': filepath.is_file()
    }


class FileHandler:
    """Class-based file handler."""

    def __init__(self, base_dir: Path = None):
        """Initialize file handler."""
        self.base_dir = base_dir or Path.cwd()

    def write(self, filename: str, content: str) -> bool:
        """Write file."""
        filepath = self.base_dir / filename
        return safe_file_write(filepath, content)

    def read(self, filename: str) -> Optional[str]:
        """Read file."""
        filepath = self.base_dir / filename
        return safe_file_read(filepath)

    def get_info(self, filename: str) -> dict:
        """Get file info."""
        filepath = self.base_dir / filename
        return get_file_info(filepath)