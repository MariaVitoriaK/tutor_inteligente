# src/agentes.py

import os
import chromadb
import ollama

class AgenteRecuperador:
    def __init__(self):
        self.nome = "Agente Recuperador"
        self.cliente_bd = chromadb.PersistentClient(path="./bd_vetorial")
        
        # Apagamos a coleção antiga ao iniciar para não duplicar dados sempre que o código corre
        try:
            self.cliente_bd.delete_collection(name="aulas_python")
        except:
            pass
            
        self.colecao = self.cliente_bd.get_or_create_collection(name="aulas_python")
        self._carregar_conhecimento()

    def _carregar_conhecimento(self):
        """Lê TODOS os ficheiros .txt dentro da pasta data"""
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_data = os.path.join(diretorio_atual, "..", "data")
        
        if not os.path.exists(pasta_data):
            print(f"❌ [{self.nome}]: Pasta 'data' não encontrada.")
            return

        documentos_totais = []
        
        # Percorre todos os ficheiros na pasta
        for nome_ficheiro in os.listdir(pasta_data):
            if nome_ficheiro.endswith(".txt"):
                caminho_ficheiro = os.path.join(pasta_data, nome_ficheiro)
                with open(caminho_ficheiro, "r", encoding="utf-8") as ficheiro:
                    # Lê o texto e adiciona uma tag com o nome da aula (ajuda o modelo de IA)
                    linhas = [f"[Origem: {nome_ficheiro}] {linha.strip()}" for linha in ficheiro.readlines() if linha.strip()]
                    documentos_totais.extend(linhas)
        
        if not documentos_totais:
            print(f"⚠️ [{self.nome}]: Nenhum conteúdo encontrado nos ficheiros.")
            return

        # Guarda tudo na base de dados vetorial
        ids = [str(i) for i in range(len(documentos_totais))]
        self.colecao.add(documents=documentos_totais, ids=ids)
        print(f"📚 [{self.nome}]: Base expandida com sucesso! ({len(documentos_totais)} blocos de texto indexados das tuas aulas)")

    def buscar_contexto(self, duvida_aluno):
        print(f"🚀 [{self.nome}]: A pesquisar na base de dados vetorial...")
        resultados = self.colecao.query(query_texts=[duvida_aluno], n_results=2) # Agora trazemos os 2 melhores resultados
        
        if resultados and resultados['documents'] and resultados['documents'][0]:
            # Junta os resultados encontrados num único texto
            return " | ".join(resultados['documents'][0])
        return "Nenhum contexto específico encontrado."

class AgenteProfessor:
    def __init__(self):
        self.nome = "Agente Professor"
        self.modelo = "llama3.2"  # Certifique-se de ter dado 'ollama run llama3.2' no terminal antes

    def responder_ao_aluno(self, duvida_aluno, contexto):
        print(f"🎓 [{self.nome}]: A consultar o modelo de IA local ({self.modelo})...")
        
        prompt_sistema = "És um professor de Python simpático e didático. Responde à dúvida do aluno usando a informação do contexto fornecido."
        prompt_utilizador = f"Contexto da Aula:\n{contexto}\n\nDúvida do Aluno: {duvida_aluno}"

        try:
            resposta_ia = ollama.chat(model=self.modelo, messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': prompt_utilizador}
            ])
            return f"\n--- RESPOSTA DO TUTOR (IA) ---\n{resposta_ia['message']['content']}"
        except Exception as e:
            return f"\n❌ Erro ao chamar o Ollama: {e}. O Ollama está rodando no seu computador?"
        
    
class AgenteAvaliador:
    def __init__(self):
        self.nome = "Agente Avaliador (Ferramenta de Teste)"
        self.modelo = "llama3.2"

    def gerar_exercicio(self, tema, contexto):
        """
        Esta é a nossa nova 'ferramenta'. Em vez de explicar, ela cria um 
        desafio prático para testar os conhecimentos do utilizador.
        """
        print(f"📝 [{self.nome}]: A gerar um exercício prático sobre '{tema}'...")
        
        prompt_sistema = "És um examinador de Python. A tua função é criar UMA pergunta de escolha múltipla (com opções A, B, C) baseada estritamente no contexto fornecido. Não dês a resposta imediatamente, pede ao aluno para adivinhar."
        prompt_utilizador = f"Contexto do material de estudo:\n{contexto}\n\nTema pedido pelo aluno: {tema}"

        try:
            resposta_ia = ollama.chat(model=self.modelo, messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': prompt_utilizador}
            ])
            return f"\n--- EXERCÍCIO DE TESTE ---\n{resposta_ia['message']['content']}"
        except Exception as e:
            return f"\n❌ Erro ao gerar o teste: {e}"