from google import genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

def analyze_resume(resume_text, job_description):

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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI service temporarily unavailable. ATS score is still available."