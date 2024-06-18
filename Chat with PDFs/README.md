# CogniChat: Chat with your PDFs
## Streamlit PDF Chatbot
A Langchain app developed to chat with Multiple PDFs

This is a Streamlit application that allows users to upload multiple PDF documents and interactively chat about the content of those documents using a conversational AI model. The chatbot is designed to process PDF files, extract text from them, and generate embeddings for the text chunks using Hugging Face models. Users can ask questions about the uploaded documents, and the chatbot will provide responses based on the document content.

## Installation

1. Clone the repository:

   ```bash
   git clone repository_link
   ```

2. Navigate to the project directory:

   ```bash
   cd CogniChat
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, execute the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server locally, and you can access the application in your web browser by navigating to the provided URL.

## Features

- Upload multiple PDF documents.
- Process the uploaded documents to extract text.
- Generate embeddings for the text chunks using Hugging Face models.
- Interact with a conversational AI model to ask questions about the document content.
- View chat history and responses in real-time.

## Dependencies

- Streamlit: For building interactive web applications.
- PyPDF2: For reading PDF files and extracting text.
- langchain: For text processing and embedding generation.
- Hugging Face Transformers: For accessing pre-trained language models.
- dotenv: For loading environment variables from a .env file.


## Demonstration 

<img width="1440" alt="Screenshot 2024-03-23 at 21 09 53" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/38156858-db38-4974-926b-666812e64e5d">
<img width="1440" alt="Screenshot 2024-03-23 at 21 10 36" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/1a7b04fb-4264-4329-be21-1e94cbc1901b">
<img width="1440" alt="Screenshot 2024-04-16 at 01 18 34" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/0c0cc886-8be1-428d-ae4c-0dacb9b2a02b">


<img width="1440" alt="Screenshot 2024-04-21 at 01 23 02" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/ae9ff445-fa8f-4f7f-9ecd-b969b55a7c38">
<img width="1440" alt="Screenshot 2024-04-21 at 01 22 07" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/187b6a5d-578a-4c07-a4ad-739cc8260e6e">
<img width="1440" alt="Screenshot 2024-04-21 at 01 21 16" src="https://github.com/Rajendran2201/CogniChat/assets/137254223/c0d2e218-9cfc-4310-9e98-f48db91f0c67">





