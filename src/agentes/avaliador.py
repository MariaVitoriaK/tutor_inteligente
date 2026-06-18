import ollama

from src.config.config import Config
from src.agentes.recuperador import AgenteRecuperador


class AgenteAvaliador:

    def __init__(self):
        self.nome = "Avaliador"
        self.modelo = Config.MODEL_NAME

    def gerar_exercicio(self, tema, contexto):
        if not contexto:
            try:
                contexto = AgenteRecuperador().recuperar(tema)
            except Exception as exc:
                print(f"⚠️ [{self.nome}] Erro ao recuperar contexto: {exc}")
                contexto = ""

        if not contexto:
            contexto = (
                "Não foi possível recuperar o material didático oficial. "
                "Gere uma questão padrão sobre a sintaxe correta do tema solicitado."
            )

        print(f"[{self.nome}] Gerando exercício...")

        try:
            resposta = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um professor de Python encarregado de criar testes de múltipla escolha.\n\n"
                            "[REGRAS OBRIGATÓRIAS]:\n"
                            "1. Crie apenas UMA questão com exatamente 4 alternativas (A, B, C, D).\n"
                            "2. Garanta precisão técnica absoluta em Python (Lembre-se: listas/dicionários são mutáveis; tuplas/strings são imutáveis).\n"
                            "3. NÃO forneça a resposta correta e NÃO explique a resolução no texto gerado.\n"
                            "4. Termine o texto da questão estritamente com a frase: 'Digite apenas a letra da resposta.'"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"[CONTEXTO DIDÁTICO]:\n{contexto}\n\n[TEMA]: {tema}"
                    }
                ]
            )

            return resposta["message"]["content"]
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro ao gerar exercício: {exc}")
            return "Desculpe — não foi possível gerar o exercício no momento."

    def corrigir_resposta(self, pergunta, resposta_aluno, contexto):
        print(f"[{self.nome}] Corrigindo resposta...")

        try:
            resposta = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um corretor rigoroso de provas de programação Python.\n\n"
                            "[INSTRUÇÕES DE CORREÇÃO]:\n"
                            "1. Analise a QUESTÃO e determine qual é a única alternativa correta baseando-se no CONTEXTO.\n"
                            "2. Compare com a RESPOSTA DO ALUNO.\n"
                            "3. Se o aluno acertou, inicie sua resposta OBRIGATORIAMENTE com: '✅ PARABÉNS, VOCÊ ACERTOU!'\n"
                            "4. Se o aluno errou, inicie sua resposta OBRIGATORIAMENTE com: '❌ INFELIZMENTE, VOCÊ ERROU.'\n"
                            "5. Na sequência, explique de forma clara o motivo da resposta correta e corrija eventuais equívocos conceituais."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"[CONTEXTO DA MATÉRIA]:\n{contexto}\n\n"
                            f"[QUESTÃO AVALIADA]:\n{pergunta}\n\n"
                            f"[RESPOSTA DO ALUNO]:\n{resposta_aluno}"
                        )
                    }
                ]
            )

            return resposta["message"]["content"]
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro ao corrigir resposta: {exc}")
            return "Desculpe — não foi possível validar sua resposta no momento."