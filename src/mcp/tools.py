from agentes.recuperador import AgenteRecuperador

def buscar_material(
    pergunta
):

    recuperador = AgenteRecuperador()

    return recuperador.recuperar(
        pergunta
    )