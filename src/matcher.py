def normalize_skill(skill):
    """
    Normalize a skill for comparison.
    """

    return skill.strip().lower()


def compare_skills(resume_skills, job_skills):
    """
    Compare resume skills against job-required skills.

    Returns:
        matching_skills
        missing_skills
        match_percentage
    """

    resume_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    job_set = {
        normalize_skill(skill)
        for skill in job_skills
    }

    matching_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set.difference(resume_set)
    )

    if not job_set:
        match_percentage = 0.0

    else:
        match_percentage = (
            len(matching_skills)
            / len(job_set)
        ) * 100

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(
            match_percentage,
            2
        )
    }