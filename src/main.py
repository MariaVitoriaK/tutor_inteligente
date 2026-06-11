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
        if pergunta is None:
            continue

        pergunta = pergunta.strip()

        if pergunta.lower() == "sair":
            print("\n👋 Encerrando sistema...")
            break

        if pergunta == "":
            print("⚠️ Entrada inválida: digite uma pergunta ou 'sair' para encerrar.")
            continue

        print("\n" + "=" * 60)
        print("🧠 INICIANDO FLUXO MULTIAGENTE")
        print("=" * 60)

        try:
            decisao = planejador.decidir_fluxo(pergunta)
        except Exception as exc:
            print(f"⚠️ [Planejador] Erro ao decidir fluxo: {exc}")
            continue

        print(
            f"📋 [Planejador] Fluxo escolhido: {decisao}"
        )

        if decisao == "AVALIACAO":

            print(
                "📝 [Planejador] Encaminhando para Avaliador"
            )

            try:
                resposta = avaliador.gerar_exercicio(pergunta, "")
            except Exception as exc:
                print(f"⚠️ [Avaliador] Erro durante a geração: {exc}")
                resposta = "Desculpe — erro ao gerar exercício."

            print("\n")
            print(resposta)

        else:

            print(
                "🎓 [Planejador] Encaminhando para Professor"
            )

            try:
                resposta_professor = professor.responder(pergunta)
            except Exception as exc:
                print(f"⚠️ [Professor] Erro durante resposta: {exc}")
                resposta_professor = "Desculpe — erro interno ao responder."

            print(
                "🔎 [Revisor] Revisando resposta..."
            )

            try:
                resposta_final = revisor.revisar(resposta_professor)
            except Exception as exc:
                print(f"⚠️ [Revisor] Erro durante revisão: {exc}")
                resposta_final = resposta_professor

            print(
                "✅ [Revisor] Revisão concluída"
            )

            print("\n📚 RESPOSTA FINAL\n")
            print(resposta_final)

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()