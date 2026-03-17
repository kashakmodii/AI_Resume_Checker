"""
AI Resume Checker - Streamlit Application
A complete AI-powered resume analysis tool using Google Gemini API
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Import custom modules
from resume_parser import extract_text_from_upload, load_job_descriptions
from ai_analyzer import analyze_resume_with_gemini, validate_analysis_result
from report_generator import generate_text_report, generate_pdf_report

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Resume Checker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Enterprise Design
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e2e8f0;
        }
        
        [data-testid="stSidebar"] h2 {
            color: #f1f5f9 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        .main {
            background: #f8fafc;
        }
        
        .header-container {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            color: white;
            padding: 2rem 3rem;
            border-radius: 0;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }
        
        .header-container h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        .header-container p {
            font-size: 1.1rem;
            opacity: 0.95;
            font-weight: 500;
        }
        
        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid #0ea5e9;
            display: inline-block;
        }
        
        .metric-card {
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #0ea5e9;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .metric-card h3 {
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .metric-card .value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0ea5e9;
        }
        
        .stMetric {
            background: white !important;
            border-radius: 1rem !important;
            padding: 1.5rem !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
            border-left: 4px solid #0ea5e9 !important;
        }
        
        .stMetric [data-testid="metricDeltaContainer"] {
            display: none;
        }
        
        .result-box {
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #10b981;
        }
        
        .result-box.warning {
            border-left-color: #f59e0b;
        }
        
        .result-box.danger {
            border-left-color: #ef4444;
        }
        
        .result-box.info {
            border-left-color: #0ea5e9;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 0.75rem !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(14, 165, 233, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(14, 165, 233, 0.4) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        .stFileUploader {
            border: 2px dashed #cbd5e1 !important;
            border-radius: 1rem !important;
            padding: 2rem !important;
            background-color: #f1f5f9 !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            border-color: #0ea5e9 !important;
            background-color: #f0f9ff !important;
        }
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stRadio > div {
            border: 1px solid #cbd5e1 !important;
            border-radius: 0.75rem !important;
            padding: 0.75rem !important;
            font-family: inherit !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
        }
        
        .stSuccess {
            background-color: #ecfdf5 !important;
            border-left: 4px solid #10b981 !important;
            border-radius: 0.75rem !important;
            color: #047857 !important;
            padding: 1rem !important;
            border: none !important;
        }
        
        .stWarning {
            background-color: #fffbeb !important;
            border-left: 4px solid #f59e0b !important;
            border-radius: 0.75rem !important;
            color: #92400e !important;
            padding: 1rem !important;
            border: none !important;
        }
        
        .stError {
            background-color: #fef2f2 !important;
            border-left: 4px solid #ef4444 !important;
            border-radius: 0.75rem !important;
            color: #991b1b !important;
            padding: 1rem !important;
            border: none !important;
        }
        
        .stInfo {
            background-color: #f0f9ff !important;
            border-left: 4px solid #0ea5e9 !important;
            border-radius: 0.75rem !important;
            color: #0c4a6e !important;
            padding: 1rem !important;
            border: none !important;
        }
        
        hr {
            border: none !important;
            border-top: 1px solid #e2e8f0 !important;
            margin: 2rem 0 !important;
        }
        
        .progress-section {
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .progress-section .stProgress > div > div {
            background-color: #0ea5e9 !important;
        }
        
        .keyword-badge {
            display: inline-block;
            background: #dbeafe;
            color: #0c4a6e;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = None
    if 'selected_job_title' not in st.session_state:
        st.session_state.selected_job_title = None
    if 'job_descriptions' not in st.session_state:
        st.session_state.job_descriptions = load_job_descriptions('job_description.txt')


def render_sidebar():
    """Render the sidebar with input controls."""
    with st.sidebar:
        st.markdown("## 📋 Resume Analysis Setup")
        st.markdown("---")
        
        # Resume Upload Section
        st.markdown("### 📄 Your Resume")
        st.markdown("*Upload in PDF or DOCX format*")
        resume_file = st.file_uploader(
            "Choose file",
            type=["pdf", "docx"],
            help="Supported formats: PDF, DOCX (Limit: 200MB)",
            label_visibility="collapsed"
        )
        
        if resume_file:
            try:
                st.session_state.resume_text = extract_text_from_upload(resume_file)
                st.success(f"✅ Loaded: {resume_file.name}")
                
                with st.expander("👁️ Preview"):
                    preview = st.session_state.resume_text[:200] + "..." if len(st.session_state.resume_text) > 200 else st.session_state.resume_text
                    st.caption(preview)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.resume_text = None
        
        st.markdown("---")
        
        # Job Description Section
        st.markdown("### 💼 Job Description")
        st.markdown("*Select from template or enter custom*")
        
        job_titles = sorted(st.session_state.job_descriptions.keys()) if st.session_state.job_descriptions else []
        
        # Show status
        if job_titles:
            st.success(f"✅ Found {len(job_titles)} positions")
        else:
            st.warning("⚠️ Templates not loaded")
        
        source = st.radio(
            "Source:",
            ["Template Library", "Custom Entry"],
            key="job_source"
        )
        
        if source == "Template Library":
            if job_titles:
                selected_job = st.selectbox(
                    "Position:",
                    job_titles,
                    key="job_select"
                )
                st.session_state.selected_job_title = selected_job
                st.session_state.job_description = st.session_state.job_descriptions[selected_job]
                
                with st.expander("📖 View Description"):
                    st.text_area(
                        "Description",
                        st.session_state.job_description,
                        height=150,
                        disabled=True,
                        key="job_preview"
                    )
            else:
                st.info("💡 No templates available. Please use Custom Entry below.")
                st.session_state.selected_job_title = st.text_input("Title:", key="custom_title_1")
                st.session_state.job_description = st.text_area("Description:", height=150, key="custom_desc_1")
        else:
            st.session_state.selected_job_title = st.text_input(
                "Position Title:",
                value=st.session_state.selected_job_title or "",
                key="custom_title_2"
            )
            st.session_state.job_description = st.text_area(
                "Paste Description:",
                value=st.session_state.job_description or "",
                height=150,
                key="custom_desc_2"
            )
        
        st.markdown("---")
        
        # Analyze Button
        if st.button("🚀 Analyze Resume", type="primary", use_container_width=True, key="analyze"):
            if not st.session_state.resume_text:
                st.error("Upload resume first")
            elif not st.session_state.job_description:
                st.error("Add job description")
            else:
                with st.spinner("🔄 Analyzing..."):
                    st.session_state.analysis_result = analyze_resume_with_gemini(
                        st.session_state.resume_text,
                        st.session_state.job_description,
                        st.session_state.selected_job_title or ""
                    )
                    if st.session_state.analysis_result:
                        if validate_analysis_result(st.session_state.analysis_result):
                            st.success("✅ Analysis complete!")
                        else:
                            st.warning("⚠️ Some data incomplete")


def render_results():
    """Render the analysis results in the main area."""
    if st.session_state.analysis_result is None:
        # Welcome Header
        st.markdown("""
            <div class="header-container">
                <h1>📊 Resume AI Analyzer</h1>
                <p>Powered by Google Gemini AI - Professional Resume-to-Job Matching</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Features Grid
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="result-box info">
                <h3>📈 Match Score</h3>
                <p>See how well your resume aligns with job requirements</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="result-box info">
                <h3>🎯 ATS Compatibility</h3>
                <p>Check if your resume passes Applicant Tracking Systems</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="result-box info">
                <h3>💡 Actionable Insights</h3>
                <p>Get specific recommendations to improve your application</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### How to Use")
        st.markdown("""
        1. **Upload Resume** - Use the sidebar to upload your resume (PDF or DOCX)
        2. **Select Job** - Choose from 27+ job templates or paste a custom description
        3. **Analyze** - Click the Analyze button to start the AI review
        4. **Review Results** - Get detailed matching analysis and suggestions
        5. **Download Report** - Export your analysis as PDF or TXT
        """)
        return
    
    # Results Header
    match_score = st.session_state.analysis_result.get('match_score', 0)
    ats_score = st.session_state.analysis_result.get('ats_score', 0)
    
    st.markdown("""
        <div class="header-container">
            <h1>📊 Your Analysis Results</h1>
            <p>Detailed AI-powered resume matching and recommendations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Resume Match Score",
            f"{match_score}%",
            help="How well your resume matches the job"
        )
        st.progress(match_score / 100)
    
    with col2:
        st.metric(
            "ATS Compatibility",
            f"{ats_score}%",
            help="How likely resume passes ATS systems"
        )
        st.progress(ats_score / 100)
    
    st.markdown("---")
    
    # Overall Assessment
    st.markdown('<span class="section-header">📝 Overall Assessment</span>', unsafe_allow_html=True)
    st.info(st.session_state.analysis_result.get('overall_summary', 'No summary'))
    
    st.markdown("---")
    
    # Strengths
    st.markdown('<span class="section-header">✅ Your Strengths</span>', unsafe_allow_html=True)
    strengths = st.session_state.analysis_result.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.markdown(f"""
            <div class="result-box">
                <strong>✓ {strength}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No strengths identified")
    
    st.markdown("---")
    
    # Areas for Improvement
    st.markdown('<span class="section-header">⚠️ Areas for Improvement</span>', unsafe_allow_html=True)
    weaknesses = st.session_state.analysis_result.get('weaknesses', [])
    if weaknesses:
        for weakness in weaknesses:
            st.markdown(f"""
            <div class="result-box warning">
                <strong>! {weakness}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No major weaknesses")
    
    st.markdown("---")
    
    # Missing Critical Skills
    st.markdown('<span class="section-header">🚨 Missing Critical Skills</span>', unsafe_allow_html=True)
    missing_skills = st.session_state.analysis_result.get('missing_skills', [])
    if missing_skills:
        for skill in missing_skills:
            st.markdown(f"""
            <div class="result-box danger">
                <strong>✗ {skill}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No critical missing skills")
    
    st.markdown("---")
    
    # Keyword Matching
    st.markdown('<span class="section-header">🔑 Keyword Match Analysis</span>', unsafe_allow_html=True)
    keywords = st.session_state.analysis_result.get('keyword_match', [])
    if keywords:
        keyword_html = " ".join([f'<span class="keyword-badge">{kw}</span>' for kw in keywords[:15]])
        st.markdown(f'<div>{keyword_html}</div>', unsafe_allow_html=True)
    else:
        st.info("No matching keywords found")
    
    st.markdown("---")
    
    # Suggestions
    st.markdown('<span class="section-header">💡 Actionable Recommendations</span>', unsafe_allow_html=True)
    suggestions = st.session_state.analysis_result.get('suggestions', [])
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            st.info(f"**{i}.** {suggestion}")
    else:
        st.info("No specific suggestions available")
    
    st.markdown("---")
    
    # Download Reports
    st.markdown('<span class="section-header">📥 Export Analysis</span>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        text_report = generate_text_report(
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.selected_job_title or "General",
            st.session_state.analysis_result
        )
        st.download_button(
            "📄 Download as Text",
            data=text_report,
            file_name="resume_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        pdf = generate_pdf_report(
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.selected_job_title or "General",
            st.session_state.analysis_result
        )
        if pdf:
            pdf_bytes = pdf.output()
            st.download_button(
                "📄 Download as PDF",
                data=pdf_bytes,
                file_name="resume_analysis.pdf",
                mime="application/pdf",
                use_container_width=True
            )


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Render layout
    render_sidebar()
    
    # Main content area
    render_results()


if __name__ == "__main__":
    main()
