from typing import Dict, List, Any
import json


def format_score(score: float, max_score: int = 100) -> str:
    """Format score with percentage."""
    return f"{score}/{max_score} ({score / max_score * 100:.1f}%)"


def format_skills_list(skills: List[str], max_display: int = 10) -> str:
    """Format skills list for display."""
    if not skills:
        return "No skills found"

    if len(skills) <= max_display:
        return ", ".join(skills)

    displayed = ", ".join(skills[:max_display])
    remaining = len(skills) - max_display
    return f"{displayed}, and {remaining} more..."


def format_bullet_points(items: List[str]) -> str:
    """Format list as bullet points."""
    if not items:
        return ""

    return "\n".join(f"• {item}" for item in items)


def format_numbered_list(items: List[str]) -> str:
    """Format list as numbered list."""
    if not items:
        return ""

    return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(items))


def format_analysis_summary(analysis: Dict[str, Any]) -> str:
    """Format complete analysis as summary text."""
    summary = []

    # ATS Score
    if 'ats_score' in analysis:
        summary.append(f"ATS Score: {analysis['ats_score']}/100")

    # Skills
    if 'skills_count' in analysis:
        summary.append(f"Skills Found: {analysis['skills_count']}")

    # Experience
    if 'years_experience' in analysis:
        summary.append(f"Experience: {analysis['years_experience']}+ years")

    # Overall recommendation
    if 'recommendation' in analysis:
        summary.append(f"\n{analysis['recommendation']}")

    return "\n".join(summary)


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage."""
    return f"{value:.{decimals}f}%"


def format_dict_as_table(data: Dict[str, Any], headers: tuple = ("Key", "Value")) -> str:
    """Format dictionary as simple table."""
    if not data:
        return "No data"

    max_key_len = max(len(str(k)) for k in data.keys())
    max_val_len = max(len(str(v)) for v in data.values())

    # Header
    table = f"{headers[0]:<{max_key_len}} | {headers[1]}\n"
    table += "-" * (max_key_len + max_val_len + 3) + "\n"

    # Rows
    for key, value in data.items():
        table += f"{key:<{max_key_len}} | {value}\n"

    return table


def export_to_json(data: Dict[str, Any], filepath: str = None) -> str:
    """Export data to JSON format."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_str)

    return json_str


def format_comparison(before: float, after: float, label: str = "Score") -> str:
    """Format before/after comparison."""
    change = after - before
    symbol = "↑" if change > 0 else "↓" if change < 0 else "→"

    return f"{label}: {before:.1f} {symbol} {after:.1f} ({change:+.1f})"


class OutputFormatter:
    """Class-based output formatter."""

    def __init__(self):
        """Initialize formatter."""
        pass

    def format_score(self, score: float, max_score: int = 100) -> str:
        """Format score."""
        return format_score(score, max_score)

    def format_skills(self, skills: List[str], max_display: int = 10) -> str:
        """Format skills list."""
        return format_skills_list(skills, max_display)

    def format_summary(self, analysis: Dict[str, Any]) -> str:
        """Format analysis summary."""
        return format_analysis_summary(analysis)

    def to_json(self, data: Dict[str, Any], filepath: str = None) -> str:
        """Export to JSON."""
        return export_to_json(data, filepath)