import os
from pathlib import Path
from typing import List

import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter


class BancoVetorial:

    def __init__(self):
        self.root_path = Path(__file__).resolve().parents[2]
        self.db_path = self.root_path / "bd_vetorial"
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.available = True
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path)
            )

            self.collection = self.client.get_or_create_collection(
                name="documentos",
                metadata={"source": "data"}
           )
        except Exception as exc:
            # Falha ao inicializar o Chroma — desabilitar busca vetorial
            print(f"⚠️ Não foi possível inicializar o banco vetorial: {exc}")
            self.available = False
            self.client = None
            self.collection = None
    def adicionar_documentos(self, documentos: List[str], ids: List[str]):
        self.collection.add(
            ids=ids,
            documents=documentos
        )

    def buscar(self, pergunta: str, top_k: int = 3) -> List[str]:
        if not self.available:
            return self._busca_textual(pergunta, top_k)

        try:
            if self.collection.count() == 0:
                return self._busca_textual(pergunta, top_k)

            resultados = self.collection.query(
                query_texts=[pergunta],
                n_results=top_k,
                include=["documents", "distances"],
            )

            documentos = resultados.get("documents", [[]])[0]
            return [doc for doc in documentos if doc]
        except Exception as exc:
            print(f"⚠️ Erro na busca vetorial: {exc}")
            return self._busca_textual(pergunta, top_k)

    def _busca_textual(self, pergunta: str, top_k: int = 3) -> List[str]:
        documentos = self._carregar_documentos()
        palavras = {p for p in pergunta.lower().split() if len(p) > 2}

        pontuacoes = []
        for texto in documentos:
            tokens = set(texto.lower().split())
            pontos = sum(1 for palavra in palavras if palavra in tokens)
            if pontos > 0:
                pontuacoes.append((pontos, texto))

        if not pontuacoes:
            return documentos[:top_k]

        pontuacoes.sort(key=lambda item: item[0], reverse=True)
        return [texto for _, texto in pontuacoes[:top_k]]

    def _carregar_documentos(self) -> List[str]:
        pasta = self.root_path / "data"
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        documentos = []
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(".txt"):
                caminho = pasta / arquivo
                with caminho.open("r", encoding="utf-8") as f:
                    texto = f.read()
                documentos.extend(splitter.split_text(texto))

        return documentos
