from src.rag.rag import RAG

class AgenteRecuperador:

    def __init__(self):
        self.nome = "Recuperador"
        self.rag = RAG()

    def recuperar(self, pergunta):
        try:
            contexto = self.rag.recuperar_contexto(pergunta)
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro ao recuperar contexto: {exc}")
            return ""

        return contexto