# src/agentes.py
import os
import chromadb
import ollama

class AgenteRecuperador:
    def __init__(self):
        self.nome = "Agente Recuperador"
        # Cria ou conecta ao banco vetorial na pasta raiz do projeto
        self.cliente_bd = chromadb.PersistentClient(path="./bd_vetorial")
        self.colecao = self.cliente_bd.get_or_create_collection(name="aulas_python")
        
        # Carrega o conhecimento tratando erros de caminhos
        self._carregar_conhecimento()

    def _carregar_conhecimento(self):
        """Descobre o caminho correto do arquivo de texto e o lê com segurança"""
        # Descobre onde o arquivo agentes.py está e localiza a pasta 'data' de forma segura
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_arquivo = os.path.join(diretorio_atual, "..", "data", "aula1.txt")
        
        if not os.path.exists(caminho_arquivo):
            print(f"❌ [{self.nome}]: Erro! O arquivo não foi encontrado em: {caminho_arquivo}")
            return

        with open(caminho_arquivo, "r", encoding="utf-8") as ficheiro:
            # Lê as linhas e ignora linhas que estejam totalmente em branco
            linhas = [linha.strip() for linha in ficheiro.readlines() if linha.strip()]
        
        # PROTEÇÃO: Se o arquivo estiver vazio, avisa o usuário em vez de quebrar o ChromaDB
        if not linhas:
            print(f"⚠️ [{self.nome}]: Atenção! O arquivo 'aula1.txt' está vazio. Insira conteúdo nele.")
            return

        # Se houver texto, gera os IDs e salva no banco vetorial
        ids = [str(i) for i in range(len(linhas))]
        self.colecao.add(documents=linhas, ids=ids)
        print(f"📚 [{self.nome}]: Base de conhecimento carregada com sucesso! ({len(linhas)} linhas indexadas)")

    def buscar_contexto(self, duvida_aluno):
        print(f"\n🚀 [{self.nome}]: A realizar busca semântica na base vetorial...")
        
        # Faz a busca inteligente por significado
        resultados = self.colecao.query(
            query_texts=[duvida_aluno],
            n_results=1
        )
        
        # Se a IA encontrou algo, retorna o texto. Se não, retorna um aviso.
        if resultados and resultados['documents'] and resultados['documents'][0]:
            return resultados['documents'][0][0]
        return "Nenhum contexto específico encontrado na base de dados."


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