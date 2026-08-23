import streamlit as st

from src.resume_parser import extract_resume_text, parse_resume
from src.skill_extractor import extract_skills
from src.matcher import compare_skills
from src.llm_matcher import analyze_resume


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
    "Upload a resume and compare the candidate against "
    "a job description using AI-powered analysis."
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.header("Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250,
    placeholder=(
        "Example:\n"
        "We are looking for a Software Engineer with strong "
        "Python, Java, SQL and data structures knowledge."
    )
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

            # =================================================
            # EXTRACTED RESUME TEXT
            # =================================================

            st.subheader(
                "Extracted Resume Text"
            )

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )


            # =================================================
            # PARSE RESUME
            # =================================================

            resume_data = parse_resume(
                resume_text
            )


            # =================================================
            # STRUCTURED RESUME
            # =================================================

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

                # ---------------------------------------------
                # Personal Information
                # ---------------------------------------------

                st.write(
                    "### Personal Information"
                )

                st.write("**Name**")

                st.write(
                    resume_data["name"]
                    if resume_data["name"]
                    else "Not detected"
                )


                st.write("**Email**")

                st.write(
                    resume_data["email"]
                    if resume_data["email"]
                    else "Not detected"
                )


                st.write("**Phone**")

                st.write(
                    resume_data["phone"]
                    if resume_data["phone"]
                    else "Not detected"
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

                st.write(
                    "### Education"
                )

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

                st.write(
                    "### Experience"
                )

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

                st.write(
                    "### Projects"
                )

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


            # =================================================
            # RESUME SKILLS
            # =================================================

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


            # =================================================
            # JOB REQUIRED SKILLS
            # =================================================

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


            # =================================================
            # BASIC SKILL MATCHING
            # =================================================

            if resume_skills and job_skills:

                result = compare_skills(
                    resume_skills,
                    job_skills
                )


                st.subheader(
                    "Resume Match Analysis"
                )


                # -------------------------------------------------
                # Match percentage
                # -------------------------------------------------

                st.metric(
                    "Keyword Skill Match",
                    f"{result['match_percentage']}%"
                )


                st.progress(
                    result["match_percentage"] / 100
                )


                # -------------------------------------------------
                # Matching and missing skills
                # -------------------------------------------------

                match_col1, match_col2 = st.columns(2)


                # =================================================
                # MATCHING SKILLS
                # =================================================

                with match_col1:

                    st.write(
                        "### ✅ Matching Skills"
                    )


                    if result["matching_skills"]:

                        for skill in result[
                            "matching_skills"
                        ]:

                            st.write(
                                f"• {skill}"
                            )

                    else:

                        st.info(
                            "No matching skills found."
                        )


                # =================================================
                # MISSING SKILLS
                # =================================================

                with match_col2:

                    st.write(
                        "### ❌ Missing Skills"
                    )


                    if result["missing_skills"]:

                        for skill in result[
                            "missing_skills"
                        ]:

                            st.write(
                                f"• {skill}"
                            )

                    else:

                        st.success(
                            "No major missing skills detected."
                        )


            # =================================================
            # AI RESUME EVALUATION
            # =================================================

            if job_description.strip():

                st.divider()

                st.header(
                    "🤖 AI Resume Evaluation"
                )


                st.write(
                    "Click the button below to perform the "
                    "AI-powered resume evaluation."
                )


                # -------------------------------------------------
                # Get Gemini API key
                # -------------------------------------------------

                api_key = st.secrets.get(
                    "GEMINI_API_KEY",
                    ""
                )


                # -------------------------------------------------
                # Analyze Resume Button
                # -------------------------------------------------

                analyze_button = st.button(
                    "🤖 Analyze Resume with AI",
                    type="primary",
                    use_container_width=True
                )


                if analyze_button:

                    if not api_key:

                        st.error(
                            "Gemini API key is not configured. "
                            "Please add GEMINI_API_KEY to "
                            "Streamlit Secrets."
                        )

                    else:

                        with st.spinner(
                            "AI is analyzing the resume..."
                        ):

                            try:

                                ai_result = analyze_resume(
                                    resume_text,
                                    job_description,
                                    api_key
                                )


                                # =================================
                                # AI SCORE
                                # =================================

                                st.subheader(
                                    "🎯 AI Match Score"
                                )


                                score_col1, score_col2 = st.columns(
                                    [1, 3]
                                )


                                with score_col1:

                                    st.metric(
                                        "Score",
                                        f"{ai_result['score']} / 10"
                                    )


                                with score_col2:

                                    st.progress(
                                        ai_result["score"] / 10
                                    )


                                # =================================
                                # AI MATCHING / MISSING SKILLS
                                # =================================

                                ai_col1, ai_col2 = st.columns(2)


                                # ---------------------------------
                                # AI Matching Skills
                                # ---------------------------------

                                with ai_col1:

                                    st.subheader(
                                        "✅ AI-Identified Matching Skills"
                                    )


                                    if ai_result[
                                        "matching_skills"
                                    ]:

                                        for skill in ai_result[
                                            "matching_skills"
                                        ]:

                                            st.write(
                                                f"• {skill}"
                                            )

                                    else:

                                        st.info(
                                            "No matching skills identified."
                                        )


                                # ---------------------------------
                                # AI Missing Skills
                                # ---------------------------------

                                with ai_col2:

                                    st.subheader(
                                        "❌ AI-Identified Missing Skills"
                                    )


                                    if ai_result[
                                        "missing_skills"
                                    ]:

                                        for skill in ai_result[
                                            "missing_skills"
                                        ]:

                                            st.write(
                                                f"• {skill}"
                                            )

                                    else:

                                        st.success(
                                            "No significant missing skills identified."
                                        )


                                # =================================
                                # AI JUSTIFICATION
                                # =================================

                                st.subheader(
                                    "📝 AI Justification"
                                )


                                st.write(
                                    ai_result["justification"]
                                )


                            except Exception as e:

                                error_message = str(e)

                                if (
                                    "429" in error_message
                                    or
                                    "RESOURCE_EXHAUSTED"
                                    in error_message
                                ):

                                    st.error(
                                        "Gemini API rate limit reached. "
                                        "Please wait and try again later."
                                    )

                                    st.info(
                                        "Your free API tier has request "
                                        "and token limits. The application "
                                        "will not automatically retry the "
                                        "request."
                                    )

                                else:

                                    st.error(
                                        f"AI analysis failed: {e}"
                                    )


        else:

            st.warning(
                "Could not extract enough text from this resume."
            )


    except Exception as e:

        st.error(
            f"Error while processing resume: {e}"
        )