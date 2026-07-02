from typing import Any
from langchain_core.messages import HumanMessage

try:
    from langchain.memory import ConversationBufferWindowMemory as _ConversationBufferWindowMemory
except ImportError:
    class _ConversationBufferWindowMemory:
        def __init__(self, k: int = 5):
            self.k = k

        def save_context(self, inputs: dict[str, Any], outputs: dict[str, Any]) -> None:
            return None

        def load_memory_variables(self, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
            return {}

        def clear(self) -> None:
            return None


ConversationBufferWindowMemory = _ConversationBufferWindowMemory


class RAGAgent:
    def __init__(self, agent, memory: Any | None = None):

        #Se inicializa el agente con memoria y un ejecutor compatible con la versión

        self.agent = agent
        self.memory = memory
        self.agent_executor = None

        try:
            from langchain.agents import AgentExecutor
        except ImportError:
            AgentExecutor = None

        if AgentExecutor is not None:
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=getattr(agent, "tools", []),
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
            )

    def _extract_text(self, response: Any) -> str:
        if isinstance(response, dict):
            if "output" in response:
                return str(response["output"])
            if "messages" in response:
                messages = response["messages"]
                if messages:
                    last_message = messages[-1]
                    if hasattr(last_message, "content"):
                        content = last_message.content
                        if isinstance(content, list):
                            return "\n".join(str(item) for item in content)
                        return str(content)
            if "result" in response:
                return str(response["result"])
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, list):
                return "\n".join(str(item) for item in content)
            return str(content)
        return str(response)

    def ask(self, query: str) -> str:
  
        #Procesa la consulta del usuario y devuelve una respuesta.

        try:
            if self.agent_executor is not None:
                response = self.agent_executor.invoke({"input": query})
            else:
                response = self.agent.invoke(
                    {"messages": [HumanMessage(content=query)]}
                )
            return self._extract_text(response)
        except Exception as exc:
            return f"Error procesando la consulta: {str(exc)}"

