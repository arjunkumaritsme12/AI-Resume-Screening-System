class JobDescriptionParser:
    def parse(self, text):
        text = text.lower()
        skills = []

        SKILL_LIST = [
            "python","java","ml","machine learning",
            "sql","aws","react","docker"
        ]

        for s in SKILL_LIST:
            if s in text:
                skills.append(s)

        return skills
