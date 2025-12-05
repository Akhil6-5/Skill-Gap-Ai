import streamlit as st
import re
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------
st.set_page_config(page_title="SkillGapAI — Milestone 2", page_icon="🧭", layout="wide")

# ------------------------------------------
# CUSTOM CSS FOR DASHBOARD LOOK
# ------------------------------------------
st.markdown(
    """
    <style>
    :root { --footer-height: 72px; }

    .main {
        background-color: #020617;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .top-header {
        color: white;
        background: #117A65;
        padding: 18px 20px;
        border-radius: 12px;
        margin-bottom: 18px;
    }
    .top-header h2 {
        margin: 0;
        font-size: 1.6rem;
    }
    .top-header p {
        margin: 4px 0 0 0;
        font-size: 0.95rem;
        opacity: 0.95;
    }

    /* MAIN DASHBOARD CARD */
    .dashboard-card {
        background: #020617;
        border-radius: 22px;
        padding: 20px 24px 26px 24px;
        margin-top: 24px;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.45);
    }

    .skill-chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 0 6px 8px 0;
        border-radius: 999px;
        background: #E8F6F3;
        color: #117A65;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .skill-chip-soft {
        background: #EEF2FF;
        color: #4338CA;
    }

    /* SMALL CHIPS FOR MATCHING / MISSING SKILLS */
    .chip-small {
        display:inline-block;
        padding: 3px 9px;
        margin: 0 5px 6px 0;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid rgba(148,163,184,0.55);
        background: rgba(15,23,42,0.9);
        color: #e5e7eb;
    }
    .chip-missing {
        border-color: rgba(248,113,113,0.7);
        background: rgba(127,29,29,0.8);
        color: #fee2e2;
    }
    .chip-extra {
        border-color: rgba(52,211,153,0.7);
        background: rgba(6,78,59,0.85);
        color: #d1fae5;
    }

    .highlight-box {
        background-color: #020617;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #1f2937;
        font-size: 0.9rem;
        line-height: 1.45;
        color: #e5e7eb;
    }
    .highlight {
        background-color: #65a30d;
        padding: 1px 3px;
        border-radius: 4px;
    }

    .metric-box {
        background-color: #020617;
        padding: 10px 12px;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #1f2937;
        margin:8px;
        box-sizing: border-box;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #9CA3AF;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F9FAFB;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #6B7280;
        margin-top: 2px;
    }

    .detail-row {
        background-color: #020617;
        border-radius: 12px;
        padding: 8px 10px 12px 10px;  /* extra bottom padding for bar */
        margin-bottom: 12px;
        border: 1px solid #1f2937;
    }
    .detail-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #E5E7EB;
    }
    .detail-subtitle {
        font-size: 0.75rem;
        color: #9CA3AF;
    }
    .detail-score {
        font-size: 0.85rem;
        font-weight: 600;
        color: #22c55e;
    }

    /* inline skill progress bar (keeps bar inside the detail-card) */
    .skill-bar {
        width: 100%;
        height: 10px;
        background: rgba(255,255,255,0.04);
        border-radius: 8px;
        margin-top: 12px;
        overflow: hidden;
        border: 1px solid rgba(31,41,55,0.6);
    }
    .skill-bar-fill {
        height: 100%;
        background: linear-gradient(90deg,#3b82f6,#06b6d4);
        width: 0%;
        transition: width 0.6s ease;
    }

    /* SUMMARY STRIP */
    .summary-strip {
        margin-top: 10px;
        margin-bottom: 10px;
        padding: 10px 12px;
        border-radius: 12px;
        background: rgba(15,23,42,0.95);
        border: 1px solid rgba(55,65,81,0.8);
    }

    /* Footer: appear only at page end (static, visually compact) */
    .app-footer {
        position: relative;                      /* static in flow so it's only visible at page bottom */
        margin: 32px auto 48px;                  /* space above and below the footer */
        max-width: calc(100% - 40px);            /* inset from page edges for nicer look */
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg,#06b6d4 0%, #3b82f6 100%);
        color: #ffffff;
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(3,7,18,0.45);
        z-index: 9999;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(3px);
    }
    .app-footer .left, .app-footer .right {
        display:flex;
        align-items:center;
        gap:12px;
    }
    .app-footer .center {
        flex: 1;
        text-align:center;
        font-size:13px;
        color: rgba(255,255,255,0.95);
    }
    .app-footer .left em { font-style: normal; font-weight:700; font-size:15px; }

    /* Keep a small trailing padding so the footer doesn't sit glued to content */
    section[data-testid="stAppViewContainer"] .block-container,
    .stApp main .block-container,
    .reportview-container .main {
        padding-bottom: 20px !important;
    }

    /* Mobile adjustments */
    @media (max-width: 900px) {
        .app-footer {
            max-width: calc(100% - 24px);
            margin: 18px auto 24px;
            flex-direction: column;
            gap:6px;
            padding:10px;
            text-align:center;
        }
        .app-footer .center { order:3; width:100%; }
    }

    /* Dark text areas */
    .stTextArea, textarea {
        background: #020617 !important;
        border-radius: 12px !important;
        border: 1px solid #1f2937 !important;
        color: white !important;
    }
    div[data-baseweb="base-input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Banner inside the big rounded box */
.dashboard-banner {
    background: #020617;  /* same as card background */
    border-radius: 999px;
    padding: 10px 18px;
    border: 1px solid rgba(148,163,184,0.45);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------
# PAGE HEADER
# ------------------------------------------
st.markdown(
    f"""
    <div style='text-align:center;margin-top:-40px;margin-bottom:70px'>
      <div style='display:inline-flex;align-items:center;gap:12px'>
        <div style='width:45px;height:45px;margin:0 auto;border-radius:12px;
                        display:flex;align-items:center;justify-content:center;
                        background:linear-gradient(135deg,#06b6d4,#3b82f6);color:#fff;
                        font-weight:800;box-shadow:0 6px 18px rgba(0,0,0,0.08);'>SG</div>
        <h1 style='font-size:40px;margin:0;font-weight:800;display:inline-block;vertical-align:middle;color:white'>AI Skill Gap Analyzer</h1>
      </div>
      <div style='font-size:17px;color:#9CA3AF;margin-top:2px'>
        Instantly compare resumes to job descriptions — highlight missing skills & export results
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

TEXT_COLOR = "#F9FAFB"
MUTED = "#9CA3AF"

# ------------------------------------------
# LOAD SPACY MODEL
# ------------------------------------------
# ------------------------------------------
# SKILL LISTS
# ------------------------------------------
technical_skills = [
    "python", "java", "c++", "sql", "html", "css", "javascript", "react", "node.js",
    "tensorflow", "pytorch", "machine learning", "data analysis", "data visualization",
    "aws", "azure", "gcp", "power bi", "tableau", "django", "flask", "scikit-learn", "nlp"
]

soft_skills = [
    "communication", "leadership", "teamwork", "problem solving", "time management",
    "adaptability", "critical thinking", "creativity", "collaboration", "decision making"
]

# ------------------------------------------
# HELPERS
# ------------------------------------------
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return text.lower().strip()

def extract_skills(text):
    text_clean = clean_text(text)
    found_tech = [skill.title() for skill in technical_skills if skill in text_clean]
    found_soft = [skill.title() for skill in soft_skills if skill in text_clean]
    return list(set(found_tech)), list(set(found_soft))

def highlight_text(text: str, skills):
    if not text:
        return ""
    highlighted = text
    for skill in sorted(skills, key=len, reverse=True):
        pattern = re.compile(re.escape(skill), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f"<span class='highlight'>{m.group(0)}</span>",
            highlighted,
        )
    highlighted = highlighted.replace("\n", "<br>")
    return highlighted

def skill_confidences(skills):
    n = len(skills)
    if n == 0:
        return {}
    start = 96
    step = 10 / max(n - 1, 1)
    conf = {}
    for i, s in enumerate(skills):
        conf[s] = max(75, round(start - i * step))
    return conf

# ------------------------------------------
# SESSION STATE FOR LAST UPDATED
# ------------------------------------------
if "last_updated" not in st.session_state:
    st.session_state["last_updated"] = "Not analyzed yet"

# ------------------------------------------
# INPUT SECTION (COLLAPSIBLE)
# ------------------------------------------
with st.expander("✏️ Input: Paste Resume & Job Description Text", expanded=False):
    col_r, col_j = st.columns(2)
    with col_r:
        st.markdown("#### 👨‍💻 Resume Text")
        resume_text = st.text_area("Paste Resume Content Here:", "", height=250)
    with col_j:
        st.markdown("#### 🏢 Job Description Text")
        jd_text = st.text_area("Paste Job Description Content Here:", "", height=250)

has_any_text = bool(resume_text or jd_text)

# Extract skills
tech_resume, soft_resume = ([], [])
tech_jd, soft_jd = ([], [])

if resume_text:
    tech_resume, soft_resume = extract_skills(resume_text)
if jd_text:
    tech_jd, soft_jd = extract_skills(jd_text)

# Sets for comparison
resume_all_skills = set(tech_resume + soft_resume)
jd_all_skills = set(tech_jd + soft_jd)
common_skills = sorted(resume_all_skills & jd_all_skills)
missing_in_resume = sorted(jd_all_skills - resume_all_skills)
extra_in_resume = sorted(resume_all_skills - jd_all_skills)

# Update last updated only when analysis has some skills/text
if has_any_text and (tech_resume or soft_resume or tech_jd or soft_jd):
    st.session_state["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ------------------------------------------
# DASHBOARD CARD
# ------------------------------------------
with st.container():
    # Banner inside the rounded box
    st.markdown(
        """
        <div class="dashboard-banner">
          <div>
            <div style="font-size:1.1rem;font-weight:700;color:#F9FAFB; ">
              Skill Extraction Interface
            </div>
            <div style="font-size:0.85rem;color:#9CA3AF;margin-top:2px;">
              View skills, confidence scores, and resume-JD gaps at a glance.
            </div>
          </div>
          <div>
            <span style="
              display:inline-block;
              padding:4px 12px;
              border-radius:999px;
              font-size:0.8rem;
              background:rgba(15,23,42,0.9);
              color:#e5e7eb;
              border:1px solid rgba(148,163,184,0.6);
            ">
              Milestone 2 • Skill Extraction
            </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top row: Left (skills + highlighted text) / Right (chart + metrics)
    left_col, right_col = st.columns([1.4, 1.1])

    # --------------------------------------------------
    # LEFT COLUMN - RESUME SKILLS PANEL
    # --------------------------------------------------
    with left_col:
        st.markdown("#### 📄 Resume Skills", unsafe_allow_html=True)

        source = st.radio(
            "Source",
            options=["Resume", "Job Description"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if source == "Resume":
            src_text = resume_text
            src_tech = tech_resume
            src_soft = soft_resume
            src_name = "Resume"
        else:
            src_text = jd_text
            src_tech = tech_jd
            src_soft = soft_jd
            src_name = "Job Description"

        all_src_skills = src_tech + src_soft

        st.markdown("##### 🏷️ Skill Tags")

        if not src_text:
            st.info(f"Paste {src_name} text in the input section above to see skills.")
        elif not all_src_skills:
            st.warning(f"No configured skills were detected in the {src_name.lower()} text.")
        else:
            conf = skill_confidences(all_src_skills)
            chips_html = ""

            for skill in src_tech:
                score = conf.get(skill, 90)
                chips_html += f"<span class='skill-chip'>{skill} {score}%</span>"

            for skill in src_soft:
                score = conf.get(skill, 88)
                chips_html += f"<span class='skill-chip skill-chip-soft'>{skill} {score}%</span>"

            st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown("##### ✏️ Highlighted Text")

        if src_text:
            highlighted_html = highlight_text(src_text, all_src_skills)
            st.markdown(
                f"<div class='highlight-box'>{highlighted_html}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div class='highlight-box'>No text available yet. Paste content in the input section to see highlighted skills.</div>",
                unsafe_allow_html=True,
            )

    # --------------------------------------------------
    # RIGHT COLUMN - DISTRIBUTION + METRICS + DETAILS
    # --------------------------------------------------
    with right_col:
        st.markdown("#### 📊 Skill Distribution")

        if not has_any_text:
            st.info("Provide Resume and/or Job Description text to view charts.")
        else:
            tech_selected = src_tech
            soft_selected = src_soft
            all_selected = tech_selected + soft_selected

            tech_count = len(tech_selected)
            soft_count = len(soft_selected)
            total_count = tech_count + soft_count

            conf = skill_confidences(all_selected)
            avg_conf = round(sum(conf.values()) / len(conf)) if conf else 0

            if total_count > 0:
                fig, ax = plt.subplots(figsize=(3.5, 3.5))
                sizes = [tech_count, soft_count]
                labels = ["Technical Skills", "Soft Skills"]
                wedges, _ = ax.pie(
                    sizes,
                    labels=None,
                    startangle=90,
                    wedgeprops=dict(width=0.35, edgecolor="white"),
                )
                ax.axis("equal")
                ax.legend(
                    wedges,
                    labels,
                    loc="lower center",
                    bbox_to_anchor=(0.5, -0.12),
                    ncol=2,
                    fontsize=8,
                )
                st.pyplot(fig, use_container_width=True)
            else:
                st.write("No skills detected yet for a chart.")

            m1, m2 = st.columns(2)
            with m1:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Technical Skills</div>
                        <div class="metric-value">{tech_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with m2:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Soft Skills</div>
                        <div class="metric-value">{soft_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            m3, m4 = st.columns(2)
            with m3:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Total Skills</div>
                        <div class="metric-value">{total_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with m4:
                st.markdown(
                    f"""
                    <div class="metric-box">
                        <div class="metric-label">Avg. Confidence</div>
                        <div class="metric-value">{avg_conf}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # -------- Resume vs JD Summary strip --------
            if resume_all_skills or jd_all_skills:
                st.markdown("#### 🔍 Resume vs JD Summary", unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="summary-strip">
                        <div style="display:flex;flex-wrap:wrap;gap:14px;font-size:0.85rem;">
                            <div>Overlap: <strong>{len(common_skills)}</strong> skills</div>
                            <div>Missing in Resume (present in JD): <strong>{len(missing_in_resume)}</strong></div>
                            <div>Extra in Resume (not in JD): <strong>{len(extra_in_resume)}</strong></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if common_skills:
                    st.markdown("**Matching skills**", unsafe_allow_html=True)
                    chips = "".join([f"<span class='chip-small'>{s}</span>" for s in common_skills])
                    st.markdown(chips, unsafe_allow_html=True)

                cols_gap = st.columns(2)
                with cols_gap[0]:
                    st.markdown("**Missing in Resume (from JD)**", unsafe_allow_html=True)
                    if missing_in_resume:
                        chips = "".join([f"<span class='chip-small chip-missing'>{s}</span>" for s in missing_in_resume])
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='font-size:0.8rem;color:#9CA3AF;'>No missing skills detected.</span>", unsafe_allow_html=True)

                with cols_gap[1]:
                    st.markdown("**Extra in Resume**", unsafe_allow_html=True)
                    if extra_in_resume:
                        chips = "".join([f"<span class='chip-small chip-extra'>{s}</span>" for s in extra_in_resume])
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='font-size:0.8rem;color:#9CA3AF;'>No extra skills detected.</span>", unsafe_allow_html=True)

            # Detailed skills section
            st.markdown("#### 📋 Detailed Skills")

            if not all_selected:
                st.write("No individual skills to display yet.")
            else:
                for skill in all_selected:
                    score = conf.get(skill, 85)
                    is_tech = skill in tech_selected
                    type_label = "Technical Skill" if is_tech else "Soft Skill"

                    st.markdown(
                        f"""
                        <div class="detail-row">
                          <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                              <div class="detail-title">{skill}</div>
                              <div class="detail-subtitle">{type_label}</div>
                            </div>
                            <div class="detail-score">{score}%</div>
                          </div>

                          <div class="skill-bar" role="progressbar" aria-valuenow="{score}" aria-valuemin="0" aria-valuemax="100">
                            <div class="skill-bar-fill" style="width:{score}%;"></div>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------
# FOOTER
# ------------------------------------------
last_updated_str = st.session_state.get("last_updated", "Not analyzed yet")

st.markdown(
    f"""
    <div class="app-footer" role="contentinfo" aria-label="App footer">
      <div class="left">
        <div style="color:rgba(255,255,255,0.98);"><em>AI Skill Gap Analyzer — Milestone 2</em></div>
      </div>
      <div class="center">
        Version: {st.session_state.get('app_version','1.0.0')} • Developed by Balu Karthik
      </div>
      <div class="right" style="color:rgba(255,255,255,0.95); font-size:14px;">
        Last updated: {last_updated_str}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)