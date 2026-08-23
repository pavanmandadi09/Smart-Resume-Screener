import streamlit as st

from src.resume_parser import extract_resume_text, parse_resume


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

            # ---------------------------------
            # Raw Resume Text
            # ---------------------------------

            st.subheader("Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )


            # ---------------------------------
            # Structured Resume
            # ---------------------------------

            resume_data = parse_resume(resume_text)

            st.subheader("Structured Resume")


            col1, col2 = st.columns(2)


            with col1:

                st.write("### Personal Information")

                st.write("**Name**")
                st.write(resume_data["name"])

                st.write("**Email**")
                st.write(resume_data["email"])

                st.write("**Phone**")
                st.write(resume_data["phone"])


                st.write("### Skills")

                st.write(resume_data["skills"])


            with col2:

                st.write("### Education")

                st.write(resume_data["education"])


                st.write("### Experience")

                st.write(resume_data["experience"])


                st.write("### Projects")

                st.write(resume_data["projects"])


                st.write("### Certifications")

                st.write(resume_data["certifications"])


        else:

            st.warning(
                "Could not extract enough text from this resume."
            )


    except Exception as e:

        st.error(
            f"Error while processing resume: {e}"
        )