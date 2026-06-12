import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração do Tutor Inteligente Multiagente."""

    # Modelo Local (Ollama)
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")
    MODEL_API_BASE = os.getenv("MODEL_API_BASE", "http://localhost:11434")

    # Embeddings locais usados pelo RAG
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ChromaDB
    CHROMA_PATH = os.getenv("CHROMA_PATH", "bd_vetorial")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documentos")

    # MCP (Model Context Protocol)
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    @classmethod
    def get_model_config(cls) -> dict:
        """Retorna configuração do modelo."""
        return {
            "model": cls.MODEL_NAME,
            "base_url": cls.MODEL_API_BASE,
        }

    @classmethod
    def get_mcp_config(cls) -> dict:
        """Retorna configuração do MCP."""
        return {
            "server_url": cls.MCP_SERVER_URL,
        }
