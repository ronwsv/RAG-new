"""Embeddings Manager - Wrapper para geração de embeddings."""

import os
from typing import List, Optional

import toml
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings


class EmbeddingsManager:
    """Gerencia a geração de embeddings para documentos e queries."""

    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Inicializa o gerenciador de embeddings.

        Args:
            provider: Provedor de embeddings ("openai", "ollama")
            model: Nome do modelo de embeddings
            api_key: API key (opcional, usa variável de ambiente se não fornecida)
            base_url: Base URL para Ollama (opcional, padrão: http://localhost:11434)
        """
        self.provider = provider
        self.model = model

        if provider == "openai":
            # Usa API key fornecida ou busca do ambiente
            resolved_key = api_key or os.getenv("OPENAI_API_KEY")
            self._embeddings = OpenAIEmbeddings(
                model=model,
                api_key=resolved_key,
            )
        elif provider == "ollama":
            # Ollama local - não precisa de API key
            self._embeddings = OllamaEmbeddings(
                model=model,
                base_url=base_url or "http://localhost:11434",
            )
        else:
            raise ValueError(f"Provedor não suportado: {provider}")

    @classmethod
    def from_config(cls, config_path: str = "config.toml", override_provider: Optional[str] = None) -> "EmbeddingsManager":
        """
        Cria EmbeddingsManager a partir de arquivo de configuração TOML.

        Args:
            config_path: Caminho para o arquivo config.toml
            override_provider: Substitui o provider do config.toml ("openai" ou "ollama")

        Returns:
            Instância configurada do EmbeddingsManager
        """
        config = toml.load(config_path)
        embeddings_config = config.get("embeddings", {})

        # Usa override se fornecido, senão usa do config
        provider = override_provider or embeddings_config.get("provider", "openai")
        
        # Ajusta modelo baseado no provider
        if provider == "ollama":
            model = embeddings_config.get("model", "bge-m3")
        else:
            model = embeddings_config.get("model", "text-embedding-3-small")

        return cls(
            provider=provider,
            model=model,
            base_url=embeddings_config.get("base_url"),
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Gera embeddings para uma lista de textos.

        Args:
            texts: Lista de textos para gerar embeddings

        Returns:
            Lista de vetores de embeddings
        """
        return self._embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Gera embedding para uma query.

        Args:
            text: Texto da query

        Returns:
            Vetor de embedding
        """
        return self._embeddings.embed_query(text)

    @property
    def embeddings(self) -> Embeddings:
        """Retorna o objeto de embeddings do LangChain."""
        return self._embeddings

    def get_info(self) -> dict:
        """Retorna informações sobre o modelo de embeddings."""
        return {
            "provider": self.provider,
            "model": self.model,
        }
