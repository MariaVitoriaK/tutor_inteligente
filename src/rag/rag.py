from .banco_vetorial import BancoVetorial


class RAG:

    def __init__(self, top_k: int = 3):
        self.banco = BancoVetorial()
        self.top_k = top_k

    def recuperar_contexto(self, pergunta: str) -> str:
        if not pergunta:
            return ""

        trechos = self.banco.buscar(pergunta, top_k=self.top_k)
        if not trechos:
            return ""

        return "\n\n".join(trechos)
