from pypdf import PdfReader


def extract_text_from_pdf(file):
    """
    Extract text from a PDF resume.

    Args:
        file: Uploaded PDF file object.

    Returns:
        Extracted text as a string.
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

    Args:
        file: Uploaded TXT file object.

    Returns:
        Extracted text as a string.
    """
    return file.read().decode("utf-8").strip()


def extract_resume_text(file):
    """
    Extract text from a supported resume file.

    Supports:
        - PDF
        - TXT

    Args:
        file: Uploaded resume file.

    Returns:
        Extracted resume text.
    """
    file_type = file.name.lower().split(".")[-1]

    if file_type == "pdf":
        return extract_text_from_pdf(file)

    if file_type == "txt":
        return extract_text_from_txt(file)

    raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")