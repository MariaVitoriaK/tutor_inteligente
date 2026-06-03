import ollama

class AgenteRevisor:

    def __init__(self):

        self.modelo = "llama3.2"

    def revisar(
        self,
        resposta
    ):

        prompt = f"""
        Revise a resposta abaixo.

        Verifique:
        - clareza
        - correção
        - didática

        Resposta:

        {resposta}
        """

        resultado = ollama.chat(
            model=self.modelo,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return resultado["message"]["content"]