import os
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from banco_vetorial import BancoVetorial
except ImportError:
    from rag.banco_vetorial import BancoVetorial


def carregar_documentos():

    documentos = []

    BASE_DIR = Path(__file__).resolve().parents[2]
    pasta = BASE_DIR / "data"

    print("Lendo arquivos de:", pasta)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".txt"):
            caminho = pasta / arquivo
            with open(caminho, encoding="utf-8") as f:
                texto = f.read()
            documentos.extend(splitter.split_text(texto))

    banco = BancoVetorial()

    if not banco.available:
        print("⚠️ O banco vetorial não está disponível; não é possível criar a base." )
        return

    if banco.collection.count() == 0:
        ids = [str(i) for i in range(len(documentos))]
        banco.adicionar_documentos(documentos, ids)
        print("Base vetorial criada.")
    else:
        print("Base vetorial já existe e não precisa ser recriada.")

if __name__ == "__main__":
    carregar_documentos()