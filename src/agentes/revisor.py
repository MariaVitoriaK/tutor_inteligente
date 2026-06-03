import ollama

class AgenteRevisor:

    def __init__(self):

        self.modelo = "llama3.2"

    def revisar(
        self,
        resposta
    ):

        prompt = f"""
        Verifique apenas:
        
        - clareza
        - gramática
        
        NÃO reescreva.
        NÃO acrescente conteúdo.
        NÃO altere conceitos.
        
        Resposta:
        
        {resposta}
        
        Retorne exatamente a mesma resposta
        caso esteja correta.
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