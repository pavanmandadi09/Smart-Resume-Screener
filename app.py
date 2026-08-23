import streamlit as st

from src.resume_parser import extract_resume_text, parse_resume
from src.skill_extractor import extract_skills


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Resume Screener",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# APPLICATION TITLE
# =========================================================

st.title("📄 Smart Resume Screener")

st.write(
    "Upload resumes and compare candidates against a job description "
    "using AI-powered semantic matching."
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.header("Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250
)


# =========================================================
# JOB SKILL EXTRACTION
# =========================================================

job_skills = []

if job_description.strip():

    job_skills = extract_skills(
        job_description
    )


# =========================================================
# RESUME UPLOAD
# =========================================================

st.header("Upload Resume")

resume_file = st.file_uploader(
    "Upload a resume",
    type=["pdf", "txt"]
)


# =========================================================
# RESUME PROCESSING
# =========================================================

if resume_file:

    st.success(
        f"Uploaded: {resume_file.name}"
    )

    try:

        # -------------------------------------------------
        # Extract resume text
        # -------------------------------------------------

        resume_text = extract_resume_text(
            resume_file
        )


        if resume_text and len(
            resume_text.strip()
        ) >= 50:

            # -------------------------------------------------
            # Raw Resume Text
            # -------------------------------------------------

            st.subheader(
                "Extracted Resume Text"
            )

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )


            # -------------------------------------------------
            # Parse Resume
            # -------------------------------------------------

            resume_data = parse_resume(
                resume_text
            )


            # -------------------------------------------------
            # Structured Resume
            # -------------------------------------------------

            st.subheader(
                "Structured Resume"
            )


            # -------------------------------------------------
            # Profile
            # -------------------------------------------------

            if resume_data["profile"]:

                st.write("### Profile")

                st.write(
                    resume_data["profile"]
                )


            # -------------------------------------------------
            # Two-column layout
            # -------------------------------------------------

            col1, col2 = st.columns(2)


            # =================================================
            # LEFT COLUMN
            # =================================================

            with col1:

                st.write(
                    "### Personal Information"
                )

                st.write("**Name**")

                st.write(
                    resume_data["name"]
                )


                st.write("**Email**")

                st.write(
                    resume_data["email"]
                )


                st.write("**Phone**")

                st.write(
                    resume_data["phone"]
                )


                # ---------------------------------------------
                # Skills
                # ---------------------------------------------

                st.write("### Skills")

                if resume_data["skills"]:

                    st.write(
                        resume_data["skills"]
                    )

                else:

                    st.info(
                        "No skills section detected."
                    )


            # =================================================
            # RIGHT COLUMN
            # =================================================

            with col2:

                # ---------------------------------------------
                # Education
                # ---------------------------------------------

                st.write("### Education")

                if resume_data["education"]:

                    st.write(
                        resume_data["education"]
                    )

                else:

                    st.info(
                        "No education section detected."
                    )


                # ---------------------------------------------
                # Experience
                # ---------------------------------------------

                st.write("### Experience")

                if resume_data["experience"]:

                    st.write(
                        resume_data["experience"]
                    )

                else:

                    st.info(
                        "No experience section detected."
                    )


                # ---------------------------------------------
                # Projects
                # ---------------------------------------------

                st.write("### Projects")

                if resume_data["projects"]:

                    st.write(
                        resume_data["projects"]
                    )

                else:

                    st.info(
                        "No projects section detected."
                    )


                # ---------------------------------------------
                # Certifications
                # ---------------------------------------------

                st.write(
                    "### Certifications"
                )

                if resume_data["certifications"]:

                    st.write(
                        resume_data["certifications"]
                    )

                else:

                    st.info(
                        "No certifications section detected."
                    )


            # =================================================
            # DETECTED SKILLS
            # =================================================

            st.subheader(
                "Detected Skills"
            )


            skills_col1, skills_col2 = st.columns(2)


            # -------------------------------------------------
            # Resume Skills
            # -------------------------------------------------

            with skills_col1:

                st.write(
                    "### Resume Skills"
                )

                resume_skills = extract_skills(
                    resume_data["skills"]
                )


                if resume_skills:

                    for skill in resume_skills:

                        st.write(
                            f"• {skill}"
                        )

                else:

                    st.info(
                        "No recognized skills found in resume."
                    )


            # -------------------------------------------------
            # Job Required Skills
            # -------------------------------------------------

            with skills_col2:

                st.write(
                    "### Job Required Skills"
                )


                if job_skills:

                    for skill in job_skills:

                        st.write(
                            f"• {skill}"
                        )

                else:

                    st.info(
                        "No recognized skills found in job description."
                    )


        else:

            st.warning(
                "Could not extract enough text from this resume."
            )


    except Exception as e:

        st.error(
            f"Error while processing resume: {e}"
        )