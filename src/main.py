# src/main.py
from agentes import AgenteRecuperador, AgenteProfessor

def iniciar_tutor():
    # Instanciando (criando) os nossos agentes
    recuperador = AgenteRecuperador()
    professor = AgenteProfessor()
    
    print("==================================================")
    print("🤖 Bem-vindo ao sistema de Tutor Inteligente! 🤖")
    print("==================================================")
    print(f"Agentes ativos: {recuperador.nome} e {professor.nome}\n") 

    # Loop contínuo para manter o terminal rodando (Interface via terminal) 
    while True:
        duvida = input("\n👨‍🎓 Digite sua dúvida sobre Python (ou digite 'sair' para fechar): ")
        
        if duvida.lower() == 'sair':
            print("Encerrando o sistema de tutoria. Bons estudos!")
            break
            
        # Passo A: O Agente Recuperador entra em ação primeiro 
        contexto_do_material = recuperador.buscar_contexto(duvida)
        
        # Passo B: O Agente Professor recebe o que o recuperador achou e responde o aluno
        resposta_final = professor.responder_ao_aluno(duvida, contexto_do_material)
        
        # Mostra o resultado final na tela
        print(resposta_final)
        print("-" * 50)

if __name__ == "__main__":
    iniciar_tutor()