from langchain.tools import tool


def build_tools(retriever):

    # Construir herramientas para el agente
    @tool
    def consultar_manuales_tecnicos(query: str):
        """Busca información técnica relevante en los manuales del camión para responder preguntas del operador."""
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

    return [consultar_manuales_tecnicos]