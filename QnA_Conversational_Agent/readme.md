# 📚 Chat with Your Data Bot 🤖

Welcome to the **Chat with Your Data Bot** project! This powerful Streamlit application allows you to interact with your PDF or TXT documents using a conversational AI model powered by Azure OpenAI. Upload your files, ask questions, and get insightful answers along with relevant source document references. Let's dive in! 🚀

## Features ✨

- **User-Friendly Interface**: Easily upload PDF or TXT files via a clean and intuitive sidebar.
- **Conversational AI**: Leverage the capabilities of Azure OpenAI to interact with your documents.
- **Support for PDF and TXT Files**: Upload documents in PDF or TXT formats.
- **Efficient Document Retrieval**: Utilize Hugging Face embeddings and in-memory vector search for quick and accurate document retrieval.
- **Source Document Reference**: Get the answer along with the source document for better context and understanding.
- **Persistent Chat History**: Keep track of your questions and answers during the session.
- **Clear Chat History**: Option to clear the chat history and start fresh at any time.

## How to Use 🛠️

### Prerequisites

- **Azure OpenAI API Key**: Make sure you have an Azure OpenAI API key, endpoint, deployment name, and API version.

### Setup

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure Azure OpenAI**:
    - Open the `main.ipynb` file.
    - Replace the placeholders with your Azure OpenAI credentials:
      ```python
      openai_api_key = "your_api_key_here"
      azure_endpoint = "your_endpoint_here"
      azure_deployment_name = "your_deployment_name_here"
      azure_api_version = "your_api_version_here"
      ```

### Running the Application

1. **Start the Streamlit App**
2. **Upload Your File**:
    - Click on the sidebar and upload your PDF or TXT file.

3. **Ask Questions**:
    - Type your question in the text input field and hit "Submit".
    - The bot will provide an answer along with the source document references.

4. **Clear Chat History**:
    - Click the "Clear History" button to start a new session.

## Requirements 📋

Make sure to have the following libraries installed. These are specified in the `requirements.txt` file:

```plaintext
streamlit==1.7.0
langchain==0.0.92
PyPDF2==1.26.0
docarray==0.0.1
torch==1.10.1
transformers==4.15.0
