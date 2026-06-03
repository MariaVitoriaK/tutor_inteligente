import json
import os
import ollama

class AgenteProfessor:

    def __init__(self):

        self.modelo = "llama3.2"

        self.arquivo_memoria = (
            "memoria/historico.json"
        )

        self.historico = self.carregar()

    def carregar(self):

        if os.path.exists(
            self.arquivo_memoria
        ):

            with open(
                self.arquivo_memoria,
                encoding="utf-8"
            ) as f:

                return json.load(f)

        return []

    def salvar(self):

        with open(
            self.arquivo_memoria,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.historico,
                f,
                ensure_ascii=False,
                indent=4
            )

    def responder(
        self,
        pergunta,
        contexto
    ):

        mensagens = [
            {
                "role": "system",
                "content":
                f"""
                Você é professor de Python.

                Use somente este contexto:

                {contexto}
                """
            }
        ]

        mensagens.extend(
            self.historico[-10:]
        )

        mensagens.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        resposta = ollama.chat(
            model=self.modelo,
            messages=mensagens
        )

        texto = resposta["message"]["content"]

        self.historico.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        self.historico.append(
            {
                "role": "assistant",
                "content": texto
            }
        )

        self.salvar()

        return texto