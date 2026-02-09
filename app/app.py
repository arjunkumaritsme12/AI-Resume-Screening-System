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
    st.header("📊 Batch Resume Screening & Ranking")
    st.markdown("**Upload multiple resumes and get an instant ranked list of the best candidates**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📂 Upload Multiple Resumes")
        st.markdown("Upload resume files (PDF, DOCX, TXT) or a CSV with resume text")
        
        upload_type = st.radio(
            "Upload method:",
            ["Individual Files", "CSV File"],
            key="batch_upload_type"
        )
        
        uploaded_files = []
        batch_df = None
        
        if upload_type == "Individual Files":
            uploaded_files = st.file_uploader(
                "Drag and drop or select multiple resume files",
                type=['pdf', 'docx', 'txt'],
                accept_multiple_files=True,
                key="batch_files"
            )
            if uploaded_files:
                st.success(f"✓ Loaded {len(uploaded_files)} resume files")
        else:
            csv_file = st.file_uploader("Upload CSV (with 'Resume' column)", type=['csv'], key="batch_csv")
            if csv_file:
                try:
                    batch_df = pd.read_csv(csv_file)
                    st.success(f"✓ Loaded {len(batch_df)} resumes from CSV")
                except Exception as e:
                    st.error(f"Error reading CSV: {str(e)}")
    
    with col2:
        st.subheader("💼 Job Description")
        st.markdown("Paste the job description to match resumes against")
        
        batch_jd = st.text_area(
            "Job Description",
            height=250,
            placeholder="Paste the job description here...",
            key="batch_jd"
        )
    
    st.divider()
    
    col_process, col_filter = st.columns([2, 1])
    
    with col_process:
        process_btn = st.button("🚀 Analyze & Rank Candidates", use_container_width=True, type="primary")
    
    with col_filter:
        min_score = st.slider("Minimum Match Score", 0, 100, 40, key="min_score_slider")
    
    if process_btn:
        if not batch_jd or len(batch_jd.strip()) < 100:
            st.error("❌ Please provide a valid job description (at least 100 characters)")
        elif upload_type == "Individual Files" and not uploaded_files:
            st.error("❌ Please upload at least one resume file")
        elif upload_type == "CSV File" and batch_df is None:
            st.error("❌ Please upload a CSV file with resumes")
        else:
            with st.spinner("⏳ Processing resumes and ranking candidates..."):
                try:
                    results = []
                    
                    if upload_type == "Individual Files":
                        for idx, uploaded_file in enumerate(uploaded_files):
                            candidate_name = Path(uploaded_file.name).stem
                            text, error = extract_file_content(uploaded_file)
                            
                            if error:
                                st.warning(f"⚠️ Skipped {uploaded_file.name}: {error}")
                            else:
                                resume_data = st.session_state.parser.parse_resume(text)
                                ranked = st.session_state.ranker.rank_candidates([resume_data], batch_jd)
                                
                                if ranked:
                                    result = ranked[0]
                                    result['candidate_name'] = candidate_name
                                    result['file_name'] = uploaded_file.name
                                    results.append(result)
                    else:
                        for idx, row in batch_df.iterrows():
                            resume_text = row.get('Resume', '')
                            candidate_name = row.get('Candidate', f'Candidate {idx+1}')
                            
                            if resume_text and len(str(resume_text)) > 100:
                                resume_data = st.session_state.parser.parse_resume(resume_text)
                                ranked = st.session_state.ranker.rank_candidates([resume_data], batch_jd)
                                
                                if ranked:
                                    result = ranked[0]
                                    result['candidate_name'] = candidate_name
                                    result['file_name'] = candidate_name
                                    results.append(result)
                    
                    if results:
                        # Sort by overall score (descending)
                        results_sorted = sorted(results, key=lambda x: x['overall_score'], reverse=True)
                        
                        # Filter by minimum score
                        results_filtered = [r for r in results_sorted if r['overall_score'] >= min_score]
                        
                        st.success(f"✓ Processed {len(results)} resumes | Showing {len(results_filtered)} above {min_score}% threshold")
                        
                        st.divider()
                        
                        # SUMMARY METRICS
                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        with metric_col1:
                            st.metric("Total Candidates", len(results))
                        with metric_col2:
                            st.metric("Qualified (80%+)", len([r for r in results if r['overall_score'] >= 80]))
                        with metric_col3:
                            st.metric("Good Fit (60-80%)", len([r for r in results if 60 <= r['overall_score'] < 80]))
                        with metric_col4:
                            best_score = max(results, key=lambda x: x['overall_score'])['overall_score']
                            st.metric("Top Score", f"{best_score}%")
                        
                        st.divider()
                        
                        # RESULTS TABLE
                        st.subheader("📋 Ranked Candidates")
                        
                        results_df = pd.DataFrame({
                            'Rank': list(range(1, len(results_filtered) + 1)),
                            'Candidate': [r['candidate_name'] for r in results_filtered],
                            'Overall Score': [f"{r['overall_score']:.1f}%" for r in results_filtered],
                            'Skills Match': [f"{r['skills_score']:.1f}%" for r in results_filtered],
                            'Experience': [f"{r['experience_score']:.1f}%" for r in results_filtered],
                            'Education': [f"{r['education_score']:.1f}%" for r in results_filtered],
                        })
                        
                        st.dataframe(results_df, use_container_width=True, hide_index=True)
                        
                        # VISUALIZATION
                        st.subheader("📊 Candidate Match Scores")
                        
                        fig = px.bar(
                            x=[r['overall_score'] for r in results_filtered],
                            y=[r['candidate_name'] for r in results_filtered],
                            orientation='h',
                            color=[r['overall_score'] for r in results_filtered],
                            color_continuous_scale='RdYlGn',
                            range_color=[0, 100],
                            title='Candidates Ranked by Match Score',
                            labels={'x': 'Match Score (%)', 'y': 'Candidate'}
                        )
                        fig.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.divider()
                        
                        # DETAILED PROFILES
                        st.subheader("👥 Top Candidates Detailed Profiles")
                        
                        for idx, result in enumerate(results_filtered[:5], 1):
                            with st.expander(f"#{idx} - {result['candidate_name']} ({result['overall_score']:.1f}%)"):
                                profile_col1, profile_col2 = st.columns(2)
                                
                                with profile_col1:
                                    st.markdown("**Scores:**")
                                    st.text(f"• Overall: {result['overall_score']:.1f}%")
                                    st.text(f"• Skills: {result['skills_score']:.1f}%")
                                    st.text(f"• Experience: {result['experience_score']:.1f}%")
                                    st.text(f"• Education: {result['education_score']:.1f}%")
                                    
                                    st.markdown("**Contact:**")
                                    if result.get('email'):
                                        st.text(f"📧 {result['email']}")
                                    if result.get('phone'):
                                        st.text(f"☎️ {result['phone']}")
                                
                                with profile_col2:
                                    st.markdown("**Experience:**")
                                    st.text(f"{result['experience_years']} years")
                                    
                                    st.markdown("**Matched Skills:**")
                                    for skill in result['matched_skills'][:8]:
                                        render_tag(skill)
                                    if len(result['matched_skills']) > 8:
                                        st.caption(f"+{len(result['matched_skills']) - 8} more skills")
                                
                        st.divider()
                        
                        # EXPORT OPTIONS
                        st.subheader("📥 Export Results")
                        
                        # Prepare detailed CSV
                        detailed_results = []
                        for r in results_filtered:
                            detailed_results.append({
                                'Candidate': r['candidate_name'],
                                'Overall_Score': round(r['overall_score'], 2),
                                'Skills_Score': round(r['skills_score'], 2),
                                'Experience_Score': round(r['experience_score'], 2),
                                'Education_Score': round(r['education_score'], 2),
                                'Years_Experience': r['experience_years'],
                                'Matched_Skills': '; '.join(r['matched_skills']),
                                'Missing_Skills': '; '.join(r['missing_skills']),
                                'Email': r.get('email', ''),
                                'Phone': r.get('phone', ''),
                            })
                        
                        detailed_df = pd.DataFrame(detailed_results)
                        
                        csv_buffer = io.BytesIO()
                        detailed_df.to_csv(csv_buffer, index=False)
                        csv_buffer.seek(0)
                        
                        col_csv, col_json = st.columns(2)
                        
                        with col_csv:
                            st.download_button(
                                label="📊 Download as CSV",
                                data=csv_buffer.getvalue(),
                                file_name="ranked_candidates.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col_json:
                            json_data = detailed_df.to_json(orient='records', indent=2)
                            st.download_button(
                                label="📋 Download as JSON",
                                data=json_data,
                                file_name="ranked_candidates.json",
                                mime="application/json",
                                use_container_width=True
                            )
                    else:
                        st.warning("❌ No valid resumes could be processed")
                
                except Exception as e:
                    st.error(f"Error processing batch: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())


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
        AI Resume Screening System v1.0 | Built with Streamlit | © 2025
    </p>
</div>
""", unsafe_allow_html=True)
