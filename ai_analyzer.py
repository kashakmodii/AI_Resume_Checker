"""
AI Analyzer Module
Integrates Google Gemini API to analyze resume vs job description match.
"""

import json
import re
import streamlit as st
import google.generativeai as genai


def setup_gemini_api(api_key):
    """
    Initialize Gemini API with the provided API key.
    
    Args:
        api_key: Google Gemini API key
        
    Returns:
        True if setup successful, False otherwise
    """
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {str(e)}")
        return False


def get_available_model():
    """
    Get the best available Gemini model for this API key.
    
    Returns:
        Model name string
    """
    try:
        # List available models
        models = genai.list_models()
        model_names = [m.name for m in models]
        
        # Prefer flash models, then pro models
        preferences = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]
        
        for pref in preferences:
            if pref in model_names:
                return pref.replace('models/', '')
        
        # If no preference matches, use the first available
        if model_names:
            return model_names[0].replace('models/', '')
        
        # Fallback default
        return 'gemini-pro'
    
    except Exception:
        # Safe fallback
        return 'gemini-pro'


def get_api_key():
    """
    Retrieve Gemini API key from Streamlit secrets or environment.
    
    Returns:
        API key string or None
    """
    try:
        # Try to get from Streamlit secrets first
        try:
            if hasattr(st, 'secrets'):
                secrets_key = st.secrets.get('GEMINI_API_KEY', None)
                if secrets_key:
                    return secrets_key
        except Exception:
            pass  # Secrets file doesn't exist, continue to env var
        
        # Fallback to environment variable
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found. Please configure it in .env or Streamlit secrets.")
            return None
        
        return api_key
    
    except Exception as e:
        st.error(f"Error retrieving API key: {str(e)}")
        return None


def analyze_resume_with_gemini(resume_text, job_description, job_title=""):
    """
    Send resume and job description to Gemini for analysis.
    
    Args:
        resume_text: Extracted resume text
        job_description: Job description text
        job_title: Optional job title for context
        
    Returns:
        Dictionary with analysis results or None if failed
    """
    try:
        api_key = get_api_key()
        if not api_key or not setup_gemini_api(api_key):
            return None

        # Get the best available model for this API key
        model_name = get_available_model()
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Analyze the resume against the job description and provide a detailed JSON response.

JOB TITLE: {job_title if job_title else "Not specified"}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Analyze and return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
  "match_score": <0-100 integer>,
  "ats_score": <0-100 integer>,
  "strengths": [<list of 3-5 key strengths found>],
  "weaknesses": [<list of 3-5 areas for improvement>],
  "missing_skills": [<list of 3-5 critical skills not mentioned>],
  "keyword_match": [<list of 5-10 important keywords from job description found in resume>],
  "suggestions": [<list of 3-5 actionable suggestions to improve match>],
  "overall_summary": "<1-2 sentence overall assessment>"
}}

IMPORTANT: Return ONLY the JSON object, nothing else."""

        with st.spinner("🤖 Analyzing with Google Gemini..."):
            response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Try to parse JSON directly
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if '```json' in response_text:
                json_str = response_text.split('```json')[1].split('```')[0].strip()
                result = json.loads(json_str)
                return result
            elif '```' in response_text:
                json_str = response_text.split('```')[1].split('```')[0].strip()
                result = json.loads(json_str)
                return result
            else:
                # Try to find JSON object in the response
                match = re.search(r'\{[\s\S]*\}', response_text)
                if match:
                    result = json.loads(match.group())
                    return result
                else:
                    st.error("❌ Could not parse Gemini response as JSON")
                    return None
    
    except Exception as e:
        st.error(f"❌ Error during AI analysis: {str(e)}")
        return None


def validate_analysis_result(result):
    """
    Validate that analysis result has all required fields.
    
    Args:
        result: Dictionary from analysis
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(result, dict):
        return False
    
    required_keys = ['match_score', 'ats_score', 'strengths', 'weaknesses', 
                     'missing_skills', 'keyword_match', 'suggestions', 'overall_summary']
    
    for key in required_keys:
        if key not in result:
            return False
    
    # Validate score ranges
    if not (0 <= result.get('match_score', -1) <= 100):
        return False
    if not (0 <= result.get('ats_score', -1) <= 100):
        return False
    
    return True
