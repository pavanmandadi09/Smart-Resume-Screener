import json
import re

from google import genai


def create_prompt(resume_text, job_description):
    """
    Create the prompt used by the LLM to evaluate
    a resume against a job description.
    """

    prompt = f"""
You are an expert technical recruiter.

Your task is to evaluate how well a candidate's resume
matches a given job description.

Analyze the candidate based on:

1. Technical skills
2. Programming languages
3. Frameworks and libraries
4. Tools and technologies
5. Education
6. Projects
7. Work experience
8. Relevant domain knowledge

Do not match only exact keywords.

Consider semantic similarity.

For example:
- Machine Learning and ML should be considered related.
- REST APIs and RESTful APIs should be considered related.
- JavaScript and JS should be considered related.

Give a realistic score from 1 to 10.

Scoring guidance:

1-2:
Very poor match. Most important requirements are missing.

3-4:
Weak match. Some relevant skills exist, but many important
requirements are missing.

5-6:
Moderate match. The candidate satisfies several requirements
but has noticeable gaps.

7-8:
Strong match. Most important requirements are satisfied,
with only some gaps.

9:
Very strong match. Almost all important requirements are
satisfied.

10:
Excellent match. The candidate is an exceptionally strong
match for the position.

Return ONLY valid JSON.

The JSON must have exactly these fields:

{{
    "score": 1,
    "matching_skills": [],
    "missing_skills": [],
    "justification": ""
}}

The score must be an integer between 1 and 10.

Keep matching_skills and missing_skills concise.

Do not include markdown.
Do not include ```json.
Do not include any text outside the JSON.

----------------------------------------
JOB DESCRIPTION
----------------------------------------

{job_description}

----------------------------------------
RESUME
----------------------------------------

{resume_text}

----------------------------------------
END INPUT
----------------------------------------
"""

    return prompt


def clean_json_response(response_text):
    """
    Clean the LLM response so that JSON can be parsed.
    """

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```json\s*",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    response_text = re.sub(
        r"^```\s*",
        "",
        response_text
    )

    response_text = re.sub(
        r"\s*```$",
        "",
        response_text
    )

    return response_text.strip()


def validate_result(result):
    """
    Validate and normalize the LLM result.
    """

    if not isinstance(result, dict):
        raise ValueError(
            "LLM returned an invalid result."
        )

    required_fields = [
        "score",
        "matching_skills",
        "missing_skills",
        "justification"
    ]

    for field in required_fields:

        if field not in result:
            raise ValueError(
                f"LLM response is missing '{field}'."
            )

    try:
        score = int(result["score"])

    except (ValueError, TypeError):

        raise ValueError(
            "LLM returned an invalid score."
        )

    if score < 1:
        score = 1

    if score > 10:
        score = 10

    matching_skills = result["matching_skills"]

    if not isinstance(
        matching_skills,
        list
    ):
        matching_skills = []

    missing_skills = result["missing_skills"]

    if not isinstance(
        missing_skills,
        list
    ):
        missing_skills = []

    matching_skills = [
        str(skill).strip()
        for skill in matching_skills
        if str(skill).strip()
    ]

    missing_skills = [
        str(skill).strip()
        for skill in missing_skills
        if str(skill).strip()
    ]

    justification = str(
        result["justification"]
    ).strip()

    return {
        "score": score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "justification": justification
    }


def analyze_resume(
    resume_text,
    job_description,
    api_key
):
    """
    Analyze a resume against a job description
    using Gemini.
    """

    if not api_key:
        raise ValueError(
            "Gemini API key is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = create_prompt(
        resume_text,
        job_description
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    response_text = response.text

    if not response_text:
        raise ValueError(
            "The LLM returned an empty response."
        )

    response_text = clean_json_response(
        response_text
    )

    try:

        result = json.loads(
            response_text
        )

    except json.JSONDecodeError as e:

        raise ValueError(
            "Could not parse the LLM response as JSON."
        ) from e

    return validate_result(result)