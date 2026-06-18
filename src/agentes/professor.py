import ollama

from src.config.config import Config
from src.mcp.tools import buscar_material
from src.mcp.esquemas import tool_busca_material


class AgenteProfessor:

    def __init__(self):
        self.modelo = Config.MODEL_NAME

    def responder(self, pergunta):

        print("\n🎓 [Professor] Analisando pergunta...")
        try:
            primeira_resposta = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um professor universitário assistente e especialista na linguagem Python.\n\n"
                            "DIRETRIZES DE ATUAÇÃO:\n"
                            "1. Sempre que a dúvida do aluno envolver conceitos teóricos, sintaxe ou conteúdos "
                            "das aulas, use obrigatoriamente a ferramenta 'buscar_material'.\n"
                            "2. Só responda diretamente se for uma interação informal (ex: 'olá', 'tudo bem?') "
                            "ou se a pergunta não tiver relação com tópicos de programação."
                        )
                    },
                    {
                        "role": "user",
                        "content": pergunta
                    }
                ],
                tools=[tool_busca_material]
            )
        except Exception as exc:
            print(f"⚠️ [Professor] Erro acessando o modelo local: {exc}")
            return "Desculpe — não foi possível acessar o modelo local no momento."

        mensagem = primeira_resposta["message"]

        if mensagem.get("tool_calls"):

            print("🛠️ [Professor] Decidiu usar uma Tool")
            tool_call = mensagem["tool_calls"][0]
            argumentos = tool_call["function"]["arguments"]

            print(f"🔍 [Professor] Buscando contexto para: {argumentos['pergunta']}")

            try:
                contexto = buscar_material(argumentos["pergunta"])
            except Exception as exc:
                print(f"⚠️ [Professor] Erro ao recuperar contexto: {exc}")
                contexto = ""

            print("📚 [Professor] Contexto recuperado")

            try:
                resposta_final = ollama.chat(
                    model=self.modelo,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é um professor especialista em Python focado em precisão técnica e didática.\n\n"
                                "[REGRAS CRÍTICAS DE RESPOSTA]:\n"
                                "1. Baseie sua resposta EXCLUSIVAMENTE nas informações fornecidas no [CONTEXTO] abaixo.\n"
                                "2. Jamais invente fatos ou inverta conceitos. Lembre-se: em Python, listas e dicionários "
                                "são MUTÁVEIS; tuplas e strings são IMUTÁVEIS.\n"
                                "3. Se o [CONTEXTO] fornecido estiver em branco ou não contiver dados suficientes para responder "
                                "à pergunta do aluno de forma completa, responda exatamente e apenas com a frase:\n"
                                "'Não encontrei essa informação na base de conhecimento.'\n\n"
                                f"[CONTEXTO]:\n{contexto}"
                            )
                        },
                        {
                            "role": "user",
                            "content": pergunta
                        }
                    ]
                )
            except Exception as exc:
                print(f"⚠️ [Professor] Erro ao gerar resposta: {exc}")
                return "Desculpe — erro ao gerar resposta baseada no contexto."

            print("✅ [Professor] Resposta gerada")
            return resposta_final["message"]["content"]

        print("💡 [Professor] Não precisou usar Tool")
        return mensagem["content"]