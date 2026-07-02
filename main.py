import os
from dotenv import load_dotenv
from tasks import build_agent_executor

def run_cli():
    # 1. Carga de variables de entorno
    load_dotenv()
    
    # 2. Construcción del agente
    print("Sistema: Inicializando Agente Técnico TransAndina...")
    try:
        rag_agent = build_agent_executor()
    except Exception as e:
        print(f"Error crítico al iniciar el agente: {e}")
        return

    # 3. Interfaz de usuario
    print("\n" + "=" * 55)
    print("SISTEMA DE SOPORTE TÉCNICO - TRANSANDINA S.A.")
    print("--- Escribe 'salir' para finalizar el sistema ---")
    print("=" * 55)

    while True:
        try:
            pregunta = input("\nOperario: ").strip()
        except EOFError:
            break

        if not pregunta:
            continue
        if pregunta.lower() in ["salir", "exit"]:
            print("Cerrando sistema de soporte...")
            break
        
        # 4. Ejecución del razonamiento
        try:
            respuesta = rag_agent.ask(pregunta)
            print(f"\nSistema: {respuesta}")
        except Exception as exc:
            print(f"\nError durante la consulta: {exc}")

if __name__ == "__main__":
    run_cli()