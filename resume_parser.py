"""
Resume Parser Module
Handles extraction of text from PDF and DOCX resume files.
"""

import PyPDF2
from docx import Document
import streamlit as st
import os
from pathlib import Path


def extract_text_from_pdf(file_input):
    """
    Extract text from a PDF file.
    
    Args:
        file_input: Path to the PDF file or file-like object (UploadedFile)
        
    Returns:
        Extracted text as string
        
    Raises:
        Exception: If PDF parsing fails
    """
    try:
        text = ""
        # Check if it's a file path or file-like object
        if isinstance(file_input, str):
            with open(file_input, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        else:
            # Handle Streamlit UploadedFile or file-like objects
            reader = PyPDF2.PdfReader(file_input)
            for page in reader.pages:
                text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_input):
    """
    Extract text from a DOCX (Word) file.
    
    Args:
        file_input: Path to the DOCX file or file-like object (UploadedFile)
        
    Returns:
        Extracted text as string
        
    Raises:
        Exception: If DOCX parsing fails
    """
    try:
        # Check if it's a file path or file-like object
        if isinstance(file_input, str):
            doc = Document(file_input)
        else:
            # Handle Streamlit UploadedFile or file-like objects
            doc = Document(file_input)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_upload(uploaded_file):
    """
    Extract text from an uploaded resume file (PDF or DOCX).
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Extracted text as string
        
    Raises:
        ValueError: If file format is not supported
        Exception: If text extraction fails
    """
    try:
        if uploaded_file.type == "application/pdf":
            with st.spinner("🔄 Extracting text from PDF..."):
                return extract_text_from_pdf(uploaded_file)
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            with st.spinner("🔄 Extracting text from Word document..."):
                return extract_text_from_docx(uploaded_file)
        
        else:
            raise ValueError(f"Unsupported file type: {uploaded_file.type}. Please upload PDF or DOCX.")
    
    except Exception as e:
        raise Exception(f"Failed to extract resume text: {str(e)}")


def load_job_descriptions(file_path):
    """
    Load job descriptions from a text file with format: Job Title: description
    Robust path handling for local development and Streamlit deployment
    
    Args:
        file_path: Path to the job descriptions file
        
    Returns:
        Dictionary with job titles as keys and descriptions as values
    """
    job_descriptions = {}

    try:
        # Try multiple path resolution strategies
        possible_paths = [
            file_path,  # Direct path as given
            Path(file_path),  # Using pathlib
            Path(__file__).parent / file_path,  # Relative to this module
        ]
        
        # Add current working directory variants
        cwd = Path.cwd()
        possible_paths.extend([
            cwd / file_path,
            cwd / "job_description.txt",  # Default filename
        ])
        
        # Try to find the file
        actual_path = None
        for p in possible_paths:
            if isinstance(p, str):
                p = Path(p)
            if p.exists():
                actual_path = p
                break
        
        if actual_path is None:
            return job_descriptions
            
        with open(actual_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            
            current_title = ""
            current_desc = []
            
            for line in lines:
                line_stripped = line.strip()
                
                # Check if this line is a job title (ends with colon)
                if line_stripped and ':' in line_stripped and not line_stripped.startswith('#'):
                    # Save previous job if exists
                    if current_title and current_desc:
                        job_descriptions[current_title] = ' '.join(current_desc).strip()
                    
                    # Parse new job title
                    parts = line_stripped.split(':', 1)
                    current_title = parts[0].strip()
                    current_desc = []
                    
                    # If there's text after the colon on the same line, add it
                    if len(parts) > 1 and parts[1].strip():
                        current_desc.append(parts[1].strip())
                
                elif line_stripped and current_title:
                    # Add to current description
                    current_desc.append(line_stripped)
            
            # Don't forget the last job
            if current_title and current_desc:
                job_descriptions[current_title] = ' '.join(current_desc).strip()

        return job_descriptions
    
    except Exception as e:
        return {}
