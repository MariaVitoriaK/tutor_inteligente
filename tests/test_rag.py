from src.rag.rag import RAG


def test_rag_recupera_contexto(monkeypatch):
    mock_trechos = ["Trecho 1 sobre listas", "Trecho 2 sobre loops"]
    monkeypatch.setattr(
        "src.rag.banco_vetorial.BancoVetorial.buscar",
        lambda self, pergunta, top_k=3: mock_trechos
    )

    rag = RAG()
    contexto = rag.recuperar_contexto("O que é lista em Python?")

    assert "Trecho 1 sobre listas" in contexto
    assert "Trecho 2 sobre loops" in contexto
