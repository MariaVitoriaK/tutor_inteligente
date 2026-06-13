from src.agentes.planejador import AgentePlanejador


def test_decidir_fluxo_avaliacao():
    p = AgentePlanejador()
    assert p.decidir_fluxo("Preciso de um teste sobre listas") == "AVALIACAO"


def test_decidir_fluxo_duvida():
    p = AgentePlanejador()
    assert p.decidir_fluxo("Como funciona o for em Python?") == "DUVIDA"
