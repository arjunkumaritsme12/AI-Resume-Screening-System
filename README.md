# 🎯 AI Resume Screening System

A comprehensive, end-to-end machine learning solution for intelligent resume screening and candidate matching using AI-powered analysis.

## 📋 Project Overview

This system helps HR professionals and recruiters quickly identify the best-fit candidates for job positions by:
- Parsing resume documents (PDF, DOCX, TXT)
- Extracting key information (skills, experience, education, certifications)
- Matching candidates against job requirements
- Ranking candidates with detailed match scores
- Providing actionable insights and recommendations

## ✨ Features

### 🎯 Single Resume Matching
- Match individual resumes against specific job descriptions
- Get detailed match scores and visualizations
- Identify matched and missing skills
- View candidate profile information

### 📊 Batch Processing
- Process multiple resumes simultaneously
- Compare candidates side-by-side
- Export results to CSV
- Rank candidates by match percentage

### 📁 File Support
- **PDF** - Professional resume PDFs
- **DOCX** - Microsoft Word documents
- **TXT** - Plain text files
- **CSV** - Batch resume processing

### 🔍 Advanced Analysis
- **Skills Matching (50%)** - Compares candidate skills with job requirements
- **Experience Matching (35%)** - Evaluates years of experience
- **Education Matching (15%)** - Verifies educational qualifications
- **Contact Information** - Extracts email and phone numbers

### 🎨 Modern UI
- Built with Streamlit for responsive, clean interface
- Interactive visualizations with Plotly
- Real-time analysis and results
- Professional score gauges and charts

## 🏗️ Project Structure

```
resume-screening-ai/
├── app/
│   ├── app.py              # Main Streamlit application
│   ├── resume_parser.py    # Resume parsing logic
│   ├── job_parser.py       # Job description parsing
│   ├── matcher.py          # Candidate matching engine
│   └── utils.py            # Utility functions
├── model/
│   ├── train_model.py      # ML model training script
│   └── *.pkl              # Trained model files (generated after training)
├── data/
│   └── resumes.csv        # Training dataset
├── notebooks/
│   └── exploration.ipynb  # Data exploration and analysis
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- At least 2GB RAM

### Installation

1. **Clone or extract the project**
```bash
cd resume-screening-ai
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

**Start the Streamlit app:**
```bash
cd app
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Training the Model (Optional)

To train the classification model on your data:

```bash
cd model
python train_model.py
```

This will:
- Load resumes from `data/resumes.csv`
- Train an SVM classifier
- Save model files for later use
- Display training accuracy and classification report

## 💡 How to Use

### Single Resume Matching

1. **Navigate to "🎯 Single Match" tab**
2. **Provide Resume:**
   - Paste resume text OR upload a file (PDF/DOCX/TXT)
3. **Provide Job Description:**
   - Paste job description text OR upload a file
4. **Click "🚀 Analyze Match"**
5. **Review Results:**
   - Overall match percentage
   - Matched and missing skills
   - Score breakdown (skills, experience, education)
   - Candidate profile
   - Recommendation

### Batch Processing

1. **Navigate to "📊 Batch Processing" tab**
2. **Upload CSV file** with resumes (required columns: `Resume`)
3. **Paste job description**
4. **Click "🚀 Process Batch"**
5. **View and export results**

### Customizing Scoring

1. **Go to "🔧 Settings" tab**
2. **Adjust weights:**
   - Skills Weight (default: 50%)
   - Experience Weight (default: 35%)
   - Education Weight (default: 15%)
3. **Apply changes**

## 📊 Scoring System

### Overall Score Calculation
```
Overall Score = (Skills Score × 0.50) + 
                (Experience Score × 0.35) + 
                (Education Score × 0.15)
