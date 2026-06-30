"""
AI Resume Analyzer Pro — Main Streamlit Application
Ties together: parsers, nlp, ml, semantic, analyzers, utils
"""

import os
import streamlit as st
import logging
from pathlib import Path

# ──────────────────────────────────────────────
# CONFIG  (imported first; also calls ensure_directories())
# ──────────────────────────────────────────────
from config import (
    APP_TITLE, APP_ICON, PAGE_LAYOUT,
    SUPPORTED_RESUME_FORMATS, MAX_FILE_SIZE_MB,
    SUPPORTED_JOB_ROLES, DEFAULT_JOB_ROLE,
    MAX_JOBS_DISPLAY, MAX_SKILLS_DISPLAY, MAX_TIPS_DISPLAY,
    SUCCESS_UPLOAD, ERROR_FILE_TOO_LARGE, ERROR_INVALID_FORMAT,
    ERROR_EMPTY_FILE, ERROR_NO_TEXT, setup_logging
)

# ──────────────────────────────────────────────
# PARSERS
# ──────────────────────────────────────────────
from parsers import extract_text

# ──────────────────────────────────────────────
# NLP
# ──────────────────────────────────────────────
from nlp import (
    clean_text,
    extract_skills,
    categorize_skills,
    extract_all_entities
)

# ──────────────────────────────────────────────
# ML
# ──────────────────────────────────────────────
from ml import quick_predict

# ──────────────────────────────────────────────
# SEMANTIC
# ──────────────────────────────────────────────
from semantic import find_best_matching_jobs

# ──────────────────────────────────────────────
# ANALYZERS
# ──────────────────────────────────────────────
from analyzers import (
    analyze_ats_compatibility,
    analyze_skills,
    analyze_experience,
    analyze_format,
    analyze_content_quality
)

# ──────────────────────────────────────────────
# UTILS
# ──────────────────────────────────────────────
from utils import (
    extract_profile_info,
    calculate_resume_score,
    get_score_interpretation,
    calculate_section_score,
    generate_improvement_tips,
    get_role_specific_tips,
    get_quick_wins,
)


