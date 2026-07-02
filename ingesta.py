import os
from dotenv import load_dotenv
import glob
from typing import Any, List
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv(dotenv_path=".env", override=True)


INDEX_DIR = "index_transandina" 
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
EMBEDDINGS_MODEL = "text-embedding-3-small"


def _build_embeddings() -> Any:
    print("Sistema: Cargando modelo de embeddings local (HuggingFace)...")
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def _get_env_var(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise EnvironmentError(f"Variable de entorno obligatoria no definida: {name}")
    return val

def _load_documents() -> List[Any]:
    #Carga documentos (.txt) de la carpeta data/
    documents: List[Any] = []
    internal_files = glob.glob("data/*.txt")

    print(f"Sistema: Cargando {len(internal_files)} archivos de texto...")

    for path in internal_files:
        try:
            loader = TextLoader(path, encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = path
            documents.extend(docs)
            print(f"Documento cargado: {path}")
        except Exception as e:
            print(f"Error cargando {path}: {e}")

    return documents


    

def build_faiss_index(index_dir: str = INDEX_DIR) -> None:
    documents = _load_documents()
    if not documents:
        raise RuntimeError("Error: Carpeta data/ vacía o sin archivos .txt válidos.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Sistema: Documentos fragmentados en {len(chunks)} partes.")

    embeddings = _build_embeddings()
    print("Sistema: Generando embeddings y creando índice FAISS...")
    
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(index_dir)
    print(f"Éxito: Índice FAISS guardado en {index_dir}.")

if __name__ == "__main__":
    build_faiss_index()