from agentes.planejador import AgentePlanejador
from agentes.recuperador import AgenteRecuperador
from agentes.professor import AgenteProfessor
from agentes.avaliador import AgenteAvaliador
from agentes.revisor import AgenteRevisor

def main():

    planejador = AgentePlanejador()

    recuperador = AgenteRecuperador()

    professor = AgenteProfessor()

    avaliador = AgenteAvaliador()

    revisor = AgenteRevisor()

    while True:

        pergunta = input(
            "\nAluno: "
        )

        if pergunta.lower() == "sair":
            break

        decisao = (
            planejador.decidir_fluxo(
                pergunta
            )
        )

        if decisao == "AVALIACAO":

            contexto = (
                recuperador.recuperar(
                    pergunta
                )
            )

            resposta = (
                avaliador.gerar_exercicio(
                    pergunta,
                    contexto
                )
            )

            print(
                "\n[Avaliador]\n",
                resposta
            )

        else:

            contexto = (
                recuperador.recuperar(
                    pergunta
                )
            )

            resposta = (
                professor.responder(
                    pergunta,
                    contexto
                )
            )

            resposta_final = (
                revisor.revisar(
                    resposta
                )
            )

            print(
                "\n[Tutor]\n",
                resposta_final
            )

if __name__ == "__main__":
    main()