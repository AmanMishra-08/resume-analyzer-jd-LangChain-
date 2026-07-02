# Frontend 
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
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#4F46E5;
}

.sub-title{
    font-size:18px;
    color:gray;
}

.section{
    padding:20px;
    border-radius:12px;
    background-color:#f7f7f7;
    margin-bottom:20px;
}

.stButton>button{
    width:100%;
    height:55px;
    font-size:18px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<p class="main-title">💼 AI Interview Preparation Assistant</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Upload your resume and paste the job description to receive AI-powered interview preparation.</p>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Two Columns
# -----------------------------
col1, col2 = st.columns(2)

# =============================
# LEFT SIDE
# =============================
with col1:

    st.subheader("📄 Upload Resume")

    uploaded_resume = st.file_uploader(
        "Choose your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_resume:
        st.success("✅ Resume uploaded successfully!")

# =============================
# RIGHT SIDE
# =============================
with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the Job Description",
        height=300,
        placeholder="""
Example:

Frontend Developer

Required Skills:
• React
• JavaScript
• Git
• REST APIs
• Docker
"""
    )

st.divider()

# -----------------------------
# Analyze Button
# -----------------------------
analyze = st.button("🚀 Analyze Resume")

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

            # Extract Resume
            resume_text = extract_resume_text(uploaded_resume)

            # AI Analysis
            success, analysis = analyze_resume(resume_text, job_description)

        if success:
            st.success("Analysis Completed!")
            st.markdown("---")
            st.subheader("📊 AI Analysis")
            st.markdown(analysis)
        else:
            st.error(f"Analysis failed: {analysis}")
    


