# AI_Resume_Checker
AI Resume Checker is an intelligent system that evaluates a candidate’s resume against predefined job descriptions and provides a match percentage based on content relevance. It leverages Natural Language Processing (NLP) techniques, such as TF-IDF and cosine similarity, to perform semantic comparison between resumes and job roles.

How It Works

Select job title (from the ones available in job_description.txt)

Upload your resume (PDF format)


The system:

Extracts text from the resume

Uses TF-IDF to vectorize both job and resume text

Calculates cosine similarity to measure match percentage

Returns the matching score


Technologies Used

Python 

NLP: NLTK, scikit-learn

PyPDF2 (for reading resumes)

TF-IDF and Cosine Similarity




