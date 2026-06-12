import ollama

from config import Config
from mcp.tools import buscar_material
from mcp.esquemas import tool_busca_material


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
                        "content": """
                    Você é um professor especialista em Python.

                    Sempre que precisar consultar
                    materiais das aulas,
                    utilize a ferramenta
                    buscar_material.

                    Se já souber responder,
                    responda diretamente.
                    """
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
            return (
                "Desculpe — não foi possível acessar o modelo local no momento."
            )

        mensagem = primeira_resposta["message"]

        if mensagem.get("tool_calls"):

            print("🛠️ [Professor] Decidiu usar uma Tool")

            tool_call = mensagem["tool_calls"][0]

            argumentos = tool_call["function"]["arguments"]

            print(
                f"🔍 [Professor] Buscando contexto para: "
                f"{argumentos['pergunta']}"
            )

            try:
                contexto = buscar_material(
                    argumentos["pergunta"]
                )
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
                            "content": f"""
                        Você é um professor de Python.
                        
                        Responda SOMENTE usando o contexto fornecido.
                        
                        Se a resposta não estiver no contexto,
                        diga:
                        
                        "Não encontrei essa informação
                        na base de conhecimento."
                        
                        CONTEXTO:
                        
                        {contexto}
                        """
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