# Configure logging before the app starts processing user input.
setup_logging()
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
CUSTOM_CSS = """
<style>
    :root {
        --bg: #07111f;
        --bg-alt: rgba(10, 17, 33, 0.74);
        --surface: rgba(13, 20, 36, 0.88);
        --surface-strong: #0f172a;
        --surface-soft: rgba(37, 99, 235, 0.14);
        --text: #e5eefb;
        --muted: #94a3b8;
        --border: rgba(148, 163, 184, 0.18);
        --shadow: 0 18px 50px rgba(2, 6, 23, 0.40);
        --shadow-soft: 0 10px 30px rgba(2, 6, 23, 0.28);
        --primary: #60a5fa;
        --primary-2: #a78bfa;
        --success: #4ade80;
        --warning: #fbbf24;
        --danger: #f87171;
        --radius-xl: 28px;
        --radius-lg: 20px;
        --radius-md: 14px;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(124, 58, 237, 0.14), transparent 26%),
            linear-gradient(180deg, var(--bg) 0%, color-mix(in srgb, var(--bg) 92%, black 8%) 100%);
        color: var(--text);
    }

    body, .stApp, [data-testid="stAppViewContainer"] {
        color: var(--text);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stApp [data-testid="stToolbar"] {
        visibility: hidden;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: var(--text);
    }

    h1, h2, h3 {
        letter-spacing: -0.03em;
    }

    h2 {
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.45rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, color-mix(in srgb, var(--surface-strong) 96%, var(--primary) 4%), var(--surface-strong)) !important;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background: var(--surface-strong) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderInstructions"] {
        color: var(--muted) !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSelectbox"] svg,
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] svg {
        color: var(--muted) !important;
        fill: var(--muted) !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stFileUploader label {
        color: var(--muted) !important;
    }

    div[data-baseweb="select"] > div {
        box-shadow: none !important;
    }

    div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] [aria-expanded] {
        background: var(--surface-strong) !important;
        color: var(--text) !important;
    }

    div[role="listbox"] {
        background: var(--surface-strong) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
    }

    div[role="option"] {
        background: var(--surface-strong) !important;
        color: var(--text) !important;
    }

    div[role="option"][aria-selected="true"],
    div[role="option"]:hover {
        background: color-mix(in srgb, var(--primary) 18%, var(--surface-strong)) !important;
    }

    .metric-card,
    .hero-shell,
    .feature-card,
    .tip-box,
    .warning-box,
    .error-box,
    .upload-area {
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(18px);
    }

    .metric-card {
        border-radius: var(--radius-lg);
        padding: 18px 16px;
        text-align: center;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--primary);
        margin: 4px 0;
    }

    .metric-label {
        font-size: 0.76rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.14em;
    }

    .score-excellent { color: var(--success); }
    .score-good      { color: var(--primary); }
    .score-fair      { color: var(--warning); }
    .score-poor      { color: var(--danger); }

    .skill-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: var(--surface-soft);
        color: var(--primary-2);
        border: 1px solid color-mix(in srgb, var(--primary-2) 20%, transparent);
        border-radius: 999px;
        padding: 0.35rem 0.8rem;
        margin: 0.18rem;
        font-size: 0.84rem;
        font-weight: 600;
    }

    .skill-tag.missing {
        background: color-mix(in srgb, var(--danger) 12%, var(--surface));
        color: var(--danger);
        border-color: color-mix(in srgb, var(--danger) 25%, transparent);
    }

    .skill-tag.optional {
        background: color-mix(in srgb, var(--warning) 14%, var(--surface));
        color: var(--warning);
        border-color: color-mix(in srgb, var(--warning) 25%, transparent);
    }

    .tip-box,
    .warning-box,
    .error-box {
        padding: 12px 14px;
        border-radius: 16px;
        margin: 8px 0;
    }

    .tip-box {
        border-left: 4px solid var(--success);
    }

    .warning-box {
        border-left: 4px solid var(--warning);
    }

    .error-box {
        border-left: 4px solid var(--danger);
    }

    .hero-shell {
        border-radius: var(--radius-xl);
        padding: 2rem 1.5rem;
        text-align: center;
        overflow: hidden;
        position: relative;
    }

    .hero-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 28%),
            radial-gradient(circle at bottom right, rgba(124, 58, 237, 0.14), transparent 24%);
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        z-index: 1;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 0.85rem;
        margin-bottom: 1rem;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: color-mix(in srgb, var(--surface-strong) 84%, var(--primary) 16%);
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .hero-title {
        margin: 0;
        font-size: clamp(2.2rem, 5vw, 3.7rem);
        line-height: 1;
        font-weight: 850;
        color: var(--text);
    }

    .hero-subtitle {
        max-width: 720px;
        margin: 1rem auto 0;
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.65;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.9rem;
        margin-top: 1.5rem;
    }

    .feature-card {
        border-radius: var(--radius-md);
        padding: 1rem 0.85rem;
        text-align: center;
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }

    .feature-emoji {
        font-size: 2rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .feature-title {
        font-weight: 700;
        color: var(--text);
    }

    .upload-area {
        border: 1.5px dashed color-mix(in srgb, var(--primary) 58%, var(--border));
        border-radius: var(--radius-lg);
        padding: 30px;
        text-align: center;
        background: linear-gradient(180deg, color-mix(in srgb, var(--surface-strong) 92%, var(--primary) 8%), var(--surface));
    }

    div[data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    button[role="tab"] {
        border-radius: 999px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        color: var(--muted) !important;
        padding: 0.55rem 0.95rem !important;
        box-shadow: none !important;
    }

    button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-2)) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .stButton > button {
        border-radius: 999px;
        border: 1px solid var(--border);
        background: linear-gradient(135deg, var(--primary), var(--primary-2));
        color: white;
        font-weight: 700;
        box-shadow: var(--shadow-soft);
        transition: transform 160ms ease, box-shadow 160ms ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }

    .stButton > button:focus,
    .stButton > button:active {
        color: white !important;
    }

    .stSelectbox, .stMultiSelect, .stTextInput, .stTextArea {
        border-radius: 14px;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--primary-2)) !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════

def _score_colour(score: int) -> str:
    """Return CSS class name for a 0-100 score."""
    if score >= 80: return "score-excellent"
    if score >= 60: return "score-good"
    if score >= 40: return "score-fair"
    return "score-poor"


def _render_metric_card(label: str, value, sub: str = ""):
    """Render a single metric card via raw HTML."""
    # Build sub-label HTML separately to avoid nested f-strings (Python 3.10 compatibility)
    sub_html = f"<div style='font-size:0.78rem;color:#64748b'>{sub}</div>" if sub else ""

    st.markdown(
        f'<div class="metric-card">'
        f'  <div class="metric-label">{label}</div>'
        f'  <div class="metric-value">{value}</div>'
        f'  {sub_html}'
        f'</div>',
        unsafe_allow_html=True
    )


def _render_skill_tags(skills: list, css_class: str = ""):
    """Render a list of skills as coloured tags."""
    html = " ".join(
        f'<span class="skill-tag {css_class}">{s}</span>' for s in skills
    )
    st.markdown(html, unsafe_allow_html=True)


def _validate_upload(uploaded_file) -> tuple:
    """
    Gate-check the uploaded file before any processing.
    Returns (raw_bytes_or_None, error_message_or_None).
    """
    if uploaded_file is None:
        return None, "No file uploaded."

    # extension
    ext = Path(uploaded_file.name).suffix.lower().lstrip(".")
    if ext not in SUPPORTED_RESUME_FORMATS:
        return None, ERROR_INVALID_FORMAT

    # size
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return None, ERROR_FILE_TOO_LARGE

    # empty
    if uploaded_file.size == 0:
        return None, ERROR_EMPTY_FILE

    return uploaded_file, None


# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════

def render_sidebar() -> tuple[object | None, str]:
    """Render the left-hand sidebar with upload + role selector."""
    st.sidebar.markdown("## 📄 AI Resume Analyzer Pro", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📤 Upload Resume")
    uploaded = st.sidebar.file_uploader(
        label="PDF, DOCX or TXT",
        type=SUPPORTED_RESUME_FORMATS,
        help=f"Max {MAX_FILE_SIZE_MB} MB. Supports PDF, DOCX, TXT."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Target Job Role")
    job_role = st.sidebar.selectbox(
        "Select the role you are targeting",
        options=SUPPORTED_JOB_ROLES,
        index=SUPPORTED_JOB_ROLES.index(DEFAULT_JOB_ROLE)
    ) or DEFAULT_JOB_ROLE

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Supported formats:** PDF · DOCX · TXT\n\n"
        "**How it works:**\n"
        "1. Upload your resume\n"
        "2. Pick a target role\n"
        "3. Review your dashboard\n"
        "4. Apply the suggestions\n"
    )

    return uploaded, job_role


def render_landing():
    """Full-width landing hero when nothing has been uploaded yet."""
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        st.markdown(
            '<div class="hero-shell">'
            '  <div class="hero-content">'
            '    <div class="hero-badge">Resume Intelligence</div>'
            '    <h1 class="hero-title">AI Resume Analyzer Pro</h1>'
            '    <p class="hero-subtitle">'
            '      Upload your resume to get a modern, production-grade analysis with ATS scoring, skill gaps, job matches, and tailored coaching.'
            '    </p>'
            '  </div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-grid">'
            '  <div class="feature-card">'
            '    <div class="feature-emoji">📊</div><div class="feature-title">ATS Score</div></div>'
            '  <div class="feature-card">'
            '    <div class="feature-emoji">🔍</div><div class="feature-title">Skill Gap</div></div>'
            '  <div class="feature-card">'
            '    <div class="feature-emoji">💼</div><div class="feature-title">Job Match</div></div>'
            '  <div class="feature-card">'
            '    <div class="feature-emoji">💡</div><div class="feature-title">Coaching</div></div>'
            '</div>',
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════
# EXTRACT & CACHE resume data  (runs once per upload)
# ══════════════════════════════════════════════

@st.cache_data(show_spinner="Parsing & analysing…")
def run_full_analysis(file_bytes: bytes, file_name: str, job_role: str) -> dict:
    """
    Parse → clean → extract → analyse → score.
    Cached by (file_bytes, file_name, job_role) so re-selecting the same
    role re-runs but switching tabs does not.
    """
    import tempfile

    # ── 1. write temp file so parsers can open it ──
    suffix = Path(file_name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file_bytes)
    tmp.close()

    try:
        raw_text = extract_text(tmp.name)
    finally:
        os.unlink(tmp.name)

    if not raw_text or len(raw_text.strip()) < 30:
        return {"error": ERROR_NO_TEXT}

    # ── 2. NLP pipeline ──
    cleaned = clean_text(raw_text)
    skills = extract_skills(cleaned)
    skill_categories = categorize_skills(skills)
    entities = extract_all_entities(raw_text)
    profile = extract_profile_info(raw_text)

    # ── 3. ML prediction ──
    try:
        predicted_role, confidence = quick_predict(cleaned)
    except (RuntimeError, ValueError, FileNotFoundError):
        predicted_role, confidence = "N/A", 0.0

    # ── 4. Analyzers ──
    ats = analyze_ats_compatibility(cleaned, skills, job_role)
    skill_an = analyze_skills(skills, cleaned, job_role)
    exp_an = analyze_experience(raw_text)
    fmt_an = analyze_format(raw_text)
    qual_an = analyze_content_quality(cleaned)

    # ── 5. Scoring ──
    has_exp = fmt_an.get("sections_present", {}).get("experience", False)
    has_edu = fmt_an.get("sections_present", {}).get("education", False)
    resume_score = calculate_resume_score(skills, cleaned, has_exp, has_edu)
    interpretation = get_score_interpretation(resume_score)
    section_score = calculate_section_score(raw_text)

    # ── 6. Feedback & tips ──
    missing_core = ats.get("missing_core_skills", [])
    missing_optional = ats.get("missing_optional_skills", [])
    missing_sections = section_score.get("critical_missing", [])

    tips = generate_improvement_tips(
        ats.get("ats_score", 0), missing_core, missing_optional, missing_sections
    )
    role_tips = get_role_specific_tips(job_role)
    quick_win_list = get_quick_wins(qual_an)

    # ── 7. Job matching ──
    try:
        job_matches = find_best_matching_jobs(cleaned, top_n=MAX_JOBS_DISPLAY)
    except (RuntimeError, ValueError, FileNotFoundError):
        job_matches = []

    return {
        "error": None,
        # raw
        "raw_text": raw_text,
        "cleaned_text": cleaned,
        # profile
        "profile": profile,
        "entities": entities,
        # skills
        "skills": skills,
        "skill_categories": skill_categories,
        # ml
        "predicted_role": predicted_role,
        "ml_confidence": confidence,
        # analyzers
        "ats": ats,
        "skill_analysis": skill_an,
        "experience": exp_an,
        "format": fmt_an,
        "quality": qual_an,
        # scoring
        "resume_score": resume_score,
        "interpretation": interpretation,
        "section_score": section_score,
        # feedback
        "tips": tips,
        "role_tips": role_tips,
        "quick_wins": quick_win_list,
        # jobs
        "job_matches": job_matches,
        # meta
        "job_role": job_role
    }


# ══════════════════════════════════════════════
# DASHBOARD TABS
# ══════════════════════════════════════════════

def tab_overview(data: dict):
    """📊 Overview — top-level metric cards + profile card."""
    ats_score = data["ats"].get("ats_score", 0)
    resume_score = data["resume_score"]
    interp = data["interpretation"]
    skill_count = len(data["skills"])
    profile = data["profile"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _render_metric_card("Resume Score", resume_score, interp["level"])
    with c2:
        _render_metric_card("ATS Score", ats_score, data["ats"].get("compatibility_level", ""))
    with c3:
        _render_metric_card("Skills Found", skill_count, data["skill_analysis"].get("skill_strength", ""))
    with c4:
        exp_yrs = data["experience"].get("years_of_experience")
        _render_metric_card("Experience", exp_yrs if exp_yrs is not None else "—", "years")

    st.markdown("---")
    left, right = st.columns([2, 1])

    with left:
        st.markdown("#### 🤖 ML Predicted Role")
        st.markdown(
            f'<span style="display:inline-flex;align-items:center;gap:0.5rem;'
            f'background:linear-gradient(135deg,var(--primary),var(--primary-2));'
            f'color:white;padding:0.45rem 1rem;border-radius:999px;font-weight:700;'
            f'font-size:1rem;box-shadow:var(--shadow-soft);">'
            f'{data["predicted_role"]}</span> '
            f'<span style="color:var(--muted);font-size:0.9rem;">'
            f'confidence {data["ml_confidence"]:.0f}%</span>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("#### 🎯 Target Role")
        st.info(data["job_role"])

    st.markdown("---")
    st.markdown("#### 👤 Candidate Profile")
    p = profile
    cols = st.columns(3)
    cols[0].markdown(f"**Name:** {p.get('name', '—')}")
    cols[1].markdown(f"**Email:** {p.get('email', '—')}")
    cols[2].markdown(f"**Phone:** {p.get('phone', '—')}")

    row2 = st.columns(2)
    row2[0].markdown(f"**LinkedIn:** {p.get('linkedin', '—')}")
    row2[1].markdown(f"**GitHub:** {p.get('github', '—')}")

    st.markdown("---")
    st.markdown("#### 📈 Overall Assessment")
    st.markdown(
        f'<div class="tip-box">'
        f'<strong>{interp["level"]}</strong> — {interp["description"]}<br>'
        f'<em>Action: {interp["action"]}</em>'
        f'</div>',
        unsafe_allow_html=True,
    )


def tab_ats(data: dict):
    """🎯 ATS Analysis — keyword / semantic breakdown + missing skills."""
    ats = data["ats"]
    score = ats.get("ats_score", 0)

    # ── score header ──
    cl = _score_colour(score)
    st.markdown(
        f'<h2>ATS Compatibility Score</h2>'
        f'<div class="metric-value {cl}">{score} / 100</div>'
        f'<p style="color:#64748b;">{ats.get("compatibility_level", "")} — '
        f'Pass probability: {ats.get("pass_probability", 0):.0f}%</p>',
        unsafe_allow_html=True
    )

    # ── keyword vs semantic sub-scores ──
    st.markdown("---")
    left, right = st.columns(2)
    with left:
        kw = ats.get("keyword_score", 0)
        st.markdown(f"**Keyword Match Score:** {kw} / 100")
        st.progress(min(kw, 100) / 100)
    with right:
        sem = ats.get("semantic_score", 0)
        st.markdown(f"**Semantic Match Score:** {sem} / 100")
        st.progress(min(sem, 100) / 100)

    # ── matched / missing ──
    st.markdown("---")
    mc, mo = st.columns(2)
    with mc:
        st.markdown("#### ✅ Matched Core Skills")
        _render_skill_tags(ats.get("matched_core_skills", []))
        st.markdown("#### ✅ Matched Optional Skills")
        _render_skill_tags(ats.get("matched_optional_skills", []))
    with mo:
        st.markdown("#### ❌ Missing Core Skills")
        _render_skill_tags(ats.get("missing_core_skills", []), "missing")
        st.markdown("#### ⚠️ Missing Optional Skills")
        _render_skill_tags(ats.get("missing_optional_skills", []), "optional")

    # ── suggestions ──
    if ats.get("suggestions"):
        st.markdown("---")
        st.markdown("#### 💡 Improvement Suggestions")
        for s in ats["suggestions"]:
            st.markdown(f'<div class="warning-box">{s}</div>', unsafe_allow_html=True)


def tab_skills(data: dict):
    """🛠️ Skills — categorised tags + strength + gap detail."""
    sa = data["skill_analysis"]
    cats = data["skill_categories"]

    # header
    st.markdown(f"#### 🛠️ Skills Overview — {sa.get('total_skills', 0)} skills detected  "
                f"({sa.get('skill_strength', '')})")

    # ── by category ──
    st.markdown("---")
    t_col, s_col, d_col = st.columns(3)
    with t_col:
        st.markdown("**💻 Technical**")
        _render_skill_tags(cats.get("technical", []))
    with s_col:
        st.markdown("**🤝 Soft Skills**")
        _render_skill_tags(cats.get("soft", []))
    with d_col:
        st.markdown("**📦 Domain**")
        _render_skill_tags(cats.get("domain", []))

    # ── recommendation ──
    st.markdown("---")
    st.markdown(f'<div class="tip-box">{sa.get("recommendation", "")}</div>', unsafe_allow_html=True)

    # ── related suggestions ──
    related = sa.get("related_suggestions", [])
    if related:
        st.markdown("#### 💫 Suggested Skills to Add")
        _render_skill_tags(related[:MAX_SKILLS_DISPLAY], "optional")


def tab_experience(data: dict):
    """📜 Experience & Format — sections checklist + word-count."""
    exp = data["experience"]
    fmt = data["format"]
    sec = data["section_score"]

    # ── experience summary ──
    st.markdown("#### 📜 Work Experience")
    st.markdown(f"- **Years of Experience:** {exp.get('years_of_experience', 'N/A')}")
    st.markdown(f"- **Experience Level:** {exp.get('experience_level', 'N/A')}")
    st.markdown(f"- **Companies:** {', '.join(exp.get('companies', [])) or 'N/A'}")
    st.markdown(f"- **Assessment:** {exp.get('assessment', '')}")

    # ── sections checklist ──
    st.markdown("---")
    st.markdown("#### 📋 Resume Sections")
    sections = fmt.get("sections_present", {})
    for name, present in sections.items():
        icon = "✅" if present else "❌"
        st.markdown(f"  {icon} **{name.title()}**")

    # ── section score ──
    st.markdown("---")
    st.markdown(f"**Section Completeness:** {sec.get('overall_score', 0):.0f}%")
    st.progress(sec.get("overall_score", 0) / 100)

    if sec.get("critical_missing"):
        missing_list = ", ".join(sec["critical_missing"])
        st.markdown(
            f'<div class="error-box">⚠️ Missing critical sections: '
            f'{missing_list}</div>',
            unsafe_allow_html=True
        )

    # ── length ──
    st.markdown("---")
    length = fmt.get("length_analysis", {})
    st.markdown(f"**Word Count:** {length.get('word_count', 0)}  —  {length.get('assessment', '')}")


def tab_quality(data: dict):
    """✨ Content Quality — action verbs, quantification, readability."""
    q = data["quality"]

    # ── score row ──
    c1, c2, c3 = st.columns(3)
    with c1:
        _render_metric_card("Overall Quality", q.get("overall_score", 0), q.get("quality_level", ""))
    with c2:
        _render_metric_card("Readability", q.get("readability_score", 0), "/100")
    with c3:
        _render_metric_card("Quantification", q.get("quantification_score", 0), "/100")

    # ── strengths / weaknesses ──
    st.markdown("---")
    s_col, w_col = st.columns(2)
    with s_col:
        st.markdown("#### ✅ Strengths")
        for s in q.get("strengths", []) or ["—"]:
            st.markdown(f'<div class="tip-box">{s}</div>', unsafe_allow_html=True)
    with w_col:
        st.markdown("#### ⚠️ Weaknesses")
        for w in q.get("weaknesses", []) or ["—"]:
            st.markdown(f'<div class="warning-box">{w}</div>', unsafe_allow_html=True)

    # ── quick wins ──
    qw = data.get("quick_wins", [])
    if qw:
        st.markdown("---")
        st.markdown("#### 🎯 Quick Wins")
        for w in qw:
            st.markdown(f'<div class="tip-box">💥 {w}</div>', unsafe_allow_html=True)


def tab_jobs(data: dict):
    """💼 Job Matches — semantic-similarity ranked list."""
    matches = data.get("job_matches", [])
    if not matches:
        st.info("Job matching requires the sentence-transformer model. "
                "Install `sentence-transformers` and try again.")
        return

    st.markdown("#### 💼 Top Job Matches")
    for i, job in enumerate(matches[:MAX_JOBS_DISPLAY], 1):
        title = job.get("job_title", "Unknown")
        match_pct = job.get("semantic_match", 0)
        desc = job.get("job_description", "")[:160]

        colour = _score_colour(int(match_pct))
        st.markdown(
            f'<div style="background:white;border-radius:10px;padding:14px 18px;'
            f'box-shadow:0 1px 4px rgba(0,0,0,0.08);margin-bottom:10px;">'
            f'  <span style="font-weight:700;font-size:1.05rem;">{i}. {title}</span>'
            f'  <span class="{colour}" style="margin-left:12px;font-weight:600;">'
            f'{match_pct:.0f}% match</span><br>'
            f'  <span style="color:#64748b;font-size:0.88rem;">{desc}…</span>'
            f'</div>',
            unsafe_allow_html=True
        )


def tab_coach(data: dict):
    """🎓 Coach — tips, role-specific advice, quick wins."""
    tips = data.get("tips", [])
    role_tips = data.get("role_tips", [])
    quick_wins = data.get("quick_wins", [])
    job_role = data.get("job_role", "")

    # ── quick wins first ──
    if quick_wins:
        st.markdown("#### 🎯 Quick Wins (do these first!)")
        for w in quick_wins:
            st.markdown(f'<div class="tip-box">💥 {w}</div>', unsafe_allow_html=True)

    # ── general tips ──
    if tips:
        st.markdown("---")
        st.markdown("#### 💡 General Improvement Tips")
        for t in tips[:MAX_TIPS_DISPLAY]:
            st.markdown(f'<div class="tip-box">{t}</div>', unsafe_allow_html=True)

    # ── role-specific ──
    if role_tips:
        st.markdown("---")
        st.markdown(f"#### 🎯 Tips for {job_role}")
        for t in role_tips:
            st.markdown(f'<div class="warning-box">📌 {t}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def main():
    try:
        uploaded_file, job_role = render_sidebar()

        # ── nothing uploaded → landing ──
        if uploaded_file is None:
            render_landing()
            return

        # ── validate ──
        file_obj, err = _validate_upload(uploaded_file)
        if err:
            st.error(err)
            return

        # ── success banner ──
        st.success(SUCCESS_UPLOAD)

        # ── run analysis (cached) ──
        data = run_full_analysis(
            file_bytes=file_obj.getvalue(),
            file_name=file_obj.name,
            job_role=job_role
        )

        # ── error from inside the pipeline ──
        if data.get("error"):
            st.error(data["error"])
            return

        # ── tab bar ──
        tab_labels = [
            "📊 Overview",
            "🎯 ATS Analysis",
            "🛠️ Skills",
            "📜 Experience",
            "✨ Quality",
            "💼 Jobs",
            "🎓 Coach"
        ]
        tabs = st.tabs(tab_labels)

        with tabs[0]:
            tab_overview(data)
        with tabs[1]:
            tab_ats(data)
        with tabs[2]:
            tab_skills(data)
        with tabs[3]:
            tab_experience(data)
        with tabs[4]:
            tab_quality(data)
        with tabs[5]:
            tab_jobs(data)
        with tabs[6]:
            tab_coach(data)

    except (RuntimeError, ValueError, FileNotFoundError, OSError) as exc:
        logger.exception("Unexpected application failure")
        st.error("Something went wrong while loading the analyzer.")
        st.caption("Check the server logs for the full traceback.")
        if os.getenv("APP_ENV", "production") != "production":
            st.exception(exc)


if __name__ == "__main__":
    main()