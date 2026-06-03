import ollama

from agentes.recuperador import AgenteRecuperador


class AgenteAvaliador:

    def __init__(self):
        self.nome = "Avaliador"
        self.modelo = "llama3.2"

    def gerar_exercicio(self, tema, contexto):
        if not contexto:
            contexto = AgenteRecuperador().recuperar(tema)

        if not contexto:
            contexto = (
                "Não foi possível recuperar o material didático. "
                "Gere a questão com base no tema informado."
            )

        print(f"[{self.nome}] Gerando exercício...")

        prompt = f"""
Você é um professor de Python.

Com base no contexto abaixo, crie UMA questão de múltipla escolha.

REGRAS:
- 4 alternativas (A, B, C, D)
- Apenas UMA correta
- Não informe a resposta correta
- No final escreva:
  "Digite apenas a letra da resposta."

CONTEXTO:
{contexto}

TEMA SOLICITADO:
{tema}
"""

        resposta = ollama.chat(
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return resposta["message"]["content"]

    def corrigir_resposta(
        self,
        pergunta,
        resposta_aluno,
        contexto
    ):

        print(f"[{self.nome}] Corrigindo resposta...")

        prompt = f"""
Você é um corretor de provas de Python.

CONTEXTO:
{contexto}

QUESTÃO:
{pergunta}

RESPOSTA DO ALUNO:
{resposta_aluno}

TAREFA:

1. Descubra qual é a alternativa correta.
2. Compare com a resposta do aluno.

Se estiver correta:

✅ PARABÉNS, VOCÊ ACERTOU!

Se estiver incorreta:

❌ INFELIZMENTE, VOCÊ ERROU.

Depois explique o motivo da correção.

Informe também qual era a resposta correta.
"""

        resposta = ollama.chat(
            model=self.modelo,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return resposta["message"]["content"]