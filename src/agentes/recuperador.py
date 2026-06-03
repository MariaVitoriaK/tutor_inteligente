from rag.banco_vetorial import BancoVetorial

class AgenteRecuperador:

    def __init__(self):

        self.nome = "Recuperador"

        self.banco = BancoVetorial()

    def recuperar(self, pergunta):

        contexto = self.banco.buscar(
            pergunta
        )

        return "\n".join(contexto)