"""
Resume Parser Module
Handles extraction of text from PDF and DOCX resume files.
"""

import PyPDF2
from docx import Document
import streamlit as st


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
    Load job descriptions from a text file with format: [job title]
    
    Args:
        file_path: Path to the job descriptions file
        
    Returns:
        Dictionary with job titles as keys and descriptions as values
    """
    job_descriptions = {}
    current_title = ""
    current_desc = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    if current_title and current_desc:
                        job_descriptions[current_title] = ' '.join(current_desc).strip()
                    current_title = line[1:-1].lower()
                    current_desc = []
                elif current_title:
                    if line:  # Only add non-empty lines
                        current_desc.append(line)

            if current_title and current_desc:
                job_descriptions[current_title] = ' '.join(current_desc).strip()

        return job_descriptions
    
    except FileNotFoundError:
        st.error(f"Job descriptions file not found: {file_path}")
        return {}
    except Exception as e:
        st.error(f"Error loading job descriptions: {str(e)}")
        return {}
