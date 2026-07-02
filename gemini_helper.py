from google import genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

def analyze_resume(resume_text, job_description):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "AI feedback is unavailable because GEMINI_API_KEY is not configured. ATS score is still available."

    prompt = f"""
    Compare this resume with the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. Match Summary
    2. Missing Skills
    3. Suggestions
    4.ATS Score
    """
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception:
        return "AI service temporarily unavailable. ATS score is still available."
