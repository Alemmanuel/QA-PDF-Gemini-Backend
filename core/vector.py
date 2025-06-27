from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

CHROMA_DIR = "./vectorstore"
_vectordb = None

def get_vectorstore():
    global _vectordb
    if _vectordb is None:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        _vectordb = Chroma(
            persist_directory=CHROMA_DIR,
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
