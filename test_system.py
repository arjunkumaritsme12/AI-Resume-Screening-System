#!/usr/bin/env python
"""
Quick test script to verify the resume screening system functionality.
Run this to test all core modules before using the Streamlit app.
"""

import sys
import os
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from resume_parser import ResumeParser
from job_parser import JobDescriptionParser
from matcher import CandidateRanker
from utils import cleanResume, is_resume, is_job_description

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_resume_parser():
    """Test resume parsing functionality."""
    print_section("Testing Resume Parser")
    
    parser = ResumeParser()
    
    sample_resume = """
    John Doe
    Senior Software Engineer
    
    Email: john.doe@example.com
    Phone: 555-123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 7 years in full-stack development
    
    TECHNICAL SKILLS
    - Programming: Python, JavaScript, TypeScript, Java
    - Web: React, Angular, Node.js, Express
    - Cloud: AWS, Docker, Kubernetes
    - Databases: PostgreSQL, MongoDB, Redis
    - Tools: Git, Jenkins, Jira
    
    WORK EXPERIENCE
    Senior Engineer at Tech Corp (2020-Present)
    - Led development of cloud-based platform using Python and AWS
    - 3+ years of experience leading engineering teams
    
    EDUCATION
    Bachelor's Degree in Computer Science, State University (2016)
    
    CERTIFICATIONS
    AWS Certified Solutions Architect (2022)
    """
    
    print("Parsing sample resume...")
    result = parser.parse_resume(sample_resume)
    
    print("\n✓ Resume parsed successfully!")
    print(f"  Skills found: {len(result['skills'])} - {result['skills'][:5]}...")
    print(f"  Experience: {result['total_experience_years']} years")
    print(f"  Email: {result['email']}")
    print(f"  Phone: {result['phone']}")
    print(f"  Education: {result['education']}")
    print(f"  Certifications: {result['certifications']}")
    
    return result

def test_job_parser():
    """Test job description parsing."""
    print_section("Testing Job Parser")
    
    parser = JobDescriptionParser()
    
    sample_jd = """
    Senior Software Engineer - Remote Position
    
    We are looking for an experienced Software Engineer to join our team.
    
    REQUIRED QUALIFICATIONS:
    - 5+ years of professional software development experience
    - Strong proficiency in Python and JavaScript
    - Experience with React for frontend development
    - AWS cloud platform experience (EC2, S3, Lambda)
    - SQL and NoSQL database experience
    - Bachelor's degree in Computer Science or related field
    
    NICE TO HAVE:
    - Machine Learning experience
    - Docker and Kubernetes knowledge
    - Leadership experience
    - AWS certification
    
    RESPONSIBILITIES:
    - Design and develop scalable software solutions
    - Participate in code reviews and technical discussions
    - Collaborate with cross-functional teams
    """
    
    print("Parsing sample job description...")
    result = parser.parse(sample_jd)
    
    print("\n✓ Job description parsed successfully!")
    print(f"  Required skills: {len(result['skills'])} - {result['skills'][:5]}...")
    print(f"  Experience required: {result['required_experience']}+ years")
    print(f"  Education level: {result['education_level']}")
    print(f"  Job title: {result['title']}")
    
    return result

def test_matcher():
    """Test candidate matching."""
    print_section("Testing Candidate Matcher")
    
    ranker = CandidateRanker()
    
    # Use parsed data from previous tests
    sample_resume = """
    John Doe
    Senior Software Engineer
    
    TECHNICAL SKILLS
    Python, JavaScript, React, AWS, PostgreSQL, Docker, Jenkins
    
    WORK EXPERIENCE
    7 years of software development experience
    
    EDUCATION
    Bachelor's in Computer Science
    
    CERTIFICATIONS
    AWS Certified Solutions Architect
    """
    
    sample_jd = """
    Senior Software Engineer - Requirements:
    5+ years experience, Python, JavaScript, React, AWS, SQL preferred
    Bachelor's degree required
    AWS certification nice to have
    """
    
    parser = ResumeParser()
    resume_data = parser.parse_resume(sample_resume)
    
    print("Matching resume against job description...")
    results = ranker.rank_candidates([resume_data], sample_jd)
    
    if results:
        result = results[0]
        print("\n✓ Matching completed successfully!")
        print(f"  Overall Score: {result['overall_score']}%")
        print(f"  Skills Score: {result['skills_score']}%")
        print(f"  Experience Score: {result['experience_score']}%")
        print(f"  Education Score: {result['education_score']}%")
        print(f"  Matched Skills: {', '.join(result['matched_skills'][:5])}")
        
        if result['overall_score'] >= 80:
            print("  Recommendation: 🟢 EXCELLENT MATCH")
        elif result['overall_score'] >= 60:
            print("  Recommendation: 🟡 GOOD MATCH")
        else:
            print("  Recommendation: 🔴 POOR MATCH")
        
        return result
    else:
        print("\n✗ Matching failed")
        return None

def test_utils():
    """Test utility functions."""
    print_section("Testing Utility Functions")
    
    test_text = """
    John Doe - Senior Software Engineer
    
    SKILLS: Python, Java, JavaScript, AWS, Machine Learning
    EXPERIENCE: 5 years in software development
    EDUCATION: Bachelor's in Computer Science
    
    Technical skills include web development, cloud computing, and AI/ML.
    """
    
    print("Testing text cleaning...")
    cleaned = cleanResume(test_text)
    print(f"✓ Text cleaned: {cleaned[:60]}...")
    
    print("\nTesting resume detection...")
    is_resume_result = is_resume(test_text)
    print(f"✓ Is resume: {is_resume_result}")
    
    print("\nTesting job description detection...")
    is_jd_result = is_job_description("Looking for software engineer with 5+ years experience")
    print(f"✓ Is job description: {is_jd_result}")

def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "AI RESUME SCREENING SYSTEM - TEST SUITE" + " "*6 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Run tests
        test_utils()
        resume_data = test_resume_parser()
        job_data = test_job_parser()
        match_result = test_matcher()
        
        # Summary
        print_section("TEST SUMMARY")
        print("\n✓ ALL TESTS PASSED!")
        print("\nSystem is ready to use. Start the application with:")
        print("  cd app && streamlit run app.py")
        
        return True
    
    except Exception as e:
        print_section("ERROR OCCURRED")
        print(f"\n✗ Test failed with error:")
        print(f"  {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