```

### Score Interpretation
- **80-100%** 🟢 Excellent - Highly recommended
- **60-79%** 🟡 Good - Worth considering
- **40-59%** 🔵 Moderate - Potential with training
- **Below 40%** 🔴 Poor - Not recommended

## 🔧 Technical Stack

### Frontend
- **Streamlit** - Interactive web framework
- **Plotly** - Data visualization

### Backend
- **Python 3.8+** - Core language
- **Pandas** - Data processing
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning

### File Processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **Regular Expressions** - Text pattern matching

## 📈 Skills Database

The system recognizes 40+ skills across multiple categories:

**Programming Languages:** Python, Java, JavaScript, C++, C#, Ruby, PHP, Go, Rust

**Data Science:** ML, Deep Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy

**Cloud & DevOps:** AWS, Azure, GCP, Docker, Kubernetes, Jenkins, CI/CD

**Web Technologies:** React, Vue, Angular, Node.js, Express, REST, GraphQL

**Databases:** SQL, PostgreSQL, MongoDB, NoSQL, Cassandra, Hbase

**and more...**

## 🧪 Testing

### Sample Test Data

Create a test with these sample inputs:

**Sample Resume:**
```
John Doe
Software Engineer

Skills: Python, JavaScript, React, AWS, SQL, Machine Learning

Experience: 5 years

Education: Bachelor's in Computer Science

Certifications: AWS Certified Solutions Architect
```

**Sample Job Description:**
```
We are looking for a Senior Software Engineer

Requirements:
- 5+ years of experience
- Proficiency in Python and JavaScript
- React.js experience
- AWS cloud expertise
- Strong SQL knowledge
- Bachelor's degree in Computer Science or related field

Nice to have:
- Machine Learning knowledge
- Docker/Kubernetes experience
```

**Expected Result:** ~85% match score

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: PDF/DOCX files not extracting
**Solution:** Ensure file format is supported and not corrupted
- Try uploading as text instead
- Check file encoding

### Issue: Low match scores despite relevant resumes
**Solution:** Adjust scoring weights in Settings tab

### Issue: Streamlit app won't start
**Solution:** Check Python version and dependencies
```bash
python --version  # Should be 3.8+
pip list          # Verify all packages installed
```

## 📝 Sample CSV Format

For batch processing, use this CSV format:

```csv
Candidate,Resume
John Doe,"Python, Java, 5 years experience..."
Jane Smith,"JavaScript, React, AWS, 3 years..."
Bob Johnson,"Data Scientist, ML, SQL, 7 years..."
```

## 🚦 Supported File Types

| Format | Extension | Max Size | Notes |
|--------|-----------|----------|-------|
| PDF | .pdf | 50MB | Scanned PDFs may not work |
| DOCX | .docx | 50MB | Microsoft Word format |
| TXT | .txt | No limit | Plain text files |
| CSV | .csv | No limit | For batch processing |

## 📊 Output Information

### Resume Data Extracted
- Skills (from predefined database)
- Years of experience
- Email address
- Phone number
- Education degrees
- Certifications

### Job Description Analysis
- Required skills
- Required experience (years)
- Education level
- Job title

### Match Results
- Overall score (0-100%)
- Skills score breakdown
- Experience score breakdown
- Education score breakdown
- Matched skills list
- Missing skills list

## 🔐 Privacy & Data

- All processing happens locally
- No data is sent to external servers
- Files are processed in memory
- No persistent data storage (unless CSV exported)

## 🤝 Contributing

To improve this project:
1. Identify issues or feature requests
2. Create improvements
3. Test thoroughly
4. Document changes

## 📚 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NLP with Python](https://www.nltk.org/)

## 📄 License

This project is open source and available for educational and commercial use.

## 🎯 Roadmap

Future enhancements:
- [ ] Resume format standardization
- [ ] Advanced NLP with transformer models
- [ ] Multi-language support
- [ ] Integration with ATS systems
- [ ] Database backend for results history
- [ ] API endpoints for integration
- [ ] Advanced filtering and search
- [ ] Custom skill database management

## ✅ Version History

### v1.0 (Current)
- Initial release
- Resume and job description parsing
- Basic skill matching algorithm
- Batch processing
- Streamlit UI
- PDF/DOCX/TXT support

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the documentation
3. Test with sample data
4. Check console output for error messages

## 🎓 Educational Value

This project demonstrates:
- Python programming best practices
- NLP and text processing
- Machine learning workflows
- UI/UX design with Streamlit
- File handling in Python
- Data processing with Pandas
- Regular expressions for text parsing

---

**Made with ❤️ for efficient hiring**

Last Updated: 2024
Version: 1.0
