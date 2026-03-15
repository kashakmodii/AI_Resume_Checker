"""
Report Generator Module
Generates text and PDF reports from analysis results.
"""

from datetime import datetime
from fpdf import FPDF
import streamlit as st


def generate_text_report(resume_text, job_description, job_title, analysis_result):
    """
    Generate a text-based report of the resume analysis.
    
    Args:
        resume_text: Extracted resume text
        job_description: Job description text
        job_title: Job title being applied for
        analysis_result: Dictionary with analysis results
        
    Returns:
        String containing formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("AI RESUME ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Job Position: {job_title.upper() if job_title else 'Not Specified'}")
    
    # Scores Section
    report.append("\n" + "=" * 80)
    report.append("MATCH SCORES")
    report.append("=" * 80)
    report.append(f"Resume Match Score: {analysis_result.get('match_score', 'N/A')}%")
    report.append(f"ATS Compatibility Score: {analysis_result.get('ats_score', 'N/A')}%")
    
    # Overall Summary
    report.append("\n" + "=" * 80)
    report.append("OVERALL ASSESSMENT")
    report.append("=" * 80)
    report.append(analysis_result.get('overall_summary', 'No summary available'))
    
    # Strengths
    report.append("\n" + "=" * 80)
    report.append("STRENGTHS (What You Did Well)")
    report.append("=" * 80)
    strengths = analysis_result.get('strengths', [])
    for i, strength in enumerate(strengths, 1):
        report.append(f"{i}. {strength}")
    if not strengths:
        report.append("No strengths identified.")
    
    # Weaknesses
    report.append("\n" + "=" * 80)
    report.append("WEAKNESSES (Areas for Improvement)")
    report.append("=" * 80)
    weaknesses = analysis_result.get('weaknesses', [])
    for i, weakness in enumerate(weaknesses, 1):
        report.append(f"{i}. {weakness}")
    if not weaknesses:
        report.append("No major weaknesses identified.")
    
    # Missing Skills
    report.append("\n" + "=" * 80)
    report.append("MISSING SKILLS (Critical to Add)")
    report.append("=" * 80)
    missing_skills = analysis_result.get('missing_skills', [])
    for i, skill in enumerate(missing_skills, 1):
        report.append(f"{i}. {skill}")
    if not missing_skills:
        report.append("No critical missing skills identified.")
    
    # Keyword Match
    report.append("\n" + "=" * 80)
    report.append("KEYWORD MATCH (JD Keywords Found in Resume)")
    report.append("=" * 80)
    keywords = analysis_result.get('keyword_match', [])
    for i, keyword in enumerate(keywords, 1):
        report.append(f"{i}. {keyword}")
    if not keywords:
        report.append("No matching keywords found.")
    
    # Suggestions
    report.append("\n" + "=" * 80)
    report.append("ACTION ITEMS (How to Improve)")
    report.append("=" * 80)
    suggestions = analysis_result.get('suggestions', [])
    for i, suggestion in enumerate(suggestions, 1):
        report.append(f"{i}. {suggestion}")
    if not suggestions:
        report.append("No specific suggestions available.")
    
    # Footer
    report.append("\n" + "=" * 80)
    report.append("End of Report")
    report.append("=" * 80)
    
    return "\n".join(report)


def generate_pdf_report(resume_text, job_description, job_title, analysis_result):
    """
    Generate a PDF report of the resume analysis.
    
    Args:
        resume_text: Extracted resume text
        job_description: Job description text
        job_title: Job title being applied for
        analysis_result: Dictionary with analysis results
        
    Returns:
        PDF object or None if generation fails
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "AI RESUME ANALYSIS REPORT", ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(0, 5, f"Job Position: {job_title.upper() if job_title else 'Not Specified'}", ln=True)
        
        # Scores
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "MATCH SCORES", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, f"Resume Match Score: {analysis_result.get('match_score', 'N/A')}%", ln=True)
        pdf.cell(0, 5, f"ATS Compatibility Score: {analysis_result.get('ats_score', 'N/A')}%", ln=True)
        
        # Overall Summary
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "OVERALL ASSESSMENT", ln=True)
        pdf.set_font("Helvetica", "", 10)
        summary = analysis_result.get('overall_summary', 'No summary available')
        pdf.multi_cell(0, 5, summary)
        
        # Strengths
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "STRENGTHS", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for strength in analysis_result.get('strengths', []):
            pdf.multi_cell(0, 5, f"• {strength}")
        
        # Weaknesses
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "WEAKNESSES", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for weakness in analysis_result.get('weaknesses', []):
            pdf.multi_cell(0, 5, f"• {weakness}")
        
        # Missing Skills
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "MISSING SKILLS", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for skill in analysis_result.get('missing_skills', []):
            pdf.multi_cell(0, 5, f"• {skill}")
        
        # Suggestions
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "ACTION ITEMS", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for suggestion in analysis_result.get('suggestions', []):
            pdf.multi_cell(0, 5, f"• {suggestion}")
        
        return pdf
    
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None
