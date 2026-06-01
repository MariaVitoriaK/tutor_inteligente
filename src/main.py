# src/main.py
import sys
import os

# Garante que o Python consegue encontrar o módulo de agentes corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentes import AgenteRecuperador, AgenteProfessor

def iniciar_tutor():
    print("==================================================")
    print("🤖 SISTEMA MULTIAGENTE: TUTOR INTELIGENTE DE IA 🤖")
    print("==================================================")
    print("A iniciar os subsistemas locais...")
    
    try:
        # Passo 7: Inicialização dos Agentes e da Base de Dados Vetorial
        recuperador = AgenteRecuperador()
        professor = AgenteProfessor()
    except Exception as e:
        print(f"\n❌ Erro crítico ao iniciar os agentes: {e}")
        print("Verifica se o arquivo 'data/aula1.txt' existe e se o Ollama está ativo.")
        return

    print("\n✅ Todos os agentes estão online e prontos!")
    print(f"-> {recuperador.nome}: Responsável pelo RAG (Busca Semântica).")
    print(f"-> {professor.nome}: Responsável pela Explicação Didática (LLM Local).")
    print("==================================================")

    # Passo 8: Loop da Interface de Terminal (CLI)
    while True:
        duvida = input("\n👨‍🎓 Coloca a tua dúvida sobre Python (ou digita 'sair' para encerrar): ")
        
        if duvida.lower() == 'sair':
            print("\nA encerrar o Tutor Inteligente. Bons estudos!")
            break
            
        if not duvida.strip():
            print("Por favor, digita uma dúvida válida.")
            continue

        print("\n" + "="*40)
        print("🧠 FLUXO DE COOPERAÇÃO DOS AGENTES COORDENADOS:")
        print("="*40)

        # 1. O Agente Recuperador executa a sua função (Simulando o uso de ferramenta/MCP)
        contexto_recuperado = recuperador.buscar_contexto(duvida)
        print(f"💡 [Contexto Obtido]: {contexto_recuperado[:100]}...") # Mostra um resumo do que encontrou

        # 2. O Agente Professor recebe o contexto e formula a resposta final
        resposta_final = professor.responder_ao_aluno(duvida, contexto_recuperado)
        
        # 3. Exibe a resposta final no ecrã para o utilizador
        print(resposta_final)
        print("="*40)

if __name__ == "__main__":
    iniciar_tutor()