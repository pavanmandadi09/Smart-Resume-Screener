from pypdf import PdfReader
import re


# =========================================================
# TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(file):
    """
    Extract text from a PDF resume.
    """

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_txt(file):
    """
    Extract text from a TXT resume.
    """

    return file.read().decode("utf-8").strip()


def extract_resume_text(file):
    """
    Extract text from a supported resume file.

    Supported formats:
    - PDF
    - TXT
    """

    file_type = file.name.lower().split(".")[-1]

    if file_type == "pdf":
        return extract_text_from_pdf(file)

    if file_type == "txt":
        return extract_text_from_txt(file)

    raise ValueError(
        "Unsupported file type. Please upload a PDF or TXT file."
    )


# =========================================================
# PERSONAL INFORMATION
# =========================================================

def extract_email(text):
    """
    Extract the first email address from the resume.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return ""


def extract_phone(text):
    """
    Extract a likely phone number from the resume.
    """

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return ""


def extract_name(text):
    """
    Extract a likely candidate name from the beginning
    of the resume.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    # Check the first few lines for a likely name.
    for line in lines[:5]:

        if (
            "@" not in line
            and not re.search(r"\d", line)
            and len(line.split()) <= 5
        ):
            return line

    return lines[0]


# =========================================================
# SECTION DEFINITIONS
# =========================================================

SECTION_HEADINGS = {

    "profile": [
        "professional profile",
        "profile",
        "professional summary",
        "summary",
        "career objective",
        "objective"
    ],

    "skills": [
        "technical skills summary",
        "technical skills",
        "skills summary",
        "technical proficiencies",
        "key skills",
        "skills"
    ],

    "education": [
        "academic qualifications",
        "educational background",
        "education"
    ],

    "experience": [
        "professional experience",
        "work experience",
        "internship experience",
        "experience"
    ],

    "projects": [
        "academic projects",
        "personal projects",
        "projects"
    ],

    "certifications": [
        "courses and certifications",
        "certifications",
        "certificates",
        "courses"
    ]
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    """
    Normalize extracted PDF text.
    """

    text = text.replace("\r", "\n")

    # Normalize spaces and tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive newlines.
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# =========================================================
# HEADING DETECTION
# =========================================================

def find_heading(text, section_name):
    """
    Find the position of a section heading.

    Special handling is used for multi-word headings such as
    'Skills Summary' because PDF extraction may place the
    heading and its content on the same line.
    """

    headings = SECTION_HEADINGS[section_name]

    # Check longer headings first.
    headings = sorted(
        headings,
        key=len,
        reverse=True
    )

    normalized_text = normalize_text(text)

    for heading in headings:

        escaped_heading = re.escape(heading)

        # -------------------------------------------------
        # All headings (single- or multi-word)
        # -------------------------------------------------
        #
        # Require the heading to be the only thing on its
        # line (aside from bullets/whitespace and an optional
        # trailing colon/dash). This prevents sentences such
        # as "Good communication skills and teamwork..." or
        # "...eager to build my technical skills, learn from
        # industry professionals..." from being mistaken for
        # a section heading just because the phrase appears
        # somewhere in a paragraph.
        #
        pattern = (
            rf"(?im)"
            rf"^[ \t•●▪■\-–—]*"
            rf"{escaped_heading}"
            rf"[ \t]*"
            rf"[:\-–—]?"
            rf"[ \t]*"
            rf"(?:\n|$)"
        )

        match = re.search(
            pattern,
            normalized_text
        )

        if match:
            return match.start(), match.end()

    return None, None


# =========================================================
# SECTION EXTRACTION
# =========================================================

def find_all_section_headings(text):
    """
    Find every recognized section heading in the document,
    in the order they actually appear.

    Returns a list of (start, content_start, section_name)
    tuples, sorted by position. Doing this in a single pass
    (rather than re-searching per section) guarantees a
    consistent, non-overlapping set of boundaries: a
    section's content always ends at the very next heading
    found in the document, whatever section that heading
    belongs to - including a second occurrence of the same
    heading type, if one ever appears.
    """

    normalized_text = normalize_text(text)

    found = []

    for section_name in SECTION_HEADINGS:

        start_position, content_start = find_heading(
            normalized_text,
            section_name
        )

        if start_position is not None:

            found.append(
                (start_position, content_start, section_name)
            )

    found.sort(key=lambda item: item[0])

    return normalized_text, found


def extract_section(text, section_name):
    """
    Extract the content belonging to a particular section.

    The content ends when the next heading (of any kind)
    begins, based on document order.
    """

    normalized_text, headings = find_all_section_headings(text)

    for index, (start, content_start, name) in enumerate(headings):

        if name != section_name:
            continue

        if index + 1 < len(headings):
            end_position = headings[index + 1][0]
        else:
            end_position = len(normalized_text)

        section_content = normalized_text[
            content_start:end_position
        ].strip()

        # Remove unnecessary whitespace.
        section_content = re.sub(
            r"\s+",
            " ",
            section_content
        )

        return section_content

    return ""


# =========================================================
# STRUCTURED RESUME PARSER
# =========================================================

def parse_resume(text):
    """
    Convert raw resume text into structured information.
    """

    resume_data = {

        # Personal information
        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        # Resume sections
        "profile": extract_section(
            text,
            "profile"
        ),

        "skills": extract_section(
            text,
            "skills"
        ),

        "education": extract_section(
            text,
            "education"
        ),

        "experience": extract_section(
            text,
            "experience"
        ),

        "projects": extract_section(
            text,
            "projects"
        ),

        "certifications": extract_section(
            text,
            "certifications"
        )
    }

    return resume_data