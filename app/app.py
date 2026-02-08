"""
AI Resume Screening System
A comprehensive application for resume screening and candidate matching.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path
import pickle
import io
from resume_parser import ResumeParser
from job_parser import JobDescriptionParser
from matcher import CandidateRanker
from utils import extract_from_file, is_resume, is_job_description, validate_text
import plotly.graph_objects as go
import plotly.express as px

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    .score-high {
        color: #28a745;
        font-weight: bold;
    }
    .score-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .score-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INITIALIZATION ============
if 'parser' not in st.session_state:
    st.session_state.parser = ResumeParser()
    st.session_state.job_parser = JobDescriptionParser()
    st.session_state.ranker = CandidateRanker()
    st.session_state.results = []
    st.session_state.job_data = None

# ============ HELPER FUNCTIONS ============
def get_score_color(score):
    """Return color class based on score."""
    if score >= 75:
        return "score-high"
    elif score >= 50:
        return "score-medium"
    else:
        return "score-low"


def create_score_gauge(score, title="Match Score"):
    """Create a gauge chart for score visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': title},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "#f8d7da"},
                {'range': [25, 50], 'color': "#fff3cd"},
                {'range': [50, 75], 'color': "#d4edda"},
                {'range': [75, 100], 'color': "#c3e6cb"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=0)
    )
    return fig


def create_skills_comparison(matched_skills, missing_skills, all_skills):
    """Create a visualization comparing skills."""
    skills_data = {
        'Matched': len(matched_skills),
        'Missing': len(missing_skills),
        'Extra': len(all_skills) - len(matched_skills)
    }
    
    fig = go.Figure(data=[
        go.Bar(
            y=list(skills_data.keys()),
            x=list(skills_data.values()),
            orientation='h',
            marker=dict(
                color=['#28a745', '#dc3545', '#007bff']
            )
        )
    ])
    
    fig.update_layout(
        title="Skills Breakdown",
        xaxis_title="Count",
        height=300,
        margin=dict(l=20, r=20, t=30, b=0)
    )
    return fig

def render_tag(label):
    """Render a small inline tag/badge for a skill or keyword."""
    st.markdown(
        f"<span style='background-color:#e6f2ff;border-radius:6px;padding:4px 8px;margin:2px;display:inline-block'>{label}</span>",
        unsafe_allow_html=True,
    )


def extract_file_content(uploaded_file):
    """Extract text content from uploaded file."""
    try:
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension == '.pdf':
            text = extract_from_file(uploaded_file, 'pdf')
        elif file_extension == '.docx':
            text = extract_from_file(uploaded_file, 'docx')
        elif file_extension == '.txt':
            text = extract_from_file(uploaded_file, 'txt')
        else:
            return None, f"Unsupported file type: {file_extension}"
        
        if not text or len(text) < 100:
            return None, "File contains too little text"
        
        return text, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"


# ============ HEADER ============
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📄 AI Resume Screening System")
    st.markdown("*Match candidates with job requirements using AI-powered analysis*")

with col2:
    st.markdown("")
    st.info("v1.0 | Powered by ML")

st.divider()

# ============ MAIN NAVIGATION ============
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Single Match",
    "📊 Batch Processing",
    "🔧 Settings",
    "ℹ️ About"
])

