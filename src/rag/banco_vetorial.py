import chromadb

class BancoVetorial:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./bd_vetorial"
        )

        self.collection = self.client.get_or_create_collection(
            name="python_aulas"
        )

    def adicionar_documentos(self, documentos, ids):

        self.collection.add(
            documents=documentos,
            ids=ids
        )

    def buscar(self, pergunta):

        resultado = self.collection.query(
            query_texts=[pergunta],
            n_results=3
        )

        if resultado["documents"]:
            return resultado["documents"][0]

        return []