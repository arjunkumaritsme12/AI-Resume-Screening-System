import re
import os
from utils import cleanResume

class ResumeParser:
    def __init__(self):
        self.SKILL_LIST = [
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust",
            "machine learning", "ml", "deep learning", "ai", "artificial intelligence",
            "sql", "mysql", "postgresql", "mongodb", "nosql", "cassandra", "hbase",
            "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
            "react", "vue", "angular", "nodejs", "node.js", "express",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
            "html", "css", "bootstrap", "tailwind",
            "git", "github", "gitlab", "bitbucket",
            "jenkins", "ci/cd", "devops",
            "api", "rest", "graphql",
            "linux", "windows", "unix",
            "excel", "tableau", "powerbi", "visualization",
            "agile", "scrum", "jira",
            "communication", "leadership", "teamwork",
            "nlp", "computer vision", "opencv"
        ]

    def parse_resume(self, input_data):
        """
        Parse resume from file path or raw text.
        Returns structured resume data with extracted information.
        """
        try:
            # Case 1: input is a FILE PATH
            if isinstance(input_data, str) and os.path.exists(input_data):
                with open(input_data, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            
            # Case 2: input is RAW TEXT
            elif isinstance(input_data, str):
                text = input_data
            
            else:
                return {}

            # Clean the text
            text_lower = text.lower()
            text_clean = cleanResume(text_lower)

            # Extract information
            skills = self._extract_skills(text_lower)
            experience_years = self._extract_experience(text_clean)
            email = self._extract_email(text)
            phone = self._extract_phone(text)
            education = self._extract_education(text_lower)
            certifications = self._extract_certifications(text_lower)

            return {
                "skills": skills,
                "total_experience_years": experience_years,
                "email": email,
                "phone": phone,
                "education": education,
                "certifications": certifications,
                "raw_text": text[:1000],
                "text_length": len(text)
            }
        except Exception as e:
            print(f"Error parsing resume: {str(e)}")
            return {}

    def _extract_skills(self, text):
        """Extract skills from resume text."""
        skills = []
        for skill in self.SKILL_LIST:
            if skill in text:
                skills.append(skill)
        return list(set(skills))  # Remove duplicates

    def _extract_experience(self, text):
        """Extract years of experience from resume text."""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)',
            r'(\d+)\+?\s+years',
            r'(\d+)\+?\s+yrs'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    years = int(match.group(1))
                    return min(years, 60)  # Cap at 60 years
                except ValueError:
                    continue
        
        return 0

    def _extract_email(self, text):
        """Extract email address from resume text."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def _extract_phone(self, text):
        """Extract phone number from resume text."""
        patterns = [
            r'(?:\+1)?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            r'\+[0-9]{1,3}[-.\s]?[0-9]{1,14}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None

    def _extract_education(self, text):
        """Extract education degrees from resume text."""
        degrees = []
        degree_keywords = [
            "bachelor", "bachelor's", "bs", "b.s.", "b.a.",
            "master", "master's", "ms", "m.s.", "m.a.", "mba",
            "phd", "ph.d.", "doctorate", "doctoral",
            "associate", "a.s.", "diploma", "diploma",
            "bootcamp", "certification", "certified"
        ]
        
        for degree in degree_keywords:
            if degree in text:
                degrees.append(degree)
        
        return list(set(degrees))

    def _extract_certifications(self, text):
        """Extract certifications from resume text."""
        certifications = []
        cert_keywords = [
            "aws certified", "azure certified", "gcp certified",
            "pmp", "ciscp", "scrum master", "cpa", "cfa",
            "certified", "certificate",
            "comptia", "ccna", "ccnp"
        ]
        
        for cert in cert_keywords:
            if cert in text:
                certifications.append(cert)
        
        return list(set(certifications))
