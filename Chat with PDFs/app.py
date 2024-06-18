import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from htmlTemplates import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    knowledge_base = FAISS.from_texts(text_chunks, embeddings)
    return knowledge_base

def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    huggingfacehub_api_token="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",
    model_kwargs={"temperature": 5, "max_length": 64}
)

    chain = load_qa_chain(llm, chain_type="stuff")
    return chain

def handle_userinput(user_question):
    docs = st.session_state.vectorstore.similarity_search(user_question)
    chain = st.session_state.chain
    response = chain.run(input_documents=docs, question=user_question)
    st.write(response)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
  
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "chain" not in st.session_state:
        st.session_state.chain = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                st.session_state.vectorstore = get_vectorstore(text_chunks)
                st.session_state.chain = get_conversation_chain(st.session_state.vectorstore)

if __name__ == '__main__':
    main()
