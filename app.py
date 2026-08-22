import streamlit as st

from src.resume_parser import extract_resume_text


st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Smart Resume Screener")

st.write(
    "Upload resumes and compare candidates against a job description "
    "using AI-powered semantic matching."
)


st.header("Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250
)


st.header("Upload Resume")

resume_file = st.file_uploader(
    "Upload a resume",
    type=["pdf", "txt"]
)


if resume_file:

    st.success(f"Uploaded: {resume_file.name}")

    try:
        resume_text = extract_resume_text(resume_file)

        if resume_text and len(resume_text.strip()) >= 50:

            st.subheader("Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )

        else:
            st.warning(
                "No text could be extracted from this resume."
            )

    except Exception as e:

        st.error(
            f"Error while processing resume: {e}"
        )