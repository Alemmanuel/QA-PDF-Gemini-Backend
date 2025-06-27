from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.vector import get_vectorstore

def ask_question(question):
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever()

    model = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash-8b",
        temperature=0.3
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever
    )

    return qa_chain.run(question)
