import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, TextLoader
from utils import load_db
import tempfile

#I have used Azure OpenAI API Key for this bot, if ypu are using OpenAI, please follow the syntax from OpenAI Website.
# Initialize Azure OpenAI client
openai_api_key = ""
azure_endpoint = ""
azure_deployment_name = ""
azure_api_version = ""

llm = AzureChatOpenAI(
    api_key=openai_api_key,
    azure_endpoint=azure_endpoint,
    deployment_name=azure_deployment_name,
    api_version=azure_api_version,
    temperature=0,
    max_tokens=500
)

# Streamlit app
st.title('Chat with Your Data Bot')
st.sidebar.header('Upload a PDF or TXT file')

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt"])



# Once the file is uploaded, the code creates a local db file, here it is creating a Chroma based DB.
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    
    # Create a temporary file to save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    if file_extension == 'pdf':
        loader = PyPDFLoader(tmp_file_path)
    elif file_extension == 'txt':
        loader = TextLoader(tmp_file_path)
    else:
        st.error('Unsupported file type!')

    documents = loader.load()
    qa = load_db(documents, llm)

    st.session_state.qa = qa
    st.session_state.chat_history = []

    st.success(f'Loaded file: {uploaded_file.name}')


if 'qa' in st.session_state:
    user_query = st.text_input("Enter your question:")

    if st.button('Submit'):
        result = st.session_state.qa({"question": user_query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.extend([(user_query, result["answer"])])

# The output shows the answer, the original query and the sourced paragraphs with in the file.
        st.write(f"**User:** {user_query}")
        st.write(f"**ChatBot:** {result['answer']}")

        st.write("**DB Query:**", result["generated_question"])
        st.write("**Source Documents:**")
        for doc in result["source_documents"]:
            st.write(doc)

    if st.button('Clear History'):
        st.session_state.chat_history = []
        st.write("Chat history cleared!")
