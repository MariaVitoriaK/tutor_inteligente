tool_busca_material = {
    "type": "function",
    "function": {
        "name": "buscar_material",
        "description": (
            "Busca informações didáticas "
            "na base de conhecimento Python"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pergunta": {
                    "type": "string",
                    "description":
                    "Pergunta do aluno"
                }
            },
            "required": ["pergunta"]
        }
    }
}