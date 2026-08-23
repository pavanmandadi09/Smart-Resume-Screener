import re


COMMON_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "html",
    "css",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",

    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "opencv",

    "data structures",
    "algorithms",
    "data structures and algorithms",

    "rest api",
    "rest apis",
    "api",
    "git",
    "github",

    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",

    "mongodb",
    "mysql",
    "postgresql",

    "react",
    "node.js",
    "flask",
    "django",
    "spring",
    "spring boot"
]


def normalize_skill(skill):
    """
    Normalize a skill name.
    """

    skill = skill.strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill


def extract_skills(text):
    """
    Extract known technical skills from text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:

        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text_lower):

            normalized_skill = normalize_skill(skill)

            if normalized_skill not in found_skills:

                found_skills.append(
                    normalized_skill
                )

    return found_skills