# ============ TAB 1: SINGLE MATCH ============
with tab1:
    st.header("Resume to Job Description Matching")
    st.markdown("Upload or paste a resume and job description to find the match score.")
    
    col1, col2 = st.columns(2)
    
    # RESUME INPUT
    with col1:
        st.subheader("📋 Resume Input")
        
        resume_input_method = st.radio(
            "How would you like to provide the resume?",
            ["Paste Text", "Upload File"],
            key="resume_input_method"
        )
        
        resume_text = ""
        
        if resume_input_method == "Paste Text":
            resume_text = st.text_area(
                "Paste resume text here",
                height=300,
                placeholder="Paste your resume content...",
                key="resume_text_area"
            )
        else:
            resume_file = st.file_uploader(
                "Upload resume (PDF, DOCX, or TXT)",
                type=['pdf', 'docx', 'txt'],
                key="resume_file"
            )
            if resume_file:
                text, error = extract_file_content(resume_file)
                if error:
                    st.error(error)
                else:
                    resume_text = text
                    st.success(f"✓ File uploaded: {resume_file.name}")
                    st.text_area(
                        "Extracted resume content",
                        value=resume_text,
                        height=200,
                        disabled=True
                    )
    
    # JOB DESCRIPTION INPUT
    with col2:
        st.subheader("💼 Job Description Input")
        
        jd_input_method = st.radio(
            "How would you like to provide the job description?",
            ["Paste Text", "Upload File"],
            key="jd_input_method"
        )
        
        job_text = ""
        
        if jd_input_method == "Paste Text":
            job_text = st.text_area(
                "Paste job description here",
                height=300,
                placeholder="Paste the job description...",
                key="job_text_area"
            )
        else:
            jd_file = st.file_uploader(
                "Upload job description (PDF, DOCX, or TXT)",
                type=['pdf', 'docx', 'txt'],
                key="job_file"
            )
            if jd_file:
                text, error = extract_file_content(jd_file)
                if error:
                    st.error(error)
                else:
                    job_text = text
                    st.success(f"✓ File uploaded: {jd_file.name}")
                    st.text_area(
                        "Extracted job description",
                        value=job_text,
                        height=200,
                        disabled=True
                    )
    
    st.divider()
    
    # ANALYSIS BUTTON
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        analyze_btn = st.button("🚀 Analyze Match", use_container_width=True, type="primary")
    
    with col2:
        clear_btn = st.button("🔄 Clear All", use_container_width=True)
    
    if clear_btn:
        st.session_state.results = []
        st.rerun()
    
    # RESULTS
    if analyze_btn:
        # Validation
        if not resume_text or len(resume_text.strip()) < 100:
            st.error("❌ Please provide a valid resume (at least 100 characters)")
        elif not job_text or len(job_text.strip()) < 100:
            st.error("❌ Please provide a valid job description (at least 100 characters)")
        else:
            # Parse and match
            with st.spinner("⏳ Analyzing resume and job description..."):
                try:
                    # Parse resume
                    resume_data = st.session_state.parser.parse_resume(resume_text)
                    
                    # Parse job description
                    job_data = st.session_state.job_parser.parse(job_text)
                    
                    # Rank candidate
                    ranked_results = st.session_state.ranker.rank_candidates(
                        [resume_data], job_text
                    )
                    
                    if ranked_results:
                        result = ranked_results[0]
                        st.session_state.results = [result]
                        st.session_state.job_data = job_data
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
            
            # Display Results
            if st.session_state.results:
                result = st.session_state.results[0]
                
                st.success("✓ Analysis completed successfully!")
                
                st.divider()
                
                # MAIN SCORE SECTION
                st.subheader("📊 Match Analysis")
                
                score_cols = st.columns(4)
                
                with score_cols[0]:
                    st.metric(
                        "Overall Match",
                        f"{result['overall_score']}%",
                        delta=None
                    )
                
                with score_cols[1]:
                    st.metric(
                        "Skills Match",
                        f"{result['skills_score']}%"
                    )
                
                with score_cols[2]:
                    st.metric(
                        "Experience Match",
                        f"{result['experience_score']}%"
                    )
                
                with score_cols[3]:
                    st.metric(
                        "Education Match",
                        f"{result['education_score']}%"
                    )
                
                st.divider()
                
                # VISUALIZATIONS
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    fig = create_score_gauge(result['overall_score'], "Overall Match Score")
                    st.plotly_chart(fig, use_container_width=True)
                
                with viz_col2:
                    fig = create_skills_comparison(
                        result['matched_skills'],
                        result['missing_skills'],
                        result['skills']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # DETAILED BREAKDOWN
                st.subheader("🔍 Detailed Breakdown")
                
                det_col1, det_col2 = st.columns(2)
                
                with det_col1:
                    st.markdown("### ✓ Matched Skills")
                    if result['matched_skills']:
                        for skill in result['matched_skills']:
                            render_tag(skill)
                    else:
                        st.info("No matching skills found")
                
                with det_col2:
                    st.markdown("### ✗ Missing Skills")
                    if result['missing_skills']:
                        for skill in result['missing_skills']:
                            render_tag(skill)
                    else:
                        st.success("All required skills are present!")
                
                st.divider()
                
                # CANDIDATE PROFILE
                st.subheader("👤 Candidate Profile")
                
                profile_col1, profile_col2 = st.columns(2)
                
                with profile_col1:
                    st.markdown("**Experience:**")
                    st.write(f"{result['experience_years']} years")
                    
                    st.markdown("**Education:**")
                    if result['education']:
                        for edu in result['education']:
                            st.text(f"• {edu.title()}")
                    else:
                        st.text("Not found")
                
                with profile_col2:
                    st.markdown("**Certifications:**")
                    if result['certifications']:
                        for cert in result['certifications']:
                            st.text(f"• {cert.title()}")
                    else:
                        st.text("Not found")
                    
                    st.markdown("**Contact:**")
                    if result['email']:
                        st.text(f"Email: {result['email']}")
                    if result['phone']:
                        st.text(f"Phone: {result['phone']}")
                
                st.divider()
                
                # JOB REQUIREMENTS
                st.subheader("💼 Job Requirements")
                
                req_col1, req_col2 = st.columns(2)
                
                with req_col1:
                    st.markdown("**Required Skills:**")
                    if st.session_state.job_data['skills']:
                        for skill in st.session_state.job_data['skills']:
                            render_tag(skill)
                    else:
                        st.info("No specific skills mentioned")
                
                with req_col2:
                    st.markdown("**Required Experience:**")
                    st.write(f"{st.session_state.job_data['required_experience']} years")
                    
                    st.markdown("**Education Level:**")
                    st.write(st.session_state.job_data['education_level'])
                
                st.divider()
                
                # RECOMMENDATION
                st.subheader("💡 Recommendation")
                
                score = result['overall_score']
                if score >= 80:
                    st.success(f"🟢 **Excellent Match ({score}%)** - Highly recommended for interview", icon="✓")
                elif score >= 60:
                    st.warning(f"🟡 **Good Match ({score}%)** - Worth considering for interview", icon="⚠️")
                elif score >= 40:
                    st.info(f"🔵 **Moderate Match ({score}%)** - Could be potential with training", icon="ℹ️")
                else:
                    st.error(f"🔴 **Poor Match ({score}%)** - Not recommended at this time", icon="❌")


# ============ TAB 2: BATCH PROCESSING ============
with tab2:
    st.header("📊 Batch Processing")
    st.markdown("Upload a CSV file with multiple resumes for batch matching against a job description.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📂 Upload Resumes CSV")
        st.info("CSV should have columns: 'Resume' (and optionally 'Candidate' name)")
        
        csv_file = st.file_uploader("Upload CSV file", type=['csv'], key="batch_csv")
        
        if csv_file:
            try:
                df = pd.read_csv(csv_file)
                st.success(f"✓ Loaded {len(df)} resumes")
                st.dataframe(df.head(3), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
    
    with col2:
        st.subheader("💼 Job Description")
        
        batch_jd = st.text_area(
            "Paste job description for batch matching",
            height=200,
            placeholder="Paste the job description...",
            key="batch_jd"
        )
    
    st.divider()
    
    if st.button("🚀 Process Batch", use_container_width=True, type="primary"):
        if not csv_file:
            st.error("Please upload a CSV file")
        elif not batch_jd or len(batch_jd.strip()) < 100:
            st.error("Please provide a valid job description")
        else:
            with st.spinner("⏳ Processing batch..."):
                try:
                    df = pd.read_csv(csv_file)
                    
                    results = []
                    for idx, row in df.iterrows():
                        resume_text = row.get('Resume', '')
                        candidate_name = row.get('Candidate', f'Candidate {idx+1}')
                        
                        if resume_text and len(str(resume_text)) > 100:
                            resume_data = st.session_state.parser.parse_resume(resume_text)
                            ranked = st.session_state.ranker.rank_candidates([resume_data], batch_jd)
                            
                            if ranked:
                                result = ranked[0]
                                result['candidate_name'] = candidate_name
                                results.append(result)
                    
                    if results:
                        st.success(f"✓ Processed {len(results)} resumes")
                        
                        # Create results dataframe
                        results_df = pd.DataFrame({
                            'Candidate': [r['candidate_name'] for r in results],
                            'Overall Score': [r['overall_score'] for r in results],
                            'Skills Score': [r['skills_score'] for r in results],
                            'Experience Score': [r['experience_score'] for r in results],
                            'Education Score': [r['education_score'] for r in results],
                            'Matched Skills': [', '.join(r['matched_skills']) for r in results],
                            'Missing Skills': [', '.join(r['missing_skills']) for r in results]
                        })
                        
                        # Sort by overall score
                        results_df = results_df.sort_values('Overall Score', ascending=False)
                        
                        st.divider()
                        st.subheader("📈 Results Summary")
                        
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Visualization
                        fig = px.bar(
                            results_df.sort_values('Overall Score', ascending=True).tail(10),
                            x='Overall Score',
                            y='Candidate',
                            orientation='h',
                            color='Overall Score',
                            color_continuous_scale='RdYlGn',
                            title='Top 10 Matched Candidates'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Download results
                        csv_buffer = io.BytesIO()
                        results_df.to_csv(csv_buffer, index=False)
                        csv_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download Results (CSV)",
                            data=csv_buffer.getvalue(),
                            file_name="resume_screening_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    else:
                        st.warning("No valid resumes found in the uploaded file")
                
                except Exception as e:
                    st.error(f"Error processing batch: {str(e)}")


# ============ TAB 3: SETTINGS ============
with tab3:
    st.header("⚙️ Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Scoring Weights")
        st.info("Adjust how different factors contribute to the overall score")
        
        skill_weight = st.slider(
            "Skills Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.05
        )
        
        experience_weight = st.slider(
            "Experience Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.35,
            step=0.05
        )
        
        education_weight = st.slider(
            "Education Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.15,
            step=0.05
        )
        
        total = skill_weight + experience_weight + education_weight
        st.metric("Total Weight", f"{total:.2f}", delta="(should be 1.0)")
        
        if abs(total - 1.0) < 0.01:
            st.success("✓ Weights are balanced")
        else:
            st.warning("⚠️ Weights should sum to 1.0")
        
        if st.button("Apply Weights"):
            st.session_state.ranker.skill_weight = skill_weight
            st.session_state.ranker.experience_weight = experience_weight
            st.session_state.ranker.education_weight = education_weight
            st.success("✓ Weights updated successfully!")
    
    with col2:
        st.subheader("ℹ️ System Information")
        
        st.text(f"Resume Parser: Initialized")
        st.text(f"Job Parser: Initialized")
        st.text(f"Candidate Ranker: Initialized")
        
        st.markdown("**Skills Database:**")
        st.metric("Total Skills", len(st.session_state.parser.SKILL_LIST))
        
        st.markdown("**Supported File Types:**")
        st.text("• PDF (.pdf)")
        st.text("• Word (.docx)")
        st.text("• Text (.txt)")


# ============ TAB 4: ABOUT ============
with tab4:
    st.header("ℹ️ About AI Resume Screening System")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📖 Overview
        
        The AI Resume Screening System is designed to help HR professionals and recruiters 
        quickly identify the best-fit candidates for job positions using machine learning 
        and natural language processing.
        
        ### ✨ Features
        
        - **🎯 Single Resume Matching** - Match individual resumes against job descriptions
        - **📊 Batch Processing** - Process multiple resumes at once
        - **📈 Score-based Ranking** - Candidates ranked by match percentage
        - **🔍 Detailed Analysis** - Skill matching, experience comparison, education verification
        - **📥 File Support** - PDF, DOCX, and TXT resume uploads
        - **🎨 Modern UI** - Interactive visualizations and easy-to-use interface
        
        ### 🔧 Technology Stack
        
        - **Frontend**: Streamlit
        - **NLP**: Python, Regular Expressions
        - **Visualization**: Plotly
        - **File Processing**: PyPDF2, python-docx
        - **Data Processing**: Pandas, NumPy
        
        ### 📝 How It Works
        
        1. **Parse Resume** - Extract skills, experience, education, and contact info
        2. **Parse Job Description** - Extract required skills and qualifications
        3. **Match & Score** - Compare resume against job requirements
        4. **Rank Results** - Generate match scores and recommendations
        
        ### 🎯 Matching Criteria
        
        The system evaluates candidates based on:
        
        - **Skills Match (50%)** - How many required skills the candidate has
        - **Experience Match (35%)** - Years of experience vs. requirements
        - **Education Match (15%)** - Educational qualifications
        
        ### 📧 Contact & Support
        
        For questions or feedback, please reach out to the development team.
        """)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric("Version", "1.0")
            st.metric("Supported Skills", len(st.session_state.parser.SKILL_LIST))
        with stat_col2:
            st.metric("File Types", "3")
            st.metric("Scoring Factors", "3")
        
        st.divider()
        
        st.markdown("### 📚 Resources")
        st.markdown("""
        - [GitHub Repository](#)
        - [Documentation](#)
        - [API Reference](#)
        - [FAQ](#)
        """)

st.divider()

# FOOTER
st.markdown("""
---
<div style='text-align: center'>
    <p style='color: grey; font-size: 12px;'>
        AI Resume Screening System v1.0 | Built with Streamlit | © 2024
    </p>
</div>
""", unsafe_allow_html=True)
