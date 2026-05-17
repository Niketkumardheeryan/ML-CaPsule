# PDF Chatbot using LangChain and Gemini LLM

This project demonstrates an end-to-end Chatbot application that processes PDF documents and answers user queries using the Google Gemini API, LangChain, and ChromaDB.

## 🌟 Features
- **PDF Text Extraction**: Uses `PyPDF2` to read and extract text from PDF files.
- **Text Chunking**: Breaks down large documents into smaller chunks using `RecursiveCharacterTextSplitter`.
- **Vector Embeddings**: Creates embeddings using `GoogleGenerativeAIEmbeddings` and stores them locally in `ChromaDB`.
- **RetrievalQA**: Uses `gemini-1.5-flash` to answer questions contextually based on the retrieved document chunks.

## 🛠️ Tech Stack
- **Framework**: LangChain
- **Vector Store**: ChromaDB
- **LLM**: Google Gemini API (`gemini-1.5-flash` & `embedding-001`)

## 🚀 Getting Started

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
You will need a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).
Copy `.env.example` to `.env` and add your API key:
```env
GOOGLE_API_KEY="your_api_key_here"
```

### 3. Usage
You can explore the project via the provided Jupyter Notebook:
1. Open `PDF_Chatbot.ipynb` in Jupyter Notebook, VS Code, or Google Colab.
2. Add your API Key in the specified cell.
3. Place a sample PDF named `sample.pdf` in the directory.
4. Run the cells step-by-step to see the extraction, embedding, and answering process in action!
