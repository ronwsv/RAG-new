"""Vector Store - FAISS para indexação e busca de documentos."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import toml
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from .embeddings import EmbeddingsManager


class VectorStore:
    """Gerencia o índice FAISS para busca por similaridade."""

    METADATA_FILE = "index_metadata.json"
    CONTEXTS_BASE_DIR = "data/faiss_index"

    def __init__(
        self,
        embeddings: Embeddings,
        index_path: Optional[str] = None,
        context_name: Optional[str] = None,
    ):
        """
        Inicializa o Vector Store.

        Args:
            embeddings: Objeto de embeddings do LangChain
            index_path: Caminho para salvar/carregar o índice (deprecado se usar context_name)
            context_name: Nome do contexto (ex: cond_169) - preferido
        """
        self._embeddings = embeddings
        self._context_name = context_name or "default"

        # Se context_name for fornecido, usa o caminho do contexto
        if context_name:
            self._index_path = str(Path(self.CONTEXTS_BASE_DIR) / context_name)
        else:
            self._index_path = index_path

        self._vectorstore: Optional[FAISS] = None
        self._indexed_files: List[str] = []
        self._indexed_at: Optional[str] = None

    @classmethod
    def from_config(
        cls,
        config_path: str = "config.toml",
        embeddings_manager: Optional[EmbeddingsManager] = None,
        context_name: Optional[str] = None,
    ) -> "VectorStore":
        """
        Cria VectorStore a partir de arquivo de configuração TOML.

        Args:
            config_path: Caminho para o arquivo config.toml
            embeddings_manager: Gerenciador de embeddings (opcional)
            context_name: Nome do contexto (ex: cond_169)

        Returns:
            Instância configurada do VectorStore
        """
        config = toml.load(config_path)
        paths_config = config.get("paths", {})

        if embeddings_manager is None:
            embeddings_manager = EmbeddingsManager.from_config(config_path)

        # Se context_name fornecido, usa sistema de contextos
        if context_name:
            return cls(
                embeddings=embeddings_manager.embeddings,
                context_name=context_name,
            )

        return cls(
            embeddings=embeddings_manager.embeddings,
            index_path=paths_config.get("faiss_index_dir", "data/faiss_index"),
        )

    @property
    def context_name(self) -> str:
        """Retorna o nome do contexto atual."""
        return self._context_name

    def create_index(self, documents: List[Document]) -> None:
        """
        Cria um novo índice FAISS a partir de documentos.

        Args:
            documents: Lista de Documents para indexar
        """
        if not documents:
            raise ValueError("Lista de documentos vazia")

        self._vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self._embeddings,
        )

    def add_documents(self, documents: List[Document]) -> None:
        """
        Adiciona documentos ao índice existente.

        Args:
            documents: Lista de Documents para adicionar
        """
        if self._vectorstore is None:
            self.create_index(documents)
        else:
            self._vectorstore.add_documents(documents)

    def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: Optional[float] = None,
    ) -> List[Tuple[Document, float]]:
        """
        Busca documentos similares à query.

        Args:
            query: Texto da consulta
            top_k: Número de resultados
            score_threshold: Threshold mínimo de similaridade

        Returns:
            Lista de tuplas (Document, score)
        """
        if self._vectorstore is None:
            raise RuntimeError("Índice não inicializado. Crie ou carregue um índice primeiro.")

        results = self._vectorstore.similarity_search_with_score(
            query=query,
            k=top_k,
        )

        # Filtra por threshold se especificado
        if score_threshold is not None:
            results = [(doc, score) for doc, score in results if score <= score_threshold]

        return results

    def search_documents(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Document]:
        """
        Busca documentos similares (retorna apenas Documents).

        Args:
            query: Texto da consulta
            top_k: Número de resultados

        Returns:
            Lista de Documents
        """
        if self._vectorstore is None:
            raise RuntimeError("Índice não inicializado.")

        return self._vectorstore.similarity_search(query=query, k=top_k)

    def save(self, path: Optional[str] = None, file_names: Optional[List[str]] = None) -> None:
        """
        Salva o índice FAISS em disco.

        Args:
            path: Caminho para salvar (usa index_path padrão se não fornecido)
            file_names: Lista de nomes dos arquivos indexados
        """
        if self._vectorstore is None:
            raise RuntimeError("Índice não inicializado.")

        save_path = path or self._index_path
        if save_path is None:
            raise ValueError("Caminho de salvamento não especificado")

        Path(save_path).mkdir(parents=True, exist_ok=True)
        self._vectorstore.save_local(save_path)

        # Salva metadados (lista de arquivos)
        if file_names:
            self._indexed_files = file_names
        self._indexed_at = datetime.now().isoformat()
        self._save_metadata(save_path)

    def _save_metadata(self, path: str) -> None:
        """Salva metadados do índice em arquivo JSON."""
        metadata = {
            "indexed_files": self._indexed_files,
            "indexed_at": self._indexed_at,
            "total_files": len(self._indexed_files),
        }
        metadata_path = Path(path) / self.METADATA_FILE
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def _load_metadata(self, path: str) -> None:
        """Carrega metadados do índice de arquivo JSON."""
        metadata_path = Path(path) / self.METADATA_FILE
        if metadata_path.exists():
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                self._indexed_files = metadata.get("indexed_files", [])
                self._indexed_at = metadata.get("indexed_at")

    def load(self, path: Optional[str] = None) -> None:
        """
        Carrega um índice FAISS do disco.

        Args:
            path: Caminho para carregar (usa index_path padrão se não fornecido)
        """
        load_path = path or self._index_path
        if load_path is None:
            raise ValueError("Caminho de carregamento não especificado")

        # Verifica se o arquivo index.faiss existe (não apenas o diretório)
        index_file = Path(load_path) / "index.faiss"
        if not index_file.exists():
            raise FileNotFoundError(f"Arquivo de índice não encontrado: {index_file}")

        self._vectorstore = FAISS.load_local(
            load_path,
            self._embeddings,
            allow_dangerous_deserialization=True,
        )

        # Carrega metadados
        self._load_metadata(load_path)

    def get_retriever(self, top_k: int = 5):
        """
        Retorna um retriever para uso com LangChain chains.

        Args:
            top_k: Número de documentos a recuperar

        Returns:
            Retriever do FAISS
        """
        if self._vectorstore is None:
            raise RuntimeError("Índice não inicializado.")

        return self._vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k},
        )

    @property
    def is_initialized(self) -> bool:
        """Verifica se o índice está inicializado."""
        return self._vectorstore is not None

    @property
    def indexed_files(self) -> List[str]:
        """Retorna lista de arquivos indexados."""
        return self._indexed_files

    @property
    def indexed_at(self) -> Optional[str]:
        """Retorna data/hora da indexação."""
        return self._indexed_at

    def get_stats(self) -> dict:
        """Retorna estatísticas do índice."""
        if self._vectorstore is None:
            return {"initialized": False}

        return {
            "initialized": True,
            "total_documents": len(self._vectorstore.docstore._dict),
            "indexed_files": self._indexed_files,
            "total_files": len(self._indexed_files),
            "indexed_at": self._indexed_at,
        }
