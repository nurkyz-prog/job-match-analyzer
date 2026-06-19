import streamlit as st
from anthropic import Anthropic
import json

st.set_page_config(page_title="Job Match Analyzer", page_icon="📊")
st.title("📊 Job Match Analyzer")
st.write(
    "Paste your CV and a job description below to see how well they match, "
    "and which of your skills to highlight."
)

api_key = st.text_input(
    "Anthropic API Key",
    type="password",
    help="Get one at console.anthropic.com. Not stored anywhere — only used for this session.",
)

cv_text = st.text_area("Your CV text", height=200, placeholder="Paste your CV content here...")
job_text = st.text_area("Job description", height=200, placeholder="Paste the job posting here...")

if st.button("Analyze Match"):
    if not api_key or not cv_text or not job_text:
        st.warning("Please fill in the API key, CV text, and job description.")
    else:
        client = Anthropic(api_key=api_key)

        prompt = f"""You are a career advisor. Compare the CV below against the job description.

CV:
{cv_text}

Job Description:
{job_text}

Respond ONLY with valid JSON in this exact format, no other text before or after:
{{
  "match_score": <integer 0-100>,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "highlight_suggestions": ["suggestion1", "suggestion2"]
}}
"""

        with st.spinner("Analyzing..."):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            raw_text = response.content[0].text

        try:
            result = json.loads(raw_text)

            st.metric("Match Score", f"{result['match_score']}/100")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Matching Skills")
                for skill in result["matching_skills"]:
                    st.write(f"- {skill}")
            with col2:
                st.subheader("⚠️ Skills to Develop")
                for skill in result["missing_skills"]:
                    st.write(f"- {skill}")

            st.subheader("💡 What to Highlight")
            for suggestion in result["highlight_suggestions"]:
                st.write(f"- {suggestion}")

        except json.JSONDecodeError:
            st.error("Couldn't parse the model's response as JSON. Raw output below:")
            st.write(raw_text)
