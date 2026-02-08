class CandidateRanker:
    def rank_candidates(self, resumes, job_description):
        jd_skills = JobDescriptionParser().parse(job_description)

        ranked = []
        for r in resumes:
            resume_skills = r["skills"]

            matched = list(set(resume_skills) & set(jd_skills))
            skill_score = (len(matched) / max(len(jd_skills), 1)) * 100

            exp_score = min(r["total_experience_years"] * 10, 100)

            overall = 0.7 * skill_score + 0.3 * exp_score

            ranked.append({
                "skills": resume_skills,
                "matched_skills": matched,
                "overall_score": round(overall, 2),
                "skills_score": round(skill_score, 2),
                "experience_score": round(exp_score, 2)
            })

        ranked.sort(key=lambda x: x["overall_score"], reverse=True)
        return ranked
