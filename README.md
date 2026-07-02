# TransAndina Support Agent

Este proyecto implementa un asistente técnico para TransAndina S.A. basado en recuperación de información (RAG) y agentes de LangChain. Su objetivo es ayudar a operarios y personal de mantenimiento a obtener respuestas técnicas útiles a partir de manuales y documentación interna, sin depender de un backend complejo ni de servicios externos durante la consulta.

## Qué resuelve

El sistema permite hacer preguntas sobre mantenimiento preventivo y correctivo, procedimientos técnicos, especificaciones, códigos de error y otras referencias del área operativa. En lugar de responder desde memoria del modelo, el agente consulta primero una base vectorial construida con los documentos técnicos del proyecto.

## Decisiones de diseño

### 1. Arquitectura local-first

Se priorizó un diseño que funcione de forma local siempre que sea posible:

- El modelo de lenguaje se ejecuta mediante Ollama.
- Los embeddings se generan con HuggingFace.
- El índice vectorial se almacena localmente en FAISS.

Esta decisión reduce la dependencia de APIs externas y facilita la ejecución en entornos con menor infraestructura.

### 2. Enfoque RAG con herramienta explícita

El agente no responde solo con el conocimiento del modelo. En cambio, utiliza una herramienta llamada consultar_manuales_tecnicos para recuperar fragmentos relevantes de la base vectorial antes de generar una respuesta.

Esto aporta dos beneficios clave:

- mejora la fidelidad técnica de las respuestas;
- reduce la probabilidad de inventar información.

### 3. Separación de responsabilidades

El proyecto está dividido en módulos para mantener el código legible y facilitar cambios futuros:

- ingestión de documentos;
- construcción del índice vectorial;
- definición de herramientas para el agente;
- creación del agente y manejo de memoria;
- interfaz de usuario por consola.

Esta separación hace que cada componente tenga un propósito claro y que el sistema sea más fácil de extender.

### 4. Compatibilidad y simplicidad operativa

Se optó por una interfaz simple de consola para que el sistema sea fácil de probar y usar en contexto operativo. El flujo es directo: el usuario pregunta, el agente recupera contexto y responde.

## Estructura del proyecto

- [main.py](main.py): punto de entrada de la aplicación. Inicia la interfaz CLI y conecta al agente.
- [tasks.py](tasks.py): orquesta la construcción del agente. Carga el índice, define el LLM, crea el retriever y arma la herramienta disponible.
- [agents.py](agents.py): encapsula la lógica del agente y adapta la ejecución a la versión actual de LangChain.
- [tools.py](tools.py): define las herramientas que el agente puede usar durante la conversación.
- [ingesta.py](ingesta.py): procesa los documentos de la carpeta data y genera el índice FAISS.
- [data/](data): documentos fuente usados para construir el conocimiento del sistema.
- [index_transandina/](index_transandina): índice vectorial persistido para recuperación semántica.

## Integración entre módulos

La arquitectura funciona como una pipeline de tres capas:

1. Ingesta de conocimiento
   - [ingesta.py](ingesta.py) carga documentos de texto desde [data/](data).
   - Divide los textos en chunks.
   - Genera embeddings y crea el índice FAISS en [index_transandina/](index_transandina).

2. Construcción del agente
   - [tasks.py](tasks.py) carga el índice vectorial.
   - Convierte el índice en un retriever.
   - Crea la herramienta de búsqueda y la asocia al modelo.
   - Define un prompt de sistema orientado a soporte técnico.

3. Ejecución de consultas
   - [main.py](main.py) inicia el ciclo de interacción.
   - Cada pregunta del usuario se envía al agente.
   - El agente usa la herramienta de recuperación para obtener contexto relevante.
   - El modelo genera una respuesta final basada en ese contexto.

## Flujo de ejecución

1. Se ejecuta [ingesta.py](ingesta.py) para preparar el conocimiento.
2. Se levanta la aplicación con [main.py](main.py).
3. El usuario escribe una pregunta técnica.
4. El sistema recupera documentos relevantes.
5. El modelo responde con una respuesta grounded en la documentación.

## Dependencias principales

El proyecto utiliza:

- LangChain y LangChain Community
- Ollama para ejecutar el modelo localmente
- FAISS para indexación vectorial
- HuggingFace embeddings para representación semántica
- Python dotenv para configuración

## Recomendación en caso de fallos

Para un uso correcto del sistema, conviene:

- tener instalado Ollama y el modelo configurado;
- haber ejecutado la ingesta previa para generar el índice;
- mantener los documentos fuente actualizados en [data/](data).

