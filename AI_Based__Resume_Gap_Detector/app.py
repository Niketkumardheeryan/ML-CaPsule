import os
import json
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
import tempfile

# 1. Load the settings file with default values
try:
    with open('settings.json', 'r') as file:
        config_data = json.load(file)
        config = config_data.get("model_configuration", {})
except FileNotFoundError:
    config = {}

# Extract defaults from JSON or use safety fallbacks
default_model = config.get("model", "gpt-4o")
default_provider = config.get("model_provider", "openai")
extra_params = config.get("extra_params", {})
default_temp = extra_params.get("temperature", 0.7)
default_tokens = extra_params.get("max_tokens", 1024)
default_base_url = config.get("base_url", "")

# 1. Set page config
st.set_page_config(page_title="Resume Gap Analyser", layout="wide", initial_sidebar_state="expanded")

# 2. Build the Streamlit Sidebar UI
st.sidebar.title("🤖 Model Configuration")

# Core init_chat_model parameters
provider = st.sidebar.selectbox(
    "Model Provider", 
    ["openai", "anthropic", "google", "ollama", "cohere"],
    index=["openai", "anthropic", "google", "ollama", "cohere"].index(default_provider)
)

model_name = st.sidebar.text_input("Model Name", value=default_model)

# API Key and Base URL inputs
api_key = st.sidebar.text_input("API Key", type="password", help="Enter your provider API key. This will be hidden.")
base_url = st.sidebar.text_input("Base URL (Optional)", value=default_base_url, help="Optional custom endpoint URL.")

# Extra parameters (kwargs)
st.sidebar.markdown("---")
st.sidebar.subheader("Hyperparameters")

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=float(default_temp), step=0.1)
max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=8192, value=int(default_tokens))

# 3. Guardrail: Ensure API key is provided before initializing the model
if not api_key:
    st.title("📄 Resume Gap Analyser")
    st.warning("⚠️ Please enter your API Key in the sidebar to initialize the model and use the application.")
    st.stop()  # Halts the execution of the rest of the script until the condition is met

# 4. Initialize the LangChain model dynamically
@st.cache_resource
def load_llm(p_provider, p_model, p_temp, p_tokens, p_api_key, p_base_url):
    kwargs = {
        "model": p_model,
        "model_provider": p_provider,
        "temperature": p_temp,
        "max_tokens": p_tokens,
        "api_key": p_api_key
    }
    # Only add base_url if it's provided so we don't overwrite provider defaults unnecessarily
    if p_base_url:
        kwargs["base_url"] = p_base_url
        
    return init_chat_model(**kwargs)

# Instantiate the model using the sidebar state
model = load_llm(provider, model_name, temperature, max_tokens, api_key, base_url)

# Main app logic
st.title("📄 Resume Gap Analyser")
st.write(f"Active Model: `{model_name}` via `{provider}`")

resume = st.file_uploader(label="Add your resume", type=["pdf", "docx"], accept_multiple_files=False)

if resume:
    try: 
        file_extension = resume.name.split(".")[-1].lower()

        # Save uploaded file to a temporary file for the loaders to read
        with tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=f".{file_extension}") as temp_file:
            temp_file.write(resume.read())
            temp_file_path = temp_file.name

        # Extract text based on file type
        if file_extension == "pdf":
            loader = PyPDFLoader(temp_file_path)
        elif file_extension == "docx":
            loader = Docx2txtLoader(temp_file_path)
            
        # Load documents and concatenate text
        documents = loader.load()
        resume_text = "\n".join([doc.page_content for doc in documents])
        
        # Clean up the temporary file
        os.remove(temp_file_path)
        
        st.success("Resume loaded successfully!")
        
        # Add Job Description Input
        st.markdown("### Target Job Description")
        job_description = st.text_area("Paste the Job Description here to analyze skill gaps:", height=200)

        # Analysis Trigger
        if st.button("Analyze Gaps", type="primary"):
            if not job_description.strip():
                st.warning("Please provide a job description for a more accurate gap analysis.")
            else:
                with st.spinner("Analyzing resume against job description..."):
                    
                    # Construct the prompt
                    prompt = f"""
                    You are an expert technical recruiter and career coach.
                    Please analyze the provided Resume against the target Job Description. 
                    
                    Identify the following:
                    1. Key Missing Skills: What required skills or tools are in the JD but missing from the resume?
                    2. Experience Gaps: Are there discrepancies in years of experience or scope of responsibilities?
                    3. Actionable Recommendations: How can the candidate improve their resume or what should they learn to bridge these gaps?

                    Job Description:
                    {job_description}

                    Resume:
                    {resume_text}
                    """
                    
                    # Call the model
                    response = model.invoke(prompt)
                    
                    # Display the results
                    st.markdown("---")
                    st.subheader("📊 Gap Analysis Report")
                    st.markdown(response.content)

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")