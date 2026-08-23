from src.matcher import compare_skills


resume_skills = [
    "python",
    "java",
    "sql",
    "git"
]


job_skills = [
    "python",
    "java",
    "sql",
    "data structures",
    "machine learning",
    "rest apis",
    "git"
]


result = compare_skills(
    resume_skills,
    job_skills
)


print("Matching Skills:")

for skill in result["matching_skills"]:
    print("-", skill)


print("\nMissing Skills:")

for skill in result["missing_skills"]:
    print("-", skill)


print(
    "\nMatch Percentage:",
    result["match_percentage"],
    "%"
)