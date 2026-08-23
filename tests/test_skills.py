from src.skill_extractor import extract_skills


text = """
We are looking for a Software Engineer with strong
Python, Java, SQL and data structures knowledge.

Candidates should have experience with machine learning,
REST APIs, Git and software development.
"""


skills = extract_skills(text)

print("Detected skills:")

for skill in skills:
    print("-", skill)