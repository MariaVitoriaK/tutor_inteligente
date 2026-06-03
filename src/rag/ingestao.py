import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

from banco_vetorial import BancoVetorial


def carregar_documentos():

    documentos = []

    BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )

    pasta = os.path.join(
        BASE_DIR,
        "data"
    )
    
    print("Lendo arquivos de:", pasta)

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

if __name__ == "__main__":
    carregar_documentos()