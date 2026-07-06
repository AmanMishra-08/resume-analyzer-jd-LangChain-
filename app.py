import streamlit as st
from backend.resume_parser import extract_resume_text
from backend.analyzer import analyze_resume

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# Custom CSS — Professional/Corporate Theme
# -----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #0f1419;
}

.hero {
    padding: 40px 30px;
    border-radius: 16px;
    background: #000000;
    border: 1px solid #1f2937;
    margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.hero-title {
    font-size: 36px;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 16px;
    color: #94a3b8;
    font-weight: 400;
    max-width: 600px;
    line-height: 1.5;
}

.badge {
    display: inline-block;
    background-color: #1e2b3d;
    color: #64748b;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
    border: 1px solid #2d3748;
}

.step-card {
    background-color: #161b22;
    border: 1px solid #2d3748;
    border-left: 4px solid #64748b;
    border-radius: 12px;
    padding: 20px;
    text-align: left;
    height: 100%;
}

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: #334155;
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}

.step-title {
    font-size: 15px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 4px;
}

.step-desc {
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.4;
}

.section-card {
    background-color: #161b22;
    border: 1px solid #2d3748;
    border-left: 4px solid #3b82f6;
    border-radius: 12px;
    padding: 24px;
    height: 100%;
}

.section-heading {
    font-size: 17px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 4px;
}

.section-subtext {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 16px;
}

.stButton > button {
    width: 100%;
    height: 52px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    background-color: #000000;
    color: #ffffff;
    border: 1px solid #2d3748;
    transition: background-color 0.2s ease;
}

.stButton > button:hover {
    background-color: #1a1a1a;
    border: 1px solid #475569;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Header
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="badge">AI-Powered</div>
    <div class="hero-title"> AI Interview Preparation Assistant</div>
    <div class="hero-subtitle">
        Upload your resume and paste a job description to get an instant match score,
        skill gap analysis, and interview readiness insights — powered by LLaMA 3.1.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# How It Works
# -----------------------------
step_col1, step_col2, step_col3 = st.columns(3)

steps = [
    ("1", "Upload Your Resume", "Add your resume as a PDF file."),
    ("2", "Paste Job Description", "Copy the JD you're applying for."),
    ("3", "Get Instant Analysis", "Receive your match score and skill breakdown."),
]

for col, (num, title, desc) in zip([step_col1, step_col2, step_col3], steps):
    with col:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------
# Two Columns — Upload & JD
# -----------------------------
col1, col2 = st.columns(2)

# =============================
# LEFT SIDE
# =============================
with col1:
    st.markdown("""
    <div class="section-card">
        <div class="section-heading">📄 Upload Resume</div>
        <div class="section-subtext">PDF format only, max 200MB</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader(
        "Choose your Resume (PDF)",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_resume:
        st.success("✅ Resume uploaded successfully!")

# =============================
# RIGHT SIDE
# =============================
with col2:
    st.markdown("""
    <div class="section-card">
        <div class="section-heading">💼 Job Description</div>
        <div class="section-subtext">Paste the full job posting text</div>
    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "Paste the Job Description",
        height=250,
        label_visibility="collapsed",
        placeholder="Example:\n\nFrontend Developer\n\nRequired Skills:\n- React\n- JavaScript\n- Git\n- REST APIs\n- Docker"
    )

st.write("")
st.divider()

# -----------------------------
# Analyze Button
# -----------------------------
analyze = st.button(" Analyze Resume")

# -----------------------------
# AI Analysis
# -----------------------------
if analyze:

    if uploaded_resume is None:
        st.error("Please upload your resume.")

    elif job_description.strip() == "":
        st.error("Please paste the Job Description.")

    else:

        with st.spinner("Analyzing Resume..."):
            resume_text = extract_resume_text(uploaded_resume)
            success, analysis = analyze_resume(resume_text, job_description)

        if success:
            st.success("Analysis Completed!")
            st.markdown("---")
            st.subheader("📊 Match Score")

            overall = analysis.get("overall_match_score", 0)
            st.markdown(f"### {overall}% Match")
            st.progress(overall / 100)
            st.caption(analysis.get("summary", ""))

            st.markdown("---")
            st.subheader("🔍 Category Breakdown")

            categories = analysis.get("categories", {})
            labels = {
                "technical_skills": "🧠 Technical Skills",
                "soft_skills": "🤝 Soft Skills",
                "experience_level": "📈 Experience Level",
                "tools_frameworks": "🛠️ Tools & Frameworks"
            }

            cols = st.columns(2)
            for i, (key, label) in enumerate(labels.items()):
                cat = categories.get(key, {})
                with cols[i % 2]:
                    with st.expander(f"{label} — {cat.get('score', 0)}%", expanded=True):
                        st.progress(cat.get("score", 0) / 100)

                        matched = cat.get("matched", [])
                        missing = cat.get("missing", [])

                        if matched:
                            tags = " ".join(
                                f'<span style="background-color:#22c55e33;color:#22c55e;'
                                f'padding:4px 10px;border-radius:12px;margin:3px;'
                                f'display:inline-block;font-size:13px;">{s}</span>'
                                for s in matched
                            )
                            st.markdown(f"**Matched:**<br>{tags}", unsafe_allow_html=True)

                        if missing:
                            tags = " ".join(
                                f'<span style="background-color:#ef444433;color:#ef4444;'
                                f'padding:4px 10px;border-radius:12px;margin:3px;'
                                f'display:inline-block;font-size:13px;">{s}</span>'
                                for s in missing
                            )
                            st.markdown(f"**Missing:**<br>{tags}", unsafe_allow_html=True)

        else:
            st.error(f"Analysis failed: {analysis}")
