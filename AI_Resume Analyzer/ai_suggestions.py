from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_suggestions(text):

    prompt = f"""
    Analyze this resume and provide:

    1. Missing skills
    2. Resume improvements
    3. ATS optimization tips
    4. Suggested projects
    5. Career recommendations

    Resume:
    {text}
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error generating AI suggestions: {e}"