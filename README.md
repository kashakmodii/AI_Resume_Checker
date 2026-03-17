#  AI Resume Checker - Streamlit Edition

An intelligent AI-powered resume analysis tool that evaluates your resume against job descriptions using **Google Gemini API**. Get detailed insights on match score, ATS compatibility, skill gaps, and actionable suggestions to improve your resume.

---

##  Features

-  **Resume Upload**: Support for PDF and DOCX formats
-  **Job Description Input**: Choose from 25+ predefined jobs or paste custom descriptions
-  **AI Analysis**: Google Gemini API for intelligent resume evaluation
-  **Comprehensive Scoring**:
  - Resume Match Score (0-100%)
  - ATS Compatibility Score (0-100%)
-  **Detailed Insights**:
  - Key Strengths
  - Areas for Improvement
  - Missing Critical Skills
  - Keyword Match Analysis
  - Actionable Suggestions
-  **Report Export**: Download analysis as Text or PDF
-  **Clean UI**: Professional Streamlit interface with real-time feedback

---

##  Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend & Backend** | Python + Streamlit |
| **AI Engine** | Google Generative AI (Gemini) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **DOCX Parsing** | python-docx |
| **Report Generation** | fpdf2 |
| **Environment** | python-dotenv |

---

##  Project Structure

```
AI_Resume_Checker/
├── app.py                      # Main Streamlit application
├── resume_parser.py            # PDF/DOCX text extraction
├── ai_analyzer.py              # Google Gemini API integration
├── report_generator.py         # Text/PDF report generation
├── requirements.txt            # Python dependencies
├── .env.example                # Environment configuration template
├── job_description.txt         # Predefined job roles (25+ positions)
├── LICENSE
└── README.md
```

---

##  Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://ai.google.dev))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kashakmodii/AI_Resume_Checker.git
   cd AI_Resume_Checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   The app will open at `http://localhost:8501`

---

##  How to Use

### Step 1: Upload Resume
- Click **"Choose a PDF or DOCX file"** in the sidebar
- Upload your resume in PDF or Word format
- Preview the extracted text to verify accuracy

### Step 2: Provide Job Description
- **Option A**: Select from 25+ predefined job roles
- **Option B**: Paste a custom job description
- View the full job description if needed

### Step 3: Analyze
- Click the **" Analyze Resume"** button
- Wait for Gemini AI to process (5-10 seconds)

### Step 4: Review Results
- **Match Score**: Overall alignment with job requirements
- **ATS Score**: Likelihood of passing Applicant Tracking Systems
- **Strengths**: What you did well
- **Weaknesses**: Areas to improve
- **Missing Skills**: Critical skills to add
- **Keywords**: Important terms from the job found in your resume
- **Suggestions**: Specific actions to improve your match

### Step 5: Download Report
- **Text Format**: Simple, easy-to-read text file
- **PDF Format**: Professional formatted report for sharing

---

##  Predefined Job Roles

The tool includes job descriptions for 25+ positions:

- Data Scientist
- Software Engineer
- Web Developer
- Machine Learning Engineer
- Android Developer
- Data Analyst
- UI/UX Designer
- Network Engineer
- DevOps Engineer
- Cybersecurity Analyst
- Project Manager
- Graphic Designer
- Content Writer
- Marketing Manager
- Accountant
- Human Resources Specialist
- Customer Support Representative
- Mechanical Engineer
- Electrical Engineer
- Civil Engineer
- AI Engineer
- Database Administrator
- Cloud Engineer
- Frontend Developer
- Backend Developer
- Full Stack Developer
- QA Tester

---

##  Configuration

### Using Environment Variables (.env)
```
GEMINI_API_KEY=your_api_key_here
```

### Using Streamlit Secrets (Streamlit Cloud)
For deployment on Streamlit Cloud, add to `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

---

##  Dependencies

```
streamlit==1.28.1
google-generativeai==0.3.0
pymupdf==1.23.8
python-docx==0.8.11
python-dotenv==1.0.0
plotly==5.17.0
fpdf2==2.7.0
```

---


##  Report Export

Generate professional reports in two formats:

### Text Report (.txt)
- Human-readable format
- Easy to share and edit
- Includes all analysis details

### PDF Report (.pdf)
- Professional formatting
- Print-ready
- Perfect for email sharing

---


##  Ready to Improve Your Resume?

Start analyzing your resume now and get actionable insights to land your dream job! 🚀
