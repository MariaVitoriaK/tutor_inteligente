import rag.banco_vetorial as bv
from agentes.recuperador import AgenteRecuperador


def test_recuperador_retorna_contexto(monkeypatch):
    monkeypatch.setattr(bv.BancoVetorial, 'buscar', lambda self, q: [' trecho1 ', 'trecho2'])

    r = AgenteRecuperador()
    resultado = r.recuperar('qualquer pergunta')

    assert 'trecho1' in resultado or 'trecho2' in resultado
