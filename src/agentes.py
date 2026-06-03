# src/agentes.py
import os
import chromadb
import ollama

class AgenteRecuperador:
    def __init__(self):
        self.nome = "Agente Recuperador"
        self.cliente_bd = chromadb.PersistentClient(path="./bd_vetorial")
        try:
            self.cliente_bd.delete_collection(name="aulas_python")
        except:
            pass
        self.colecao = self.cliente_bd.get_or_create_collection(name="aulas_python")
        self._carregar_conhecimento()

    def _carregar_conhecimento(self):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_data = os.path.join(diretorio_atual, "..", "data")
        
        if not os.path.exists(pasta_data):
            print(f"❌ [{self.nome}]: Pasta 'data' não encontrada.")
            return

        documentos_totais = []
        for nome_ficheiro in os.listdir(pasta_data):
            if nome_ficheiro.endswith(".txt"):
                caminho_ficheiro = os.path.join(pasta_data, nome_ficheiro)
                with open(caminho_ficheiro, "r", encoding="utf-8") as ficheiro:
                    linhas = [f"[Origem: {nome_ficheiro}] {linha.strip()}" for linha in ficheiro.readlines() if linha.strip()]
                    documentos_totais.extend(linhas)
        
        if documentos_totais:
            ids = [str(i) for i in range(len(documentos_totais))]
            self.colecao.add(documents=documentos_totais, ids=ids)
            print(f"📚 [{self.nome}]: Base de dados carregada ({len(documentos_totais)} blocos indexados).")

    def buscar_contexto(self, duvida_aluno):
        print(f"🚀 [{self.nome}]: A pesquisar na base de dados vetorial...")
        resultados = self.colecao.query(query_texts=[duvida_aluno], n_results=2)
        if resultados and resultados['documents'] and resultados['documents'][0]:
            return " | ".join(resultados['documents'][0])
        return "Nenhum contexto específico encontrado."


class AgenteProfessor:
    def __init__(self):
        self.nome = "Agente Professor"
        self.modelo = "llama3.2"
        # 🧠 NOVA PROPRIEDADE: Lista para guardar o histórico de conversas do aluno
        self.historico = []

    def responder_ao_aluno(self, duvida_aluno, contexto):
        print(f"🎓 [{self.nome}]: A consultar o modelo local com memória de chat...")
        
        # O prompt do sistema define a regra principal, alimentada pelo RAG
        prompt_sistema = f"És um professor de Python simpático. Responde às dúvidas usando este contexto das aulas:\n{contexto}"
        
        # Montamos a estrutura de mensagens contendo o histórico completo para a IA não esquecer o passado
        mensagens = [{'role': 'system', 'content': prompt_sistema}]
        mensagens.extend(self.historico) # Injeta o passado
        mensagens.append({'role': 'user', 'content': duvida_aluno}) # Injeta a dúvida atual

        try:
            resposta_ia = ollama.chat(model=self.modelo, messages=mensagens)
            conteudo_resposta = resposta_ia['message']['content']
            
            # Guardamos essa interação na memória para a próxima pergunta
            self.historico.append({'role': 'user', 'content': duvida_aluno})
            self.historico.append({'role': 'assistant', 'content': conteudo_resposta})
            
            return f"\n--- RESPOSTA DO TUTOR (IA) ---\n{conteudo_resposta}"
        except Exception as e:
            return f"\n❌ Erro no Ollama: {e}"


class AgenteAvaliador:
    def __init__(self):
        self.nome = "Agente Avaliador"
        self.modelo = "llama3.2"

    def gerar_exercicio(self, tema, contexto):
        print(f"📝 [{self.nome}]: A gerar um exercício prático sobre '{tema}'...")
        prompt_sistema = "És um examinador de Python. Cria UMA pergunta de escolha múltipla (A, B, C, D) baseada no contexto fornecido. Não dês a resposta, pede ao aluno para responder."
        prompt_utilizador = f"Contexto:\n{contexto}\n\nPedido do aluno: {tema}"

        try:
            resposta_ia = ollama.chat(model=self.modelo, messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': prompt_utilizador}
            ])
            return f"\n--- EXERCÍCIO DE TESTE ---\n{resposta_ia['message']['content']}"
        except Exception as e:
            return f"\n❌ Erro ao gerar teste: {e}"

    # 🎯 ATUALIZADO: Agora recebe também a 'pergunta_feita'
    def validar_resposta(self, resposta_aluno, contexto_aula, pergunta_feita):
        print(f"⚖️ [{self.nome}]: A corrigir a tua resposta...")
        
        # Criamos um prompt com regras lógicas estritas e passos sequenciais
        prompt_sistema = (
            "És um sistema automático de correção de testes de Python 100% exato e imparcial.\n"
            "Para avaliares o aluno, deves seguir OBRIGATORIAMENTE estes passos mentalmente antes de responder:\n"
            "1. Analisa a pergunta que foi feita e determina qual é a ÚNICA letra/opção correta com base no material da aula.\n"
            "2. Identifica qual foi a letra/opção que o aluno escolheu.\n"
            "3. Compara as duas:\n"
            "   - Se a escolha do aluno for IGUAL à opção correta, começa a tua resposta OBRIGATORIAMENTE com: '**PARABÉNS, ACERTOU!**'\n"
            "   - Se a escolha do aluno for DIFERENTE da opção correta, começa a tua resposta OBRIGATORIAMENTE com: '**INFELIZMENTE, ERROU.**'\n"
            "4. Logo a seguir, apresenta a justificativa didática de forma clara."
        )
        
        prompt_utilizador = (
            f"--- CONTEXTO DO MATERIAL DIDÁTICO ---\n{contexto_aula}\n\n"
            f"--- PERGUNTA DE ESCOLA MÚLTIPLA GERADA ---\n{pergunta_feita}\n\n"
            f"--- RESPOSTA FORNECIDA PELO ALUNO ---\n{resposta_aluno}"
        )

        try:
            resposta_ia = ollama.chat(model=self.modelo, messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': prompt_utilizador}
            ])
            return f"\n--- CORREÇÃO DO TESTE ---\n{resposta_ia['message']['content']}"
        except Exception as e:
            return f"\n❌ Erro ao corrigir teste: {e}"