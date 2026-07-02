import os
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

from agents import ConversationBufferWindowMemory, RAGAgent
from tools import build_tools

load_dotenv()

INDEX_DIR = "index_transandina"

def load_vector_db(index_dir: str = INDEX_DIR) -> FAISS:
    #Carga el índice local usando embeddings de HuggingFace (Local).
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    except Exception as exc:
        raise RuntimeError(f"Índice {index_dir} no encontrado. Ejecuta primero ingesta.py") from exc

def build_llm() -> ChatOllama:
    #Configura el modelo local Llama 3 con soporte para herramientas.
    return ChatOllama(model="llama3.1", temperature=0)

def build_agent_executor() -> RAGAgent:
    #Construye el agente RAG
    # 1. Carga base de datos vectorial
    vector_db = load_vector_db()
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # 2. Construcción herramientas
    tools = build_tools(retriever)
    
    # 3. Configuración memoria y LLM
    memory = ConversationBufferWindowMemory(k=5)
    llm = build_llm()

    # 4. Prompt para el "Ingeniero de Soporte"
    system_prompt = (
        "Eres el Ingeniero de Soporte Senior de TransAndina S.A. "
        "Tu objetivo es el mantenimiento preventivo y correctivo de la flota pesada. "
        "DEBES seguir estrictamente el patrón: Thought -> Action -> Observation -> Final Answer. "
        "Usa la herramienta disponible para buscar en los manuales técnicos antes de responder. "
        "Si la información no está en los manuales, infórmalo explícitamente."
    )

    # 5. Creación del agente
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        debug=True,
    )
    
    return RAGAgent(agent, memory)