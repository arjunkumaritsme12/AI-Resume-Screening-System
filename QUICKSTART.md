# Quick Start Guide - AI Resume Screening System

## ⚡ 30-Second Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
cd app
streamlit run app.py
```

### Step 3: Open in Browser
The app will automatically open at `http://localhost:8501`

## 🚀 First-Time Usage

### Test the System
Before using with real data, run the test script:

```bash
python test_system.py
```

This will verify all components are working correctly.

### Try a Sample Match

**Resume Example:**
```
John Smith
Senior Developer

Skills: Python, JavaScript, React, AWS, Docker
Experience: 5 years
Education: Bachelor's in Computer Science
Email: john@example.com
```

**Job Description Example:**
```
Senior Developer Position

Requirements:
- 5+ years development experience
- Python and JavaScript skills
- React experience
- AWS knowledge
- Bachelor's degree preferred
```

**Expected Result:** ~85% match score ✓

## 📖 Using the App

### Single Resume Matching
1. Go to "🎯 Single Match" tab
2. Paste or upload resume
3. Paste or upload job description
4. Click "🚀 Analyze Match"
5. Review scores and recommendations

### Batch Processing
1. Go to "📊 Batch Processing" tab
2. Upload CSV with resumes
3. Paste job description
4. Click "🚀 Process Batch"
5. Download results as CSV

### Customize Scoring
1. Go to "🔧 Settings" tab
2. Adjust weight sliders
3. Click "Apply Weights"

## 📋 CSV Format for Batch

```csv
Candidate,Resume
John Doe,"Python, Java, 5 years..."
Jane Smith,"JavaScript, React, 3 years..."
```

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port 8501 in use | Run `streamlit run app.py --server.port 8502` |
| File upload fails | Ensure file is PDF, DOCX, or TXT format |
| Low scores | Check Settings tab to adjust weights |

## 📁 Important Files

- `app/app.py` - Main application
- `app/resume_parser.py` - Resume parsing
- `app/job_parser.py` - Job description parsing
- `app/matcher.py` - Matching engine
- `requirements.txt` - Dependencies
- `test_system.py` - System test script

## 💡 Tips

- ✓ Use clear, formatted documents for best results
- ✓ Save results as CSV for record keeping
- ✓ Test with sample data first
- ✓ Adjust scoring weights for your needs
- ✓ Use batch mode for multiple candidates

## 🔄 Workflow Example

```
1. Receive job req → Create job description
2. Receive resumes → Use batch processing
3. Review scores → Filter by threshold (e.g., > 70%)
4. Interview top candidates
5. Export results → Share with hiring team
```

## ⚙️ System Requirements

- Python 3.8+
- 2GB RAM minimum
- Internet connection (first run only)
- Modern web browser

## 📞 Need Help?

1. Check README.md for detailed documentation
2. Review console output for error messages
3. Run `test_system.py` to diagnose issues
4. Check file formats and encoding

## 🎯 Common Use Cases

### Quick Screening
- Match single resume: ~2 minutes
- Get instant match score and insights

### Bulk Hiring
- Batch process 100+ resumes: ~5 minutes
- Filter candidates by score threshold
- Export ranked list

### Custom Matching
- Adjust scoring weights for role type
- Emphasize skills for tech roles
- Emphasize experience for senior roles

## ✨ Features Explained

| Feature | What It Does |
|---------|-------------|
| Skills Matching | Compares resume skills with job requirements |
| Experience Scoring | Evaluates years of experience |
| Education Verification | Checks educational qualifications |
| Batch Processing | Handles multiple resumes at once |
| Score Visualization | Shows match scores as gauges and charts |
| CSV Export | Save results for later review |

## 🎓 Learning Path

1. Start with sample data
2. Try single matching
3. Try batch processing
4. Customize scoring weights
5. Export and analyze results

---

**Ready to start?** Run: `streamlit run app/app.py`

Happy screening! 🎯
