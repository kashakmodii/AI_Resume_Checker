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

# Custom CSS - Professional Design
st.markdown("""
    <style>
        * {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main {
            padding: 2rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a237e 0%, #283593 100%);
            color: white;
        }
        
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: white !important;
        }
        
        .stMetric {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            color: white;
            border: none;
        }
        
        .stMetric [data-testid="metricContainer"] {
            color: white;
        }
        
        .stMetric [data-testid="metricDelta"] {
            color: rgba(255, 255, 255, 0.8);
        }
        
        .header-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1.5rem;
            letter-spacing: -1px;
        }
        
        .analysis-header {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.75rem;
        }
        
        .stSuccess {
            background-color: #d4edda !important;
            border-left: 5px solid #28a745 !important;
            border-radius: 0.5rem;
        }
        
        .stWarning {
            background-color: #fff3cd !important;
            border-left: 5px solid #ffc107 !important;
            border-radius: 0.5rem;
        }
        
        .stError {
            background-color: #f8d7da !important;
            border-left: 5px solid #dc3545 !important;
            border-radius: 0.5rem;
        }
        
        .stInfo {
            background-color: #d1ecf1 !important;
            border-left: 5px solid #17a2b8 !important;
            border-radius: 0.5rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            border-radius: 0.5rem !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border: 2px solid #667eea !important;
            border-radius: 0.5rem !important;
            padding: 0.75rem !important;
        }
        
        .stFileUploader {
            border: 2px dashed #667eea !important;
            border-radius: 1rem !important;
            padding: 2rem !important;
            background-color: rgba(102, 126, 234, 0.05) !important;
        }
        
        .welcome-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2.5rem;
            border-radius: 1.5rem;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
        }
        
        .welcome-box h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        .welcome-box ul {
            font-size: 1.1rem;
            line-height: 1.8;
            list-style: none;
            padding-left: 0;
        }
        
        .welcome-box li {
            margin-bottom: 0.8rem;
            padding-left: 2rem;
            position: relative;
        }
        
        .welcome-box li:before {
            content: "✓";
            position: absolute;
            left: 0;
            font-weight: bold;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 0.5rem;
            border-radius: 0.25rem;
        }
        
        hr {
            border: none;
            border-top: 2px solid #667eea !important;
            margin: 2rem 0 !important;
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
        # Header
        st.markdown("---")
        st.markdown("## 📋 **INPUT SECTION**")
        st.markdown("---")
        
        # Resume Upload
        st.markdown("### 📄 Upload Resume")
        st.markdown("*Choose a PDF or DOCX file*")
        resume_file = st.file_uploader(
            "Resume file",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or Word format (Max 200MB)",
            label_visibility="collapsed"
        )
        
        if resume_file:
            try:
                st.session_state.resume_text = extract_text_from_upload(resume_file)
                st.success("✅ Resume uploaded successfully!")
                
                # Show preview
                with st.expander("👀 Preview Resume"):
                    preview_text = st.session_state.resume_text[:300] + "..." if len(st.session_state.resume_text) > 300 else st.session_state.resume_text
                    st.text(preview_text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.resume_text = None
        
        st.markdown("---")
        
        # Job Description Input
        st.markdown("### 💼 Job Description")
        st.markdown("*Select or enter job details*")
        
        # Load job descriptions from file
        job_titles = sorted(st.session_state.job_descriptions.keys()) if st.session_state.job_descriptions else []
        
        # Option to select from predefined jobs or enter custom
        input_method = st.radio(
            "Choose job description source:",
            ["Select from predefined jobs", "Enter custom job description"],
            key="job_source_radio"
        )
        
        if input_method == "Select from predefined jobs":
            if job_titles:
                selected_job = st.selectbox(
                    "📚 Available Positions:",
                    job_titles,
                    help="Choose from available job descriptions",
                    key="job_select"
                )
                st.session_state.selected_job_title = selected_job
                st.session_state.job_description = st.session_state.job_descriptions[selected_job]
                
                with st.expander("📖 View Full Job Description"):
                    st.text_area(
                        "Job Description",
                        st.session_state.job_description,
                        height=200,
                        disabled=True,
                        key="job_desc_preview"
                    )
            else:
                st.warning("⚠️ No predefined job descriptions found.")
                st.info("💡 Please enter a custom job description below or check the job_description.txt file.")
                # Allow custom entry even if no predefined jobs
                st.session_state.selected_job_title = st.text_input(
                    "Job Title (optional):",
                    value=st.session_state.selected_job_title or "",
                    help="Enter the job title you're applying for",
                    key="custom_job_title_1"
                )
                st.session_state.job_description = st.text_area(
                    "Paste job description here:",
                    value=st.session_state.job_description or "",
                    height=200,
                    help="Paste the full job description",
                    key="custom_job_desc_1"
                )
        
        else:
            st.session_state.selected_job_title = st.text_input(
                "Job Title (optional):",
                value=st.session_state.selected_job_title or "",
                help="Enter the job title you're applying for",
                key="custom_job_title_2"
            )
            st.session_state.job_description = st.text_area(
                "Paste job description here:",
                value=st.session_state.job_description or "",
                height=200,
                help="Paste the full job description",
                key="custom_job_desc_2"
            )
        
        st.markdown("---")
        
        # Analyze Button
        st.markdown("### 🚀 Analyze Resume")
        if st.button("🔍 Start Analysis", type="primary", use_container_width=True, key="analyze_btn"):
            if not st.session_state.resume_text:
                st.error("❌ Please upload a resume first")
            elif not st.session_state.job_description:
                st.error("❌ Please provide a job description")
            else:
                st.session_state.analysis_result = analyze_resume_with_gemini(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    st.session_state.selected_job_title or ""
                )
                
                if st.session_state.analysis_result:
                    if validate_analysis_result(st.session_state.analysis_result):
                        st.success("✅ Analysis complete! Scroll down to see results.")
                    else:
                        st.warning("⚠️ Analysis returned but some fields may be incomplete.")


def render_results():
    """Render the analysis results in the main area."""
    if st.session_state.analysis_result is None:
        # Welcome Section
        st.markdown("""
            <div class="header-title">🎯 AI Resume Checker</div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="welcome-box">
                <h1>Welcome to Your Resume Analysis Tool! 👋</h1>
                <p>Powered by Google Gemini AI, this tool analyzes how well your resume matches job descriptions.</p>
                
                <h2 style="margin-top: 1.5rem; font-size: 1.3rem;">How It Works:</h2>
                <ul>
                    <li>📄 Upload your resume (PDF or DOCX)</li>
                    <li>💼 Provide a job description (select from templates or paste your own)</li>
                    <li>🤖 Let Gemini AI analyze the match</li>
                    <li>📊 Review detailed results and suggestions</li>
                    <li>📥 Download a comprehensive report</li>
                </ul>
                
                <h2 style="margin-top: 1.5rem; font-size: 1.3rem;">Key Features:</h2>
                <ul>
                    <li>✅ Resume Match Score</li>
                    <li>✅ ATS Compatibility Score</li>
                    <li>✅ Skills Gap Analysis</li>
                    <li>✅ Keyword Matching</li>
                    <li>✅ Actionable Suggestions</li>
                    <li>✅ Professional Report Export</li>
                </ul>
                
                <p style="margin-top: 1.5rem; font-size: 1.1rem;"><strong>👈 Use the sidebar to get started!</strong></p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Analysis Results Layout
    st.markdown('<div class="header-title">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Resume Match Score",
            f"{st.session_state.analysis_result.get('match_score', 'N/A')}%",
            delta=None,
            help="How well your resume matches the job description"
        )
        st.progress(st.session_state.analysis_result.get('match_score', 0) / 100)
    
    with col2:
        st.metric(
            "ATS Compatibility Score",
            f"{st.session_state.analysis_result.get('ats_score', 'N/A')}%",
            delta=None,
            help="How likely your resume will pass ATS (Applicant Tracking System)"
        )
        st.progress(st.session_state.analysis_result.get('ats_score', 0) / 100)
    
    # Overall Summary
    st.markdown('<div class="analysis-header">📝 Overall Assessment</div>', unsafe_allow_html=True)
    st.info(st.session_state.analysis_result.get('overall_summary', 'No summary available'))
    
    # Strengths (Green - Success)
    st.markdown('<div class="analysis-header">✅ Your Strengths</div>', unsafe_allow_html=True)
    strengths = st.session_state.analysis_result.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.success(f"✓ {strength}")
    else:
        st.info("No strengths identified.")
    
    # Weaknesses (Yellow - Warning)
    st.markdown('<div class="analysis-header">⚠️ Areas for Improvement</div>', unsafe_allow_html=True)
    weaknesses = st.session_state.analysis_result.get('weaknesses', [])
    if weaknesses:
        for weakness in weaknesses:
            st.warning(f"! {weakness}")
    else:
        st.info("No major weaknesses identified.")
    
    # Missing Skills (Red - Error)
    st.markdown('<div class="analysis-header">🚨 Missing Critical Skills</div>', unsafe_allow_html=True)
    missing_skills = st.session_state.analysis_result.get('missing_skills', [])
    if missing_skills:
        for skill in missing_skills:
            st.error(f"✗ {skill}")
    else:
        st.info("No critical missing skills.")
    
    # Keyword Match
    st.markdown('<div class="analysis-header">🔑 Keyword Match</div>', unsafe_allow_html=True)
    keywords = st.session_state.analysis_result.get('keyword_match', [])
    if keywords:
        cols = st.columns(min(3, len(keywords)))
        for i, keyword in enumerate(keywords):
            with cols[i % len(cols)]:
                st.write(f"🏷️ **{keyword}**")
    else:
        st.info("No matching keywords found.")
    
    # Suggestions (Blue - Info)
    st.markdown('<div class="analysis-header">💡 Actionable Suggestions</div>', unsafe_allow_html=True)
    suggestions = st.session_state.analysis_result.get('suggestions', [])
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            st.info(f"{i}. {suggestion}")
    else:
        st.info("No specific suggestions available.")
    
    # Download Report Section
    st.markdown("---")
    st.markdown('<div class="analysis-header">📥 Download Report</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate Text Report
        text_report = generate_text_report(
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.selected_job_title or "General",
            st.session_state.analysis_result
        )
        st.download_button(
            label="📄 Download as Text",
            data=text_report,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Generate PDF Report
        pdf = generate_pdf_report(
            st.session_state.resume_text,
            st.session_state.job_description,
            st.session_state.selected_job_title or "General",
            st.session_state.analysis_result
        )
        if pdf:
            pdf_bytes = pdf.output()
            st.download_button(
                label="📄 Download as PDF",
                data=pdf_bytes,
                file_name="resume_analysis_report.pdf",
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
