# src/agentes.py

import chromadb

class AgenteRecuperador:
    def __init__(self):
        self.nome = "Agente Recuperador"
        # Criamos/ligamos a uma base de dados vetorial local (vai criar uma pasta nova no teu projeto)
        self.cliente_bd = chromadb.PersistentClient(path="./bd_vetorial")
        # Criamos uma "coleção" para guardar as nossas aulas
        self.colecao = self.cliente_bd.get_or_create_collection(name="aulas_python")
        
        # Vamos carregar o ficheiro de texto e guardá-lo na base de dados
        self._carregar_conhecimento()

    def _carregar_conhecimento(self):
        """Lê o ficheiro e guarda na base de dados vetorial de forma automática"""
        with open("../data/aula1.txt", "r", encoding="utf-8") as ficheiro:
            linhas = ficheiro.readlines()
        
        # Para simplificar, cada linha será um "pedaço" (chunk) de conhecimento
        ids = [str(i) for i in range(len(linhas))]
        
        # O ChromaDB converte automaticamente o texto em embeddings (números) e guarda!
        self.colecao.add(documents=linhas, ids=ids)
        print(f"📚 [{self.nome}]: Base de conhecimento carregada com sucesso!")

    def buscar_contexto(self, duvida_aluno):
        print(f"\n🚀 [{self.nome}]: A realizar busca semântica na base vetorial...")
        
        # Aqui fazemos a magia! Procuramos o texto mais semelhante à pergunta
        resultados = self.colecao.query(
            query_texts=[duvida_aluno],
            n_results=1 # Queremos apenas o 1 resultado mais relevante
        )
        
        # Extraímos o texto encontrado
        contexto_encontrado = resultados['documents'][0][0]
        return contexto_encontrado


import ollama

class AgenteProfessor:
    def __init__(self):
        self.nome = "Agente Professor"
        # Vamos usar o modelo que descarregaste
        self.modelo = "llama3.2" 

    def responder_ao_aluno(self, duvida_aluno, contexto):
        print(f"🎓 [{self.nome}]: A consultar o modelo de IA local ({self.modelo})...")
        
        # Criamos as instruções (Prompt)
        prompt_sistema = "És um professor de Python simpático e didático. Responde à dúvida do aluno usando APENAS a informação do contexto fornecido."
        prompt_utilizador = f"Contexto da Aula:\n{contexto}\n\nDúvida do Aluno: {duvida_aluno}"

        # Chamamos a Inteligência Artificial
        resposta_ia = ollama.chat(model=self.modelo, messages=[
            {'role': 'system', 'content': prompt_sistema},
            {'role': 'user', 'content': prompt_utilizador}
        ])
        
        # Retornamos o texto gerado pela IA
        return f"\n--- RESPOSTA DO TUTOR (IA) ---\n{resposta_ia['message']['content']}"