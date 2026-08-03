📄 Resume Gap Analyser
A Streamlit-based AI tool that helps job seekers and recruiters compare a resume against a target Job Description (JD). Powered by LangChain, this app dynamically connects to various LLM providers (OpenAI, Anthropic, Google, etc.) to identify missing skills, highlight experience discrepancies, and provide actionable recommendations.

✨ Features
Multi-Format Support: Upload resumes in .pdf or .docx formats.

LLM Agnostic: Choose between multiple AI providers (OpenAI, Anthropic, Google, Cohere, Ollama) directly from the UI.

Customizable Parameters: Tweak hyperparameters like Temperature and Max Tokens to control the creativity and length of the analysis.

Secure API Key Handling: Enter your API key securely via the Streamlit UI (passwords are masked and not hardcoded).

Rich Markdown Reports: Get clear, well-formatted feedback highlighting exactly what you need to work on to land the job.

🔄 How It Works (The Workflow)
Model Configuration:

In the sidebar, select your preferred AI provider, model name, and paste your API key.

Adjust the temperature and token limits if desired.

Document Upload:

Upload your resume. The app securely saves it to a temporary file, extracts the text using LangChain's PyPDFLoader or Docx2txtLoader, and immediately deletes the temporary file to protect your data.

Job Description Input:

Paste the full text of the Job Description you are targeting into the text area.

AI Analysis:

Click Analyze Gaps. The app builds a customized prompt containing your resume and the JD, acting as an "expert technical recruiter."

Insights Delivery:

The LLM processes the data and outputs a comprehensive Gap Analysis Report directly on the screen, detailing missing skills, experience gaps, and actionable advice.

🛠️ Prerequisites & Installation
Make sure you have Python 3.8+ installed.

1. Clone or download the repository.

2. Install the required dependencies:
You will need Streamlit, LangChain, and the document parsing libraries. Run the following command in your terminal:

```bash
pip install streamlit langchain langchain-community pypdf docx2txt
```
(Note: Depending on the model provider you choose, you may also need to install their specific SDK, e.g., pip install langchain-openai, langchain-anthropic, or langchain-google-genai)

3. Optional Settings File:
The app looks for a settings.json file in the root directory to load default configurations. You can create one like this:

```json
{
  "model_configuration": {
    "model_provider": "openai",
    "model": "gpt-4o",
    "extra_params": {
      "temperature": 0.7,
      "max_tokens": 1024
    }
  }
}
```

(If you don't create this file, the app will safely fall back to its internal defaults).

🚀 Running the App
Run the following command in your terminal:
```bash
streamlit run app.py
```

The application will open automatically in your default web browser at http://localhost:8501. Enter your API key in the sidebar, upload a resume, paste a JD, and start analyzing!