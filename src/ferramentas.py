# src/ferramentas.py

def ferramenta_busca_base_dados(duvida_aluno):
    """
    Esta é a ferramenta (Tool) que será acionada pelo sistema.
    Ela encapsula a nossa busca vetorial, seguindo os princípios de divisão
    de responsabilidades que o MCP sugere.
    """
    # Na prática, isto iria comunicar com o teu ChromaDB (como fizemos no Passo 5)
    # Por agora, importamos o agente para executar a função
    from agentes import AgenteRecuperador
    recuperador = AgenteRecuperador()
    return recuperador.buscar_contexto(duvida_aluno)

# Estrutura JSON (Schema) - É assim que explicamos ao LLM (e ao MCP) o que a ferramenta faz
esquema_da_ferramenta = {
    "type": "function",
    "function": {
        "name": "ferramenta_busca_base_dados",
        "description": "Recupera informações didáticas e contexto da base de dados de aulas de Python.",
        "parameters": {
            "type": "object",
            "properties": {
                "duvida_aluno": {
                    "type": "string",
                    "description": "A pergunta que o aluno fez, otimizada para busca semântica."
                }
            },
            "required": ["duvida_aluno"]
        }
    }
}