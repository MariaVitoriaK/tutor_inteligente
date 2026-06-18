import ollama

from src.config.config import Config

class AgenteRevisor:

    def __init__(self):
        self.modelo = Config.MODEL_NAME

    def revisar(self, resposta):
        print("🔎 [Revisor] Revisando resposta...")
        
        try:
            resultado = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um revisor de textos técnicos focado em computação e na linguagem Python.\n\n"
                            "SUA MISSÃO:\n"
                            "Avaliar a resposta fornecida quanto à correção gramatical, clareza e exatidão técnica "
                            "(garantindo que estruturas mutáveis como listas NÃO sejam chamadas de imutáveis).\n\n"
                            "REGRAS DE RETORNO (OBRIGATÓRIO):\n"
                            "- Corrija erros gramaticais gritantes ou problemas conceituais se houver.\n"
                            "- NÃO adicione saudações, introduções ou explicações (ex: Não diga 'Aqui está a correção').\n"
                            "- NÃO acrescente conteúdos, novos tópicos ou exemplos de código que não estavam no original.\n"
                            "- Se o texto original estiver correto e claro, retorne exatamente o mesmo texto recebido, caractere por caractere."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Texto a ser revisado:\n---\n{resposta}\n---"
                    }
                ]
            )

            return resultado["message"]["content"]
        except Exception as exc:
            print(f"⚠️ [Revisor] Erro ao acessar o modelo: {exc}")
            # Mantém o princípio de robustez retornando a resposta original como fallback 
            return resposta