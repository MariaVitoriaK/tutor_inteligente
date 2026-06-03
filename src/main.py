# src/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agentes import AgenteRecuperador, AgenteProfessor, AgenteAvaliador

def iniciar_tutor():
    print("==================================================")
    print("🤖 SISTEMA MULTIAGENTE: TUTOR INTELIGENTE COM MEMÓRIA 🤖")
    print("==================================================")
    
    try:
        recuperador = AgenteRecuperador()
        professor = AgenteProfessor()
        avaliador = AgenteAvaliador()
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        return

    # 🎛️ CONTROLE DE ESTADO DA CONVERSA
    modo_quiz = False
    contexto_salvo_para_o_quiz = ""
    pergunta_salva_para_o_quiz = "" 

    print("\n✅ Sistema pronto e corrigido!")
    print("-> Digite suas dúvidas normalmente.")
    print("-> Peça um 'teste' para iniciar um quiz.")
    print("==================================================")

    while True:
        entrada = input("\n👨‍🎓 Tu: ")
        
        if entrada.lower() == 'sair':
            print("A encerrar o Tutor. Bons estudos!")
            break
            
        if not entrada.strip():
            continue

        print("\n" + "="*50)
        print("🧠 FLUXO DE COOPERAÇÃO DOS AGENTES:")
        print("="*50)

        # CASO 1: O aluno está respondendo ao quiz
        if modo_quiz:
            resposta_final = avaliador.validar_resposta(entrada, contexto_salvo_para_o_quiz, pergunta_salva_para_o_quiz)
            print(resposta_final)
            
            modo_quiz = False
            contexto_salvo_para_o_quiz = ""
            pergunta_salva_para_o_quiz = ""
            
        # CASO 2: Fluxo normal
        else:
            contexto_recuperado = recuperador.buscar_contexto(entrada)
            
            if "teste" in entrada.lower() or "exercício" in entrada.lower():
                # 🛠️ LINHA CORRIGIDA AQUI: Mudado de 'generar_exercicio' para 'gerar_exercicio'
                resposta_final = avaliador.gerar_exercicio(entrada, contexto_recuperado)
                print(resposta_final)
                
                modo_quiz = True
                contexto_salvo_para_o_quiz = contexto_recuperado
                pergunta_salva_para_o_quiz = resposta_final 
            
            else:
                resposta_final = professor.responder_ao_aluno(entrada, contexto_recuperado)
                print(resposta_final)
                
        print("="*50)

if __name__ == "__main__":
    iniciar_tutor()