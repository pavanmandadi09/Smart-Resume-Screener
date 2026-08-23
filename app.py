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
# HELPER FUNCTION - RECOMMENDATION
# =========================================================

def get_recommendation(score):
    """
    Convert the AI score into a recruiter-friendly
    recommendation.
    """

    if score >= 9:
        return "🟢 Strong Match"

    if score >= 7:
        return "🟢 Good Match"

    if score >= 5:
        return "🟡 Moderate Match"

    if score >= 3:
        return "🟠 Weak Match"

    return "🔴 Poor Match"


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
        "Python, Java, SQL and data structures knowledge.\n\n"
        "Candidates should have experience with machine learning, "
        "REST APIs, Git and software development."
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

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

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
            # CANDIDATE SUMMARY
            # =================================================

            st.header(
                "👤 Candidate Summary"
            )


            summary_col1, summary_col2, summary_col3 = st.columns(
                3
            )


            with summary_col1:

                st.write("**Name**")

                st.write(
                    resume_data["name"]
                    if resume_data["name"]
                    else "Not detected"
                )


            with summary_col2:

                st.write("**Email**")

                st.write(
                    resume_data["email"]
                    if resume_data["email"]
                    else "Not detected"
                )


            with summary_col3:

                st.write("**Phone**")

                st.write(
                    resume_data["phone"]
                    if resume_data["phone"]
                    else "Not detected"
                )


            # =================================================
            # PROFILE
            # =================================================

            if resume_data["profile"]:

                st.subheader(
                    "Profile"
                )

                st.write(
                    resume_data["profile"]
                )


            # =================================================
            # STRUCTURED RESUME
            # =================================================

            with st.expander(
                "📋 View Structured Resume"
            ):

                col1, col2 = st.columns(2)


                # =================================================
                # LEFT COLUMN
                # =================================================

                with col1:

                    st.write(
                        "### Skills"
                    )

                    if resume_data["skills"]:

                        st.write(
                            resume_data["skills"]
                        )

                    else:

                        st.info(
                            "No skills section detected."
                        )


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


                # =================================================
                # RIGHT COLUMN
                # =================================================

                with col2:

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
            # SKILL ANALYSIS
            # =================================================

            st.header(
                "🛠️ Skill Analysis"
            )


            skills_col1, skills_col2 = st.columns(2)


            # =================================================
            # RESUME SKILLS
            # =================================================

            with skills_col1:

                st.subheader(
                    "Resume Skills"
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

                st.subheader(
                    "Job Required Skills"
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
            # BASIC KEYWORD MATCHING
            # =================================================

            basic_result = None


            if resume_skills and job_skills:

                basic_result = compare_skills(
                    resume_skills,
                    job_skills
                )


                st.subheader(
                    "📊 Keyword Match Analysis"
                )


                metric_col1, metric_col2 = st.columns(2)


                with metric_col1:

                    st.metric(
                        "Keyword Skill Match",
                        f"{basic_result['match_percentage']}%"
                    )


                with metric_col2:

                    st.progress(
                        basic_result["match_percentage"] / 100
                    )


                match_col1, match_col2 = st.columns(2)


                # =================================================
                # MATCHING SKILLS
                # =================================================

                with match_col1:

                    st.write(
                        "### ✅ Matching Skills"
                    )


                    if basic_result[
                        "matching_skills"
                    ]:

                        for skill in basic_result[
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


                    if basic_result[
                        "missing_skills"
                    ]:

                        for skill in basic_result[
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
                    "Use Gemini AI to perform a semantic evaluation "
                    "of the candidate against the job description."
                )


                # -------------------------------------------------
                # Gemini API key
                # -------------------------------------------------

                api_key = st.secrets.get(
                    "GEMINI_API_KEY",
                    ""
                )


                # -------------------------------------------------
                # Analyze button
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
                            "Please add GEMINI_API_KEY to Streamlit Secrets."
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


                                st.session_state[
                                    "ai_result"
                                ] = ai_result


                            except Exception as e:

                                error_message = str(e)


                                if (
                                    "429" in error_message
                                    or
                                    "RESOURCE_EXHAUSTED"
                                    in error_message
                                ):

                                    st.error(
                                        "Gemini API rate limit reached."
                                    )

                                    st.info(
                                        "Please wait before trying again."
                                    )

                                else:

                                    st.error(
                                        f"AI analysis failed: {e}"
                                    )


                # -------------------------------------------------
                # Retrieve previous AI result
                # -------------------------------------------------

                ai_result = st.session_state.get(
                    "ai_result"
                )


                # =================================================
                # DISPLAY AI RESULT
                # =================================================

                if ai_result:

                    score = ai_result["score"]

                    recommendation = get_recommendation(
                        score
                    )


                    # =================================================
                    # SCORE + RECOMMENDATION
                    # =================================================

                    st.subheader(
                        "🎯 Final Candidate Assessment"
                    )


                    score_col1, score_col2 = st.columns(2)


                    with score_col1:

                        st.metric(
                            "AI Match Score",
                            f"{score} / 10"
                        )

                        st.progress(
                            score / 10
                        )


                    with score_col2:

                        st.metric(
                            "Recruiter Recommendation",
                            recommendation
                        )


                    # =================================================
                    # AI MATCHING / MISSING SKILLS
                    # =================================================

                    ai_col1, ai_col2 = st.columns(2)


                    # -------------------------------------------------
                    # AI Matching Skills
                    # -------------------------------------------------

                    with ai_col1:

                        st.subheader(
                            "✅ AI Matching Skills"
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


                    # -------------------------------------------------
                    # AI Missing Skills
                    # -------------------------------------------------

                    with ai_col2:

                        st.subheader(
                            "❌ AI Missing Skills"
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


                    # =================================================
                    # AI JUSTIFICATION
                    # =================================================

                    st.subheader(
                        "📝 AI Justification"
                    )

                    st.write(
                        ai_result["justification"]
                    )


                    # =================================================
                    # SCREENING REPORT
                    # =================================================

                    st.divider()

                    st.subheader(
                        "📄 Screening Report"
                    )


                    report = []

                    report.append(
                        "SMART RESUME SCREENER"
                    )

                    report.append(
                        "=" * 60
                    )

                    report.append("")

                    report.append(
                        "CANDIDATE INFORMATION"
                    )

                    report.append(
                        "-" * 60
                    )

                    report.append(
                        f"Name: {resume_data['name'] or 'Not detected'}"
                    )

                    report.append(
                        f"Email: {resume_data['email'] or 'Not detected'}"
                    )

                    report.append(
                        f"Phone: {resume_data['phone'] or 'Not detected'}"
                    )

                    report.append("")

                    report.append(
                        "JOB DESCRIPTION"
                    )

                    report.append(
                        "-" * 60
                    )

                    report.append(
                        job_description
                    )

                    report.append("")

                    report.append(
                        "DETECTED RESUME SKILLS"
                    )

                    report.append(
                        "-" * 60
                    )

                    for skill in resume_skills:

                        report.append(
                            f"- {skill}"
                        )

                    report.append("")


                    # =================================================
                    # KEYWORD MATCH REPORT
                    # =================================================

                    if basic_result:

                        report.append(
                            "KEYWORD MATCH ANALYSIS"
                        )

                        report.append(
                            "-" * 60
                        )

                        report.append(
                            f"Keyword Match: "
                            f"{basic_result['match_percentage']}%"
                        )

                        report.append("")

                        report.append(
                            "Matching Skills:"
                        )

                        for skill in basic_result[
                            "matching_skills"
                        ]:

                            report.append(
                                f"- {skill}"
                            )

                        report.append("")

                        report.append(
                            "Missing Skills:"
                        )

                        for skill in basic_result[
                            "missing_skills"
                        ]:

                            report.append(
                                f"- {skill}"
                            )

                        report.append("")


                    # =================================================
                    # AI REPORT
                    # =================================================

                    report.append(
                        "AI RESUME EVALUATION"
                    )

                    report.append(
                        "-" * 60
                    )

                    report.append(
                        f"AI Match Score: {score} / 10"
                    )

                    report.append(
                        f"Recommendation: {recommendation}"
                    )

                    report.append("")

                    report.append(
                        "AI Matching Skills:"
                    )

                    for skill in ai_result[
                        "matching_skills"
                    ]:

                        report.append(
                            f"- {skill}"
                        )

                    report.append("")

                    report.append(
                        "AI Missing Skills:"
                    )

                    for skill in ai_result[
                        "missing_skills"
                    ]:

                        report.append(
                            f"- {skill}"
                        )

                    report.append("")

                    report.append(
                        "AI Justification:"
                    )

                    report.append(
                        ai_result["justification"]
                    )

                    report.append("")

                    report.append(
                        "=" * 60
                    )

                    report.append(
                        "Generated by Smart Resume Screener"
                    )


                    report_text = "\n".join(
                        report
                    )


                    # =================================================
                    # DOWNLOAD REPORT
                    # =================================================

                    st.download_button(
                        label="⬇️ Download Screening Report",
                        data=report_text,
                        file_name=(
                            "resume_screening_report.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True
                    )


        else:

            st.warning(
                "Could not extract enough text from this resume."
            )


    except Exception as e:

        st.error(
            f"Error while processing resume: {e}"
        )