class AgentePlanejador:

    def __init__(self):
        self.nome = "Planejador"

    def decidir_fluxo(self, pergunta):

        texto = pergunta.lower()

        palavras_teste = [
            "teste",
            "quiz",
            "exercício",
            "avaliar",
            "prova"
        ]

        if any(p in texto for p in palavras_teste):
            return "AVALIACAO"

        return "DUVIDA"