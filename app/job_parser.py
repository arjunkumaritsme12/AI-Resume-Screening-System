import re
from utils import cleanResume

class JobDescriptionParser:
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

    def parse(self, text):
        """
        Parse job description and extract required skills and qualifications.
        """
        try:
            if not text:
                return {
                    "skills": [],
                    "required_experience": 0,
                    "education_level": "",
                    "title": "",
                    "raw_text": ""
                }

            text_lower = text.lower()
            text_clean = cleanResume(text_lower)

            # Extract information
            skills = self._extract_required_skills(text_lower)
            experience = self._extract_required_experience(text_clean)
            education = self._extract_education_requirement(text_lower)
            title = self._extract_job_title(text)

            return {
                "skills": skills,
                "required_experience": experience,
                "education_level": education,
                "title": title,
                "raw_text": text[:1000],
                "text_length": len(text)
            }
        except Exception as e:
            print(f"Error parsing job description: {str(e)}")
            return {
                "skills": [],
                "required_experience": 0,
                "education_level": "",
                "title": "",
                "raw_text": text[:1000] if text else ""
            }

    def _extract_required_skills(self, text):
        """Extract required skills from job description."""
        skills = []
        for skill in self.SKILL_LIST:
            if skill in text:
                skills.append(skill)
        return list(set(skills))  # Remove duplicates

    def _extract_required_experience(self, text):
        """Extract required years of experience from job description."""
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
                    return min(years, 60)
                except ValueError:
                    continue
        
        return 0

    def _extract_education_requirement(self, text):
        """Extract education requirement from job description."""
        degree_mapping = [
            ("phd", "PhD"),
            ("doctorate", "PhD"),
            ("master", "Master's Degree"),
            ("m.s.", "Master's Degree"),
            ("mba", "MBA"),
            ("bachelor", "Bachelor's Degree"),
            ("b.s.", "Bachelor's Degree"),
            ("b.a.", "Bachelor's Degree"),
            ("associate", "Associate Degree"),
            ("a.s.", "Associate Degree"),
            ("diploma", "Diploma"),
            ("bootcamp", "Bootcamp/Certification")
        ]
        
        for keyword, degree in degree_mapping:
            if keyword in text:
                return degree
        
        return "Not Specified"

    def _extract_job_title(self, text):
        """Extract job title from text (usually first line or title case)."""
        lines = text.strip().split('\n')
        for line in lines[:3]:  # Check first 3 lines
            line_clean = line.strip()
            if len(line_clean) > 5 and len(line_clean) < 100:
                return line_clean[:80]
        
        return "Job Title Not Found"
