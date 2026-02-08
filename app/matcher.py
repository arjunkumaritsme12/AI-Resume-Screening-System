from job_parser import JobDescriptionParser

class CandidateRanker:
    """
    Ranks candidates based on resume match with job description.
    Uses skill matching, experience level, and education requirements.
    """

    def __init__(self):
        self.job_parser = JobDescriptionParser()
        self.skill_weight = 0.50
        self.experience_weight = 0.35
        self.education_weight = 0.15

    def rank_candidates(self, resumes, job_description):
        """
        Rank multiple candidates against a job description.
        
        Args:
            resumes: List of resume dictionaries (output from ResumeParser)
            job_description: Job description text string or dict
        
        Returns:
            List of ranked candidates with scores
        """
        try:
            # Parse job description if it's a string
            if isinstance(job_description, str):
                jd_data = self.job_parser.parse(job_description)
            else:
                jd_data = job_description

            ranked = []
            
            for resume in resumes:
                if not resume:
                    continue

                # Calculate individual scores
                skill_score = self._calculate_skill_score(resume.get("skills", []), jd_data.get("skills", []))
                experience_score = self._calculate_experience_score(
                    resume.get("total_experience_years", 0),
                    jd_data.get("required_experience", 0)
                )
                education_score = self._calculate_education_score(
                    resume.get("education", []),
                    jd_data.get("education_level", "")
                )

                # Calculate weighted overall score
                overall_score = (
                    self.skill_weight * skill_score +
                    self.experience_weight * experience_score +
                    self.education_weight * education_score
                )

                matched_skills = list(set(resume.get("skills", [])) & set(jd_data.get("skills", [])))
                missing_skills = list(set(jd_data.get("skills", [])) - set(resume.get("skills", [])))

                ranked.append({
                    "skills": resume.get("skills", []),
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "overall_score": round(overall_score, 2),
                    "skills_score": round(skill_score, 2),
                    "experience_score": round(experience_score, 2),
                    "education_score": round(education_score, 2),
                    "experience_years": resume.get("total_experience_years", 0),
                    "education": resume.get("education", []),
                    "certifications": resume.get("certifications", []),
                    "email": resume.get("email"),
                    "phone": resume.get("phone"),
                    "match_percentage": round(overall_score, 2)
                })

            # Sort by overall score
            ranked.sort(key=lambda x: x["overall_score"], reverse=True)
            return ranked

        except Exception as e:
            print(f"Error ranking candidates: {str(e)}")
            return []

    def rank_single_resume(self, resume, job_description):
        """Rank a single resume against a job description."""
        ranked = self.rank_candidates([resume], job_description)
        return ranked[0] if ranked else {}

    def _calculate_skill_score(self, resume_skills, jd_skills):
        """
        Calculate skill match score.
        100% if all JD skills are present in resume, else prorated.
        """
        if not jd_skills:
            return 100.0

        matched = len(set(resume_skills) & set(jd_skills))
        return (matched / len(jd_skills)) * 100

    def _calculate_experience_score(self, resume_experience, required_experience):
        """
        Calculate experience score.
        100% if meets or exceeds requirement, prorated otherwise.
        """
        if required_experience == 0:
            return 100.0

        if resume_experience >= required_experience:
            return 100.0

        # Linear scoring: (actual / required) * 100
        return (resume_experience / required_experience) * 100

    def _calculate_education_score(self, resume_education, required_education):
        """
        Calculate education score based on degree level.
        """
        if not required_education or required_education == "Not Specified":
            return 100.0

        if not resume_education:
            return 0.0

        # Simple education hierarchy
        education_levels = {
            "phd": 5,
            "master's degree": 4,
            "mba": 4,
            "bachelor's degree": 3,
            "associate degree": 2,
            "diploma": 1,
            "bootcamp/certification": 1
        }

        required_level = education_levels.get(required_education.lower(), 0)

        resume_education_lower = [e.lower() for e in resume_education]
        max_resume_level = max(
            [education_levels.get(e, 0) for e in resume_education_lower],
            default=1
        )

        if required_level == 0:
            return 100.0

        if max_resume_level >= required_level:
            return 100.0

        return (max_resume_level / required_level) * 100
