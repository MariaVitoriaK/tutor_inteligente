import os

from langchain.text_splitter import RecursiveCharacterTextSplitter

from banco_vetorial import BancoVetorial


def carregar_documentos():

    documentos = []

    pasta = "../data"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    for arquivo in os.listdir(pasta):

        if arquivo.endswith(".txt"):

            caminho = os.path.join(
                pasta,
                arquivo
            )

            with open(
                caminho,
                encoding="utf-8"
            ) as f:

                texto = f.read()

            chunks = splitter.split_text(texto)

            documentos.extend(chunks)

    banco = BancoVetorial()

    if banco.collection.count() == 0:

        ids = [str(i) for i in range(len(documentos))]

        banco.adicionar_documentos(
            documentos,
            ids
        )

        print("Base vetorial criada.")