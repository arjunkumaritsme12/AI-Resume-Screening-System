"""
Sample data generator for testing the resume screening system.
Generates sample resumes and job descriptions for testing purposes.
"""

import csv
import os
from pathlib import Path

# Sample resumes data
SAMPLE_RESUMES = [
    {
        "name": "Alice Johnson",
        "resume": """Alice Johnson
Senior Software Engineer
Email: alice.johnson@tech.com
Phone: 555-0101

PROFESSIONAL SUMMARY
Experienced software engineer with 7 years of expertise in full-stack development
and cloud architecture.

TECHNICAL SKILLS
- Languages: Python, JavaScript, TypeScript, Java
- Frontend: React, Vue.js, Angular, HTML/CSS
- Backend: Node.js, Express, Django, Python Flask
- Cloud: AWS (EC2, S3, Lambda), Google Cloud Platform
- Databases: PostgreSQL, MongoDB, Redis
- DevOps: Docker, Kubernetes, Jenkins, CI/CD
- Tools: Git, GitHub, JIRA, VS Code

WORK EXPERIENCE
Senior Engineer at CloudTech Solutions (2021-Present)
- Led development of microservices architecture using Python and AWS
- Managed team of 4 engineers in full-stack development
- 7+ years of professional software development experience

EDUCATION
Bachelor's Degree in Computer Science, Tech State University (2016)
Master's Degree in Software Engineering, Online University (2019)

CERTIFICATIONS
- AWS Certified Solutions Architect (2022)
- Kubernetes Application Developer (2021)
"""
    },
    {
        "name": "Bob Smith",
        "resume": """Bob Smith
Full Stack Developer
Email: bob.smith@code.com
Phone: 555-0102

TECHNICAL SKILLS
Programming: Java, Python, JavaScript, C++
Web Development: React, Node.js, Express, REST APIs
Mobile: React Native, Swift
Databases: MySQL, MongoDB, Firebase
Tools: Git, Docker, Jenkins

WORK EXPERIENCE
Full Stack Developer at WebApps Inc (2019-Present)
- 4 years building web applications with React and Node.js
- Developed REST APIs serving 100k+ users
- Implemented CI/CD pipelines with Jenkins

Junior Developer at StartupXYZ (2018-2019)
- Started career in web development
- 1 year experience with JavaScript and basic backend

EDUCATION
Bachelor's in Information Technology, Code Academy (2018)

CERTIFICATIONS
None listed
"""
    },
    {
        "name": "Carol Davis",
        "resume": """Carol Davis
Data Scientist
Email: carol.davis@data.com
Phone: 555-0103

SUMMARY
Data scientist with 6 years of experience in machine learning and data analytics.

TECHNICAL SKILLS
Programming: Python, R, SQL
ML Frameworks: TensorFlow, PyTorch, Scikit-learn
Data Tools: Pandas, NumPy, Matplotlib, Tableau
Cloud: AWS SageMaker, Google Cloud ML
Databases: PostgreSQL, Cassandra, HBase

PROFESSIONAL EXPERIENCE
Senior Data Scientist at AnalyticsPlus (2020-Present)
- 6+ years building ML models and data pipelines
- Deployed deep learning models for recommendation systems
- Led data science team of 3 people

Data Analyst at DataCorp (2016-2020)
- Performed statistical analysis on large datasets
- Created dashboards and visualizations

EDUCATION
Master's in Data Science, Online University (2019)
Bachelor's in Statistics, State University (2016)

CERTIFICATIONS
- TensorFlow Certification
- AWS Certified ML Specialty
"""
    },
    {
        "name": "David Wilson",
        "resume": """David Wilson
Network Administrator
Email: david@network.com

EXPERIENCE
3 years as Network Administrator
- Basic Linux and Windows server knowledge
- Some networking experience
- Help desk support

SKILLS
- Windows Server
- Basic networking
- IT Support

EDUCATION
Diploma in IT Support (2020)
"""
    },
    {
        "name": "Eve Martinez",
        "resume": """Eve Martinez
DevOps Engineer
Email: eve.martinez@devops.com

TECHNICAL SKILLS
Cloud: AWS, Azure, GCP
Containerization: Docker, Kubernetes, Docker Compose
Infrastructure as Code: Terraform, CloudFormation
CI/CD: Jenkins, GitLab CI, GitHub Actions
Monitoring: Prometheus, Grafana, ELK Stack
Scripting: Bash, Python, Go

EXPERIENCE
DevOps Engineer at CloudOps (2020-Present)
- 4 years managing cloud infrastructure with Kubernetes
- Implemented automated deployment pipelines
- Reduced deployment time by 60%

Cloud Support Engineer at HostingCo (2018-2020)
- Provided AWS infrastructure support
- 2 years cloud experience

EDUCATION
Bachelor's in Computer Engineering (2018)

CERTIFICATIONS
- AWS Solutions Architect Professional
- Kubernetes Application Developer
"""
    }
]

