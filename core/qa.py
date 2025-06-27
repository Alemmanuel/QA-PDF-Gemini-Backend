from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from core.vector import get_vectorstore

def ask_question(question: str):
    import os
    vectorstore_path = os.environ.get('VECTORSTORE_PATH', '/tmp/vectorstore')
    from langchain_community.vectorstores import Chroma
    from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma(persist_directory=vectorstore_path, embedding_function=embeddings)
    retriever = vectordb.as_retriever()
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.chains import RetrievalQA
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=0.2)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.invoke({"query": question})
