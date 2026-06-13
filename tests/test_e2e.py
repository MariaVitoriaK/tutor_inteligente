import builtins
import sys
import ollama
import src.rag.banco_vetorial as bv

from importlib import reload


def test_e2e_fluxo_duvida(monkeypatch, capsys):
    # Mock modelo para sempre retornar uma resposta simples (sem tool_calls)
    monkeypatch.setattr(ollama, 'chat', lambda **k: {"message": {"content": "Resposta do professor"}})
    # Mock banco vetorial para evitar acessos reais
    monkeypatch.setattr(bv.BancoVetorial, 'buscar', lambda self, q: ['conteudo didatico'])

    # Simula duas entradas: uma pergunta e o comando 'sair'
    inputs = iter(['O que é if em Python?', 'sair'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))

    # Importa e executa main
    import src.main as mainmod
    reload(mainmod)
    mainmod.main()

    captured = capsys.readouterr()
    assert 'RESPOSTA FINAL' in captured.out
    assert 'Resposta do professor' in captured.out
