import ollama
from src.agentes.avaliador import AgenteAvaliador
from src.agentes.recuperador import AgenteRecuperador


def test_gerar_exercicio_com_recuperacao(monkeypatch):
    # Quando contexto ausente, AgenteAvaliador chama AgenteRecuperador
    monkeypatch.setattr(AgenteRecuperador, 'recuperar', lambda self, t: 'contexto de teste')
    monkeypatch.setattr(ollama, 'chat', lambda **k: {"message": {"content": "QUESTÃO GERADA"}})

    a = AgenteAvaliador()
    out = a.gerar_exercicio('listas', '')

    assert 'QUESTÃO GERADA' in out
