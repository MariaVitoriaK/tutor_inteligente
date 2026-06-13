import ollama
from src.agentes.revisor import AgenteRevisor


def test_revisor_retorna_mesma_resposta(monkeypatch):
    monkeypatch.setattr(ollama, 'chat', lambda **k: {"message": {"content": "Resposta sem erros"}})

    r = AgenteRevisor()
    out = r.revisar('Resposta sem erros')

    assert 'Resposta sem erros' in out
