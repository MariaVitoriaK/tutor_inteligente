from src.rag.rag import RAG

class AgenteRecuperador:

    def __init__(self):
        self.nome = "Recuperador"
        try:
            self.rag = RAG()
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro ao inicializar o motor RAG: {exc}")
            self.rag = None

    def recuperar(self, pergunta):
        if not self.rag:
            print(f"⚠️ [{self.nome}] RAG indisponível. Ativando fallback textual direto.")
            return ""

        try:
            contexto = self.rag.recuperar_contexto(pergunta)
            
            # Garante que o retorno seja limpo e tratável
            if not contexto or not str(contexto).strip():
                return ""
                
            return contexto
            
        except Exception as exc:
            print(f"⚠️ [{self.nome}] Erro crítico durante a recuperação vetorial: {exc}")
            return ""