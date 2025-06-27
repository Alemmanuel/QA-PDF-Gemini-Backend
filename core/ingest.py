from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.vector import get_vectorstore
import os

def process_pdf(pdf_path):
    print(f"[DEBUG] Iniciando process_pdf con: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    try:
        documents = loader.load()
        print(f"[DEBUG] PDF cargado, {len(documents)} documentos")
    except Exception as e:
        print(f"[ERROR] Al cargar PDF: {e}")
        raise

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    try:
        docs = splitter.split_documents(documents)
        print(f"[DEBUG] PDF spliteado en {len(docs)} chunks")
    except Exception as e:
        print(f"[ERROR] Al splitear PDF: {e}")
        raise

    vectorstore_path = os.environ.get('VECTORSTORE_PATH', '/tmp/vectorstore')
    try:
        vectordb = get_vectorstore(vectorstore_path)
        vectordb.add_documents(docs)
        vectordb.persist()
        print(f"[DEBUG] Embeddings guardados en {vectorstore_path}")
    except Exception as e:
        print(f"[ERROR] Al guardar en vectorstore: {e}")
        raise
