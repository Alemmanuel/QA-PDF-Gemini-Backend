from langchain_community.vectorstores import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

CHROMA_DIR = "./vectorstore"
_vectordb = None

def get_vectorstore(path=None):
    if path is None:
        import os
        path = os.environ.get('VECTORSTORE_PATH', '/tmp/vectorstore')
    global _vectordb
    if _vectordb is None:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        _vectordb = Chroma(
            persist_directory=path,
            embedding_function=embeddings
        )
    return _vectordb

def close_vectorstore():
    global _vectordb
    if _vectordb is not None:
        try:
            _vectordb._collection = None
            if hasattr(_vectordb, '_client') and hasattr(_vectordb._client, 'conn'):
                try:
                    _vectordb._client.conn.close()
                except:
                    pass
            del _vectordb
        except Exception as e:
            print(f"⚠️ Problema cerrando vectorstore: {e}")
        _vectordb = None