# Sample job descriptions
SAMPLE_JOB_DESCRIPTIONS = {
    "Senior Full Stack Engineer": """
    Senior Full Stack Engineer - Remote

    ABOUT THE ROLE
    We are seeking an experienced Full Stack Engineer to lead our technical initiatives.

    REQUIREMENTS
    - 6+ years software development experience
    - Expert-level: Python, JavaScript/TypeScript
    - React.js for frontend development
    - Node.js or similar backend framework
    - AWS cloud platform experience (EC2, S3, Lambda)
    - SQL and NoSQL database expertise
    - Docker and Kubernetes knowledge
    - Team leadership experience
    
    NICE TO HAVE
    - Machine Learning background
    - Microservices architecture
    - GraphQL experience
    
    EDUCATION
    Bachelor's degree in Computer Science or related field

    SALARY: $150,000 - $200,000
    """,
    
    "Data Scientist": """
    Data Scientist - AI/ML Focus

    POSITION OVERVIEW
    Join our data science team to build machine learning solutions.

    REQUIRED QUALIFICATIONS
    - 5+ years data science experience
    - Python programming expertise
    - TensorFlow or PyTorch
    - SQL and database knowledge
    - Statistical analysis and ML algorithms
    - Experience with big data tools (Hadoop, Spark)
    - Cloud platform experience (AWS, GCP)
    
    NICE TO HAVE
    - NLP/Computer Vision experience
    - Deep Learning specialization
    - Published research papers
    
    EDUCATION
    Master's degree in Computer Science, Statistics, or related field
    
    SALARY: $120,000 - $160,000
    """,
    
    "Junior Developer": """
    Junior Developer

    ABOUT US
    Growing tech startup looking for junior developers to join our team.

    REQUIREMENTS
    - 1-2 years development experience
    - JavaScript or Python knowledge
    - Basic HTML/CSS skills
    - Git version control
    - Problem-solving abilities
    
    NICE TO HAVE
    - React experience
    - API development
    - Testing background
    
    EDUCATION
    Bachelor's degree or bootcamp graduate
    
    SALARY: $60,000 - $80,000
    """,
    
    "DevOps Engineer": """
    DevOps Engineer

    THE OPPORTUNITY
    Help us scale our infrastructure and deployment processes.

    REQUIRED SKILLS
    - 4+ years DevOps/infrastructure experience
    - Kubernetes orchestration
    - Docker containerization
    - AWS or Azure cloud platform
    - Terraform or CloudFormation (IaC)
    - CI/CD pipeline tools (Jenkins, GitLab CI)
    - Linux administration
    - Bash/Python scripting
    
    PREFERRED
    - Monitoring tools experience (Prometheus, Grafana)
    - Helm experience
    - Go programming language
    
    EDUCATION
    Bachelor's in Computer Science or equivalent experience
    
    SALARY: $110,000 - $150,000
    """
}

def create_sample_csv():
    """Create a sample CSV file with resumes for testing."""
    csv_path = Path(__file__).parent / 'data' / 'sample_resumes.csv'
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Candidate', 'Resume'])
        
        for resume_data in SAMPLE_RESUMES:
            writer.writerow([resume_data['name'], resume_data['resume']])
    
    print(f"✓ Created sample CSV: {csv_path}")
    return str(csv_path)

def create_job_descriptions():
    """Create sample job description files."""
    jobs_dir = Path(__file__).parent / 'sample_jobs'
    jobs_dir.mkdir(exist_ok=True)
    
    for job_title, job_desc in SAMPLE_JOB_DESCRIPTIONS.items():
        file_path = jobs_dir / f"{job_title.replace(' ', '_').lower()}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(job_desc)
        print(f"✓ Created job description: {file_path}")

def print_sample_resume():
    """Print a sample resume for manual testing."""
    if SAMPLE_RESUMES:
        print("\n" + "="*60)
        print("SAMPLE RESUME FOR TESTING")
        print("="*60)
        print(SAMPLE_RESUMES[0]['resume'])
        print("="*60)

def print_sample_job_desc():
    """Print a sample job description for testing."""
    job_title = list(SAMPLE_JOB_DESCRIPTIONS.keys())[0]
    job_desc = SAMPLE_JOB_DESCRIPTIONS[job_title]
    
    print("\n" + "="*60)
    print("SAMPLE JOB DESCRIPTION FOR TESTING")
    print("="*60)
    print(job_desc)
    print("="*60)

if __name__ == "__main__":
    print("Creating sample data for testing...\n")
    
    # Create CSV
    create_sample_csv()
    
    # Create job description files
    create_job_descriptions()
    
    # Print samples
    print_sample_resume()
    print_sample_job_desc()
    
    print("\n✓ Sample data created successfully!")
    print("\nYou can now:")
    print("1. Use the sample_resumes.csv in batch processing")
    print("2. Use resumes from SAMPLE_RESUMES for single matching")
    print("3. Use job descriptions from sample_jobs/ directory")
