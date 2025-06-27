from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.vector import get_vectorstore
import os

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(documents)

    # Usar /tmp/vectorstore para compatibilidad con Render
    vectorstore_path = os.environ.get('VECTORSTORE_PATH', '/tmp/vectorstore')
    vectordb = get_vectorstore(vectorstore_path)
    vectordb.add_documents(docs)
    vectordb.persist()
