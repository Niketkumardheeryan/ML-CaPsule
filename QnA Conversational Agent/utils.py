from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_db(documents, llm, k=4, chain_type="stuff"):
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # Ensure each document has text and metadata
    for doc in docs:
        if not hasattr(doc, 'metadata'):
            doc.metadata = {}
        doc.metadata['text'] = doc.page_content

    #Embeddings are defined here, I have used Hugging-Face based Embeddings.
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    #A Vector-Database is created from the data or the file.
    db = DocArrayInMemorySearch.from_documents(docs, embedding)

    # Retreiver is the function which retrieves the file based on similarity index.
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})

    # Conversational Chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )

    return qa
