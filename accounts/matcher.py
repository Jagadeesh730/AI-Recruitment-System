def calculate_match_score(
    candidate_skills,
    job_skills
):

    matched = 0

    for skill in job_skills:

        if skill.lower() in [
            s.lower()
            for s in candidate_skills
        ]:

            matched += 1

    score = (
        matched / len(job_skills)
    ) * 100

    return round(score, 2)