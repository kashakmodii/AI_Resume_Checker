# 🎯 API Resume Checker - Complete Reference

## 📁 Project Files Summary

### Core Application Files

| File | Purpose | Key Components |
|------|---------|-----------------|
| **app.py** | Main Streamlit UI | Sidebar input, results dashboard, report download |
| **resume_parser.py** | Resume text extraction | PDF/DOCX parsing, job description loader |
| **ai_analyzer.py** | Gemini API integration | API setup, prompt engineering, response parsing |
| **report_generator.py** | Report generation | Text & PDF report formatting |

### Configuration Files

| File | Purpose |
|------|---------|
| **requirements.txt** | Python package dependencies |
| **.env.example** | Environment variable template |
| **.env** | Your local API key (create this) |
| **job_description.txt** | 25+ predefined job descriptions |
| **.streamlit/config.toml** | Streamlit UI configuration |
| **.gitignore** | Files to exclude from git |

### Documentation

| File | Purpose |
|------|---------|
| **README.md** | Complete project documentation |
| **SETUP_INSTRUCTIONS.md** | Step-by-step setup guide |
| **QUICK_REFERENCE.md** | This file - quick lookup |

---

## 🚀 Running the Application

### First Time Setup (5 minutes)
```bash
# 1. Get API key from https://ai.google.dev
# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
copy .env.example .env

# 4. Edit .env and paste your API key
# GEMINI_API_KEY=your_key_here

# 5. Run the app
streamlit run app.py
```

### Subsequent Runs
```bash
cd g:\AI_Resume_Checker
streamlit run app.py
```

---

## 📊 Application Features

### Input Section (Sidebar)
- 📄 **Resume Upload**: PDF or DOCX file
- 💼 **Job Description**: Select from 25+ or enter custom
- 🔍 **Analyze Button**: Start AI analysis

### Results Section (Main Area)
- 📈 **Match Score**: Resume alignment %
- 🤖 **ATS Score**: Applicant Tracking System score
- ✅ **Strengths**: What you did well
- ⚠️ **Weaknesses**: Areas to improve
- 🚨 **Missing Skills**: Critical gaps
- 🔑 **Keywords**: Job terms found in resume
- 💡 **Suggestions**: Actionable improvements
- 📥 **Download**: Text or PDF report

---

## 🔑 Data Flow

```
User Resume (PDF/DOCX)
        ↓
[resume_parser.py]
        ↓
Extract Raw Text
        ↓
User Job Description
        ↓
[ai_analyzer.py]
        ↓
Call Gemini API
        ↓
Parse JSON Response
        ↓
[app.py - Display Results]
        ↓
[report_generator.py - Generate Report]
        ↓
User Downloads Report (Text/PDF)
```

---

## 🛠️ Key Technologies

| Library | Version | Purpose |
|---------|---------|---------|
| Streamlit | 1.28.1 | Web UI framework |
| google-generativeai | 0.3.0 | Gemini API client |
| pymupdf | 1.23.8 | PDF text extraction |
| python-docx | 0.8.11 | DOCX text extraction |
| python-dotenv | 1.0.0 | Environment variables |
| fpdf2 | 2.7.0 | PDF generation |

---

## 📋 Available Job Roles

The app includes 25+ predefined job descriptions:

```
• Data Scientist            • Project Manager
• Software Engineer         • Graphic Designer
• Web Developer            • Content Writer
• ML Engineer              • Marketing Manager
• Android Developer        • Accountant
• Data Analyst             • HR Specialist
• UI/UX Designer           • Customer Support
• Network Engineer         • Mechanical Engineer
• DevOps Engineer          • Electrical Engineer
• Cybersecurity Analyst    • Civil Engineer
• AI Engineer              • Database Admin
• Cloud Engineer           • Frontend Developer
• Backend Developer        • Full Stack Developer
• QA Tester
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=your_api_key_here
```

### Streamlit Config (.streamlit/config.toml)
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
textColor = "#262730"

