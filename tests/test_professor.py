import builtins
import types

import ollama
import mcp.tools as tools

from agentes.professor import AgenteProfessor


def test_professor_usa_tool_e_responde(monkeypatch):
    # Simula primeira chamada do modelo que solicita tool
    def fake_chat_first(model, messages, tools=None):
        return {
            "message": {
                "tool_calls": [
                    {
                        "function": {"arguments": {"pergunta": "listas em python"}}
                    }
                ],
                "content": ""
            }
        }

    # Simula segunda chamada do modelo retornando resposta final
    def fake_chat_second(model, messages, tools=None):
        return {"message": {"content": "Resposta baseada no contexto"}}

    # contador simples para alternar entre as duas respostas
    calls = {"n": 0}

    def fake_chat(*a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            return fake_chat_first(*a, **k)
        return fake_chat_second(*a, **k)

    monkeypatch.setattr(ollama, 'chat', fake_chat)
    monkeypatch.setattr(tools, 'buscar_material', lambda pergunta: "CONTEXT: exemplo de listas")

    prof = AgenteProfessor()
    resposta = prof.responder('Explique listas')

    assert 'Resposta baseada no contexto' in resposta
