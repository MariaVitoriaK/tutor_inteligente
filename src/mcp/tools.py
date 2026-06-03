def buscar_material(pergunta: str):
    from agentes.recuperador import AgenteRecuperador
    
    recuperador = AgenteRecuperador()

    return recuperador.recuperar(pergunta)