[server]
maxUploadSize = 200       # MB
enableXsrfProtection = true
```

---

## 🔧 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| API key not found | Create .env file with GEMINI_API_KEY |
| PDF extraction error | Try different PDF or convert format |
| Port 8501 in use | `streamlit run app.py --server.port 8080` |
| Response parsing error | Check internet, verify API key |
| Module import error | Verify all packages in requirements.txt |

---

## 💾 File Sizes

```
app.py                 ~12 KB   (Main application)
resume_parser.py       ~4 KB    (Resume extraction)
ai_analyzer.py         ~6 KB    (API integration)
report_generator.py    ~5 KB    (Report generation)
job_description.txt    ~8 KB    (Job descriptions)
requirements.txt       ~0.3 KB  (Dependencies list)
```

---

## 🎯 Common Tasks

### Add a New Job Description
Edit `job_description.txt`:
```
[new job title]
Job description text here...
Keywords and requirements...
```

### Change UI Colors
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#new_color"
backgroundColor = "#new_color"
```

### Export Different Formats
See `report_generator.py`:
- `generate_text_report()` - Text format
- `generate_pdf_report()` - PDF format

### Debug API Issues
Check `ai_analyzer.py`:
- `setup_gemini_api()` - API setup
- `analyze_resume_with_gemini()` - Main analysis
- `validate_analysis_result()` - Response validation

---

## 📊 Analysis Output Example

```json
{
  "match_score": 78,
  "ats_score": 65,
  "strengths": [
    "Strong Python skills",
    "Cloud experience",
    "Problem solving"
  ],
  "weaknesses": [
    "Limited metrics",
    "Weak leadership",
    "Missing Docker/K8s"
  ],
  "missing_skills": [
    "Docker",
    "Kubernetes",
    "CI/CD"
  ],
  "keyword_match": [
    "Python",
    "AWS",
    "REST APIs",
    "Git",
    "Agile"
  ],
  "suggestions": [
    "Add quantified achievements",
    "Include DevOps tools",
    "Emphasize metrics"
  ],
  "overall_summary": "Good match with room for improvement in DevOps skills..."
}
```

---

## 🔐 Security Notes

- ✅ API key stored locally in .env
- ✅ Never commit .env to git
- ✅ Use .env in .gitignore (already there)
- ✅ For Streamlit Cloud, use Secrets tab
- ✅ No data storage on servers
- ✅ Communications encrypted

---

## 📈 API Costs

- **Gemini API**: Free tier available
- **Free quota**: Sufficient for most use
- **Check usage**: https://ai.google.dev/dashboard
- **Paid tiers**: Available for higher volume

---

## 🆘 Error Messages & Solutions

### "GEMINI_API_KEY not found"
```
1. Create .env file: copy .env.example .env
2. Edit .env with your actual key
3. Restart streamlit
```

### "ModuleNotFoundError: No module named 'streamlit'"
```
pip install -r requirements.txt
```

### "Failed to extract text from PDF"
```
1. Verify PDF is not corrupted
2. Try online PDF converter
3. Ensure it's not password protected
4. Try a different PDF
```

### "Could not parse Gemini response as JSON"
```
1. Check internet connection
2. Verify API key is valid
3. Try different resume/job description
4. Wait a moment and retry
```

---

## 📖 Documentation Files

- **README.md** - Full project documentation
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide
- **QUICK_REFERENCE.md** - Quick lookup (this file)

---

## 🎯 Next Steps

1. ✅ Run: `streamlit run app.py`
2. ✅ Upload your resume
3. ✅ Select a job description
4. ✅ Click Analyze
5. ✅ Review results
6. ✅ Download report
7. ✅ Improve your resume!

---

## 📞 Support Resources

- Check README.md for comprehensive docs
- Review SETUP_INSTRUCTIONS.md for detailed steps
- Check .streamlit/logs for error details
- Verify all dependencies: `pip list`

---

**Last Updated**: March 2026
**Version**: 1.0 (Streamlit Edition)
**Status**: ✅ Complete and Ready to Use
