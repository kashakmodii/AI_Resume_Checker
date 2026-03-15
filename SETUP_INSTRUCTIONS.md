# 🚀 AI Resume Checker - Setup Instructions

## ⚡ Quick Start (5 minutes)

### 1. Get Google Gemini API Key
- Visit: https://ai.google.dev
- Click "Get API Key"
- Create a new API key for "AI Resume Checker"
- Copy the key (you'll need it in step 3)

### 2. Install Python Dependencies
```bash
# Navigate to project directory
cd g:\AI_Resume_Checker

# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed streamlit google-generativeai pymupdf python-docx python-dotenv plotly fpdf2
```

### 3. Configure Environment
**Option A: Using .env file (Recommended for local development)**

```bash
# Create .env file from template
copy .env.example .env

# Edit .env file and add your API key
# (or use any text editor to open .env and paste your key)
```

Edit `.env`:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Option B: Using Streamlit Secrets (For Streamlit Cloud)**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

### 4. Run the Application
```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### 5. Open in Browser
- The app automatically opens at: **http://localhost:8501**
- If not, manually navigate to that URL

---

## 📖 First-Time Usage

### Step 1: Upload Your Resume
1. Click "Choose a PDF or DOCX file" in the sidebar
2. Select your resume (PDF or Word document)
3. Wait for extraction and see "✅ Resume uploaded successfully!"
4. (Optional) Click "Preview Resume" to verify text extraction

### Step 2: Select or Enter Job Description
**Option A - Use Predefined Jobs:**
- Select "Select from predefined jobs"
- Choose from 25+ available positions (Data Scientist, Software Engineer, etc.)
- Click the expander to preview the job description

**Option B - Enter Custom Job:**
- Select "Enter custom job description"
- Type or paste the job title
- Paste the full job description in the text area

### Step 3: Analyze
1. Click the **"🔍 Analyze Resume"** button
2. Wait 5-10 seconds while Gemini AI analyzes
3. Green checkmark shows analysis is complete

### Step 4: Review Results
- **Match Score**: How well your resume matches (0-100%)
- **ATS Score**: Likely to pass Applicant Tracking System (0-100%)
- **Green boxes**: Your strengths
- **Yellow boxes**: Areas to improve
- **Red boxes**: Missing critical skills
- **Blue boxes**: Suggestions to improve match
- **Tags**: Keywords from the job found in your resume

### Step 5: Download Report
- Click **"📄 Download as Text"** for a readable report
- Click **"📄 Download as PDF"** for a professional formatted report
- Save to your computer

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "GEMINI_API_KEY not found"
**Solutions:**
1. Check `.env` file exists in project root
2. Verify API key is correctly entered (no extra spaces)
3. Restart Streamlit app (Ctrl+C, then `streamlit run app.py`)
4. For Streamlit Cloud: Check `.streamlit/secrets.toml` has correct key

### Error: "PDF extraction failed"
**Solutions:**
- Ensure PDF is not corrupted
- Try converting PDF to a simpler format
- Ensure PDF is not password-protected
- Use a modern PDF creation tool

### Error: "AI response parsing error"
**Solutions:**
- Check internet connection
- Verify Gemini API quota isn't exceeded
- Try a different resume/job description
- Check that GEMINI_API_KEY is correct

### Error: "Streamlit not found on port 8501"
**Solution:**
- Port 8501 might be in use. Streamlit will try 8502, 8503, etc.
- Or specify different port:
```bash
streamlit run app.py --server.port 8080
```

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| **Python** | 3.8 | 3.10+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk** | 500 MB | 1 GB |
| **Internet** | Required for API | Fast connection |
| **OS** | Windows/Mac/Linux | Any |

---

## 📦 Project Files Explained

```
AI_Resume_Checker/
│
├── app.py
│   └── Main Streamlit application
│       - Handles UI and page layout
│       - Manages user interactions
│       - Displays results
│
├── resume_parser.py
│   └── Resume text extraction module
│       - Extracts text from PDF files
│       - Extracts text from DOCX files
│       - Loads predefined job descriptions
│
├── ai_analyzer.py
│   └── Google Gemini API integration
│       - Connects to Gemini API
│       - Sends resume + job description
│       - Parses JSON response
│       - Validates results
│
├── report_generator.py
│   └── Report generation module
│       - Generates text reports
│       - Generates PDF reports
│       - Formats analysis results
│
├── requirements.txt
│   └── Python dependencies
│       - All packages needed to run
│
├── .env.example
│   └── Environment template
│       - Shows what variables to set
│
├── .gitignore
│   └── Git configuration
│       - Hides sensitive files
│       - Excludes API keys
│
├── job_description.txt
│   └── 25+ predefined job descriptions
│       - Data Scientist, Software Engineer, etc.
│       - Ready to use without typing
│
└── README.md
    └── Complete documentation

```

---

## 🔐 Security Best Practices

1. **Never commit .env file**
   ```bash
   # Already in .gitignore, but be careful
   git status  # Verify .env is not staged
   ```

2. **Keep API key secret**
   - Don't share your .env file
   - Don't paste key in public forums
   - Generate new key if compromised

3. **Use environment variables**
   - Never hardcode API keys in code
   - Always use .env or secrets.toml

4. **For Streamlit Cloud**
   - Use Secrets management (built-in)
   - Never use .env file

---

## 📈 Tips for Better Results

1. **Resume Format**
   - Use clear section headers (Experience, Skills, Education)
   - Keep formatting simple (Gemini reads text, not formatting)
   - Include quantified metrics (e.g., "increased revenue by 20%")

2. **Job Description**
   - Use the full job description if possible
   - Include all requirements and nice-to-haves
   - Better descriptions = better analysis

3. **API Usage**
   - Free tier allows good usage volume
   - Each analysis uses minimal API quota
   - Check your usage at https://ai.google.dev

---

## 🚀 Deployment Options

### Option 1: Local Computer (Simplest)
```bash
pip install -r requirements.txt
streamlit run app.py
```
✅ Easiest  |  ❌ Only accessible from your computer

### Option 2: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add GEMINI_API_KEY to Secrets
5. Deploy!

✅ Publicly accessible  |  ✅ Free tier  |  ✅ Easy updates

### Option 3: Heroku/Railway/Others
See README.md for standard Streamlit deployment guides

---

## 📊 What Gets Analyzed

### Resume Analysis Includes:
- ✅ All text content
- ✅ Skills mentioned
- ✅ Experience and achievements
- ✅ Education and certifications
- ✅ Keywords and phrases

### AI Provides:
- ✅ Overall match percentage (0-100%)
- ✅ ATS compatibility score
- ✅ Key strengths identified
- ✅ Weaknesses to address
- ✅ Missing critical skills
- ✅ Keyword matching
- ✅ 5+ specific suggestions

### Data Privacy:
- ❌ Nothing is stored permanently
- ❌ No data training on your resume
- ✅ Only sent to Gemini API for analysis
- ✅ Your files stay on your computer

---

## ❓ FAQ

**Q: Is my resume data stored?**
A: No. It's sent to Gemini for analysis only, not stored.

**Q: How much does this cost?**
A: Gemini API is free with generous quotas. Check https://ai.google.dev/pricing

**Q: Can I use my own job descriptions?**
A: Yes! Select "Enter custom job description" option.

**Q: What resume formats are supported?**
A: PDF and DOCX (Word documents) only.

**Q: How long does analysis take?**
A: Usually 5-10 seconds depending on resume length.

**Q: Can I run this offline?**
A: No, it requires Google Gemini API (internet connection needed).

**Q: Can I background this?**
A: Yes, you can run on Streamlit Cloud for 24/7 access.

---

## 📞 Need Help?

1. **Check README.md** - Full documentation
2. **Review Troubleshooting** - Common issues
3. **Verify setup** - Confirm all steps completed
4. **Check logs** - Streamlit shows error details

---

## ✅ Setup Checklist

Before using the app:

- [ ] Python 3.8+ installed
- [ ] Google Gemini API key obtained
- [ ] `pip install -r requirements.txt` completed
- [ ] `.env` file created with API key
- [ ] `streamlit run app.py` works
- [ ] App opens at http://localhost:8501
- [ ] You can upload a resume
- [ ] Analysis runs successfully
- [ ] Report downloads work

---

## 🎉 You're All Set!

Start analyzing your resume and get insights to improve your job match!

**Questions?** Check the README.md or review Troubleshooting section above.

Happy job hunting! 🚀
