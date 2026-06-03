# src/main.py
# src/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agentes import AgenteRecuperador, AgenteProfessor, AgenteAvaliador

def iniciar_tutor():
    print("==================================================")
    print("🤖 SISTEMA MULTIAGENTE: TUTOR INTELIGENTE DE IA 🤖")
    print("==================================================")
    
    try:
        recuperador = AgenteRecuperador()
        professor = AgenteProfessor()
        avaliador = AgenteAvaliador() # Instanciamos o nosso novo agente!
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        return

    print("\n✅ Agentes operacionais!")
    print("-> Dica: Se quiseres ser testado, usa a palavra 'teste' ou 'exercício' na tua frase.\n")

    while True:
        entrada = input("\n👨‍🎓 Digita a tua dúvida (ou pede um 'teste sobre X') | 'sair' para fechar: ")
        
        if entrada.lower() == 'sair':
            print("A encerrar o Tutor Inteligente. Bons estudos!")
            break
            
        if not entrada.strip():
            continue

        print("\n" + "="*50)
        
        # 1. Recuperador procura sempre a informação na base de dados expandida
        contexto_recuperado = recuperador.buscar_contexto(entrada)
        
        # ROTEAMENTO DE TAREFAS (A magia acontece aqui)
        # Verificamos se o utilizador quer ser testado
        if "teste" in entrada.lower() or "exercício" in entrada.lower():
            # Acionamos a nova ferramenta: O Agente Avaliador
            resposta_final = avaliador.gerar_exercicio(entrada, contexto_recuperado)
        else:
            # Acionamos o fluxo normal: O Agente Professor
            resposta_final = professor.responder_ao_aluno(entrada, contexto_recuperado)
        
        print(resposta_final)
        print("="*50)

if __name__ == "__main__":
    iniciar_tutor()