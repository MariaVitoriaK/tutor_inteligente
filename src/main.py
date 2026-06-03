from agentes.planejador import AgentePlanejador
from agentes.professor import AgenteProfessor
from agentes.avaliador import AgenteAvaliador
from agentes.revisor import AgenteRevisor


def main():

    print("=" * 60)
    print("🤖 TUTOR INTELIGENTE MULTIAGENTE")
    print("=" * 60)

    planejador = AgentePlanejador()
    professor = AgenteProfessor()
    avaliador = AgenteAvaliador()
    revisor = AgenteRevisor()

    while True:

        pergunta = input("\n👨‍🎓 Aluno: ")

        if pergunta.lower() == "sair":
            print("\n👋 Encerrando sistema...")
            break

        print("\n" + "=" * 60)
        print("🧠 INICIANDO FLUXO MULTIAGENTE")
        print("=" * 60)

        decisao = planejador.decidir_fluxo(
            pergunta
        )

        print(
            f"📋 [Planejador] Fluxo escolhido: {decisao}"
        )

        if decisao == "AVALIACAO":

            print(
                "📝 [Planejador] Encaminhando para Avaliador"
            )

            resposta = avaliador.gerar_exercicio(
                pergunta,
                ""
            )

            print("\n")
            print(resposta)

        else:

            print(
                "🎓 [Planejador] Encaminhando para Professor"
            )

            resposta_professor = (
                professor.responder(
                    pergunta
                )
            )

            print(
                "🔎 [Revisor] Revisando resposta..."
            )

            resposta_final = (
                revisor.revisar(
                    resposta_professor
                )
            )

            print(
                "✅ [Revisor] Revisão concluída"
            )

            print("\n📚 RESPOSTA FINAL\n")
            print(resposta_final)

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()