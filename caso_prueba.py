from tasks import build_agent_executor

# Casos que cubren: Diagnóstico, Órdenes de Trabajo y Consultas Técnicas
# Esto para usar codigos de error, agilizando ciertas consultas
examples = [
    "Tengo el código 128 en el tablero, ¿qué debo hacer?",
    "Necesito generar una orden técnica de emergencia para un camión con sobrecalentamiento.",
    "¿A cuánto equivale 150 Nm en libras-pie para el torque del motor?",
    "¿Qué hago si escucho un ruido extraño en el motor durante la marcha?",
]

if __name__ == "__main__":
    rag_agent = build_agent_executor()
    print("--- DEMOSTRACIÓN DE CASOS DE USO: TRANSANDINA S.A. ---")
    print("=" * 60)
    
    for pregunta in examples:
        print(f"\nOperario: {pregunta}")
        try:
            respuesta = rag_agent.execute(pregunta)
            print(f"Sistema: {respuesta}")
        except Exception as exc:
            print(f"Error técnico en el caso de prueba: {exc}")