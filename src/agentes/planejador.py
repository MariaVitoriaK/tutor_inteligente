import unicodedata

class AgentePlanejador:

    def __init__(self):
        self.nome = "Planejador"

    def _normalizar_texto(self, texto):
        # Remove acentos e converte para minúsculas para evitar falhas de digitação do aluno
        texto_f_normal = unicodedata.normalize('NFD', texto)
        return "".join(ch for ch in texto_f_normal if unicodedata.category(ch) != 'Mn').lower()

    def decidir_fluxo(self, pergunta):
        texto = self._normalizar_texto(pergunta)

        # Base de palavras-chave estendida e normalizada sem acentos
        palavras_teste = [
            "teste", "quiz", "exercicio", "avaliar", 
            "prova", "questao", "simulado", "desafio"
        ]

        if any(p in texto for p in palavras_teste):
            return "AVALIACAO"

        return "DUVIDA"