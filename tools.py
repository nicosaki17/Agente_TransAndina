from langchain.tools import tool

def build_tools(retriever):

    #Construir herramientas para el agente
    @tool
    def consultar_manuales_tecnicos(query: str):

        # Buscar en documentos
        docs = retriever.invoke(query)
        # Formateo de datos
        return "\n\n".join([d.page_content for d in docs])

    return [consultar_manuales_tecnicos]