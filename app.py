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

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .analysis-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
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
        st.markdown("## 📋 Input Section")
        
        # Resume Upload
        st.markdown("### 📄 Upload Resume")
        resume_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=["pdf", "docx"],
            help="Upload your resume in PDF or Word format"
        )
        
        if resume_file:
            try:
                st.session_state.resume_text = extract_text_from_upload(resume_file)
                st.success("✅ Resume uploaded successfully!")
                
                # Show preview
                with st.expander("👀 Preview Resume (first 500 chars)"):
                    st.text_area(
                        "Resume Preview",
                        st.session_state.resume_text[:500] + "..." if len(st.session_state.resume_text) > 500 else st.session_state.resume_text,
                        height=150,
                        disabled=True
                    )
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.session_state.resume_text = None
        
        # Job Description Input
        st.markdown("### 💼 Job Description")
        
        # Load job descriptions from file
        job_titles = sorted(st.session_state.job_descriptions.keys())
        
        # Option to select from predefined jobs or enter custom
        input_method = st.radio(
            "Choose job description source:",
            ["Select from predefined jobs", "Enter custom job description"]
        )
        
        if input_method == "Select from predefined jobs":
            if job_titles:
                selected_job = st.selectbox(
                    "Select a job role:",
                    job_titles,
                    help="Choose from available job descriptions"
                )
                st.session_state.selected_job_title = selected_job
                st.session_state.job_description = st.session_state.job_descriptions[selected_job]
                
                with st.expander("📖 View Job Description"):
                    st.text_area(
                        "Job Description",
                        st.session_state.job_description,
                        height=200,
                        disabled=True
                    )
            else:
                st.error("❌ No job descriptions found in job_description.txt")
        
        else:
            st.session_state.selected_job_title = st.text_input(
                "Job Title (optional):",
                value=st.session_state.selected_job_title or "",
                help="Enter the job title you're applying for"
            )
            st.session_state.job_description = st.text_area(
                "Paste job description here:",
                value=st.session_state.job_description or "",
                height=200,
                help="Paste the full job description"
            )
        
        # Analyze Button
        st.markdown("### 🚀 Analyze")
        if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
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
        st.markdown("""
            <div class="header-title">🎯 AI Resume Checker</div>
            
            ### Welcome! 👋
            
            This tool uses Google Gemini AI to analyze how well your resume matches a job description.
            
            **How it works:**
            1. 📄 Upload your resume (PDF or DOCX)
            2. 💼 Provide a job description (select from templates or paste your own)
            3. 🤖 Let Gemini AI analyze the match
            4. 📊 Review detailed results and suggestions
            5. 📥 Download a comprehensive report
            
            **Features:**
            - ✅ Resume Match Score
            - ✅ ATS Compatibility Score
            - ✅ Skills Gap Analysis
            - ✅ Keyword Matching
            - ✅ Actionable Suggestions
            - ✅ Professional Report Export
            
            Use the sidebar to get started!
        """, unsafe_allow_html=True)
        return
    
    # Analysis Results Layout
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
