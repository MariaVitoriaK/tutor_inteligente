from rag.banco_vetorial import BancoVetorial

class AgenteRecuperador:

    def __init__(self):

        self.nome = "Recuperador"

        self.banco = BancoVetorial()

    def recuperar(self, pergunta):

        try:
            contexto = self.banco.buscar(
                pergunta
            )
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro ao buscar no banco vetorial: {exc}")
            contexto = []

        if not contexto:
            return ""

        return "\n".join(contexto)