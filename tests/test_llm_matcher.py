import os

from src.llm_matcher import analyze_resume


resume_text = """
Software Engineer with experience in Python, Java and SQL.

Skills:
Python
Java
SQL
Git
Machine Learning

Projects:
Built a machine learning application using Python and
scikit-learn.
"""


job_description = """
We are looking for a Software Engineer with strong
Python, Java, SQL and data structures knowledge.

Candidates should have experience with machine learning,
REST APIs, Git and software development.
"""


api_key = os.getenv(
    "GEMINI_API_KEY"
)


if not api_key:

    print(
        "GEMINI_API_KEY environment variable is not set."
    )

else:

    result = analyze_resume(
        resume_text,
        job_description,
        api_key
    )

    print("\nScore:")
    print(result["score"])

    print("\nMatching Skills:")

    for skill in result["matching_skills"]:
        print("-", skill)

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print("-", skill)

    print("\nJustification:")
    print(result["justification"])