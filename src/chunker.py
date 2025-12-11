"""Chunker - Estratégias de chunking para documentos."""

from typing import List, Optional

import toml
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)


class Chunker:
    """Divide documentos em chunks otimizados para RAG."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None,
    ):
        """
        Inicializa o chunker.

        Args:
            chunk_size: Tamanho máximo de cada chunk em caracteres
            chunk_overlap: Sobreposição entre chunks (10% recomendado)
            separators: Lista de separadores para split
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
        )

        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "header_1"),
                ("##", "header_2"),
                ("###", "header_3"),
            ]
        )

    @classmethod
    def from_config(cls, config_path: str = "config.toml") -> "Chunker":
        """
        Cria Chunker a partir de arquivo de configuração TOML.

        Args:
            config_path: Caminho para o arquivo config.toml

        Returns:
            Instância configurada do Chunker
        """
        config = toml.load(config_path)
        chunking_config = config.get("chunking", {})

        return cls(
            chunk_size=chunking_config.get("chunk_size", 512),
            chunk_overlap=chunking_config.get("chunk_overlap", 50),
            separators=chunking_config.get("separators"),
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """
        Divide documentos em chunks.

        Args:
            documents: Lista de Documents para dividir

        Returns:
            Lista de Documents (chunks) com metadados preservados
        """
        all_chunks = []

        for doc in documents:
            # Usa splitter específico para Markdown
            if doc.metadata.get("file_type") in [".md", ".markdown"]:
                chunks = self._split_markdown(doc)
            else:
                chunks = self._split_text(doc)

            # Adiciona índice do chunk aos metadados
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_index"] = i
                chunk.metadata["total_chunks"] = len(chunks)

            all_chunks.extend(chunks)

        return all_chunks

    def _split_text(self, document: Document) -> List[Document]:
        """Divide documento usando RecursiveCharacterTextSplitter."""
        return self._text_splitter.split_documents([document])

    def _split_markdown(self, document: Document) -> List[Document]:
        """Divide documento Markdown preservando estrutura de headers."""
        # Primeiro split por headers
        md_splits = self._markdown_splitter.split_text(document.page_content)

        # Depois aplica split recursivo em cada seção
        final_chunks = []
        for split in md_splits:
            # Cria documento temporário com metadados do header
            temp_doc = Document(
                page_content=split.page_content,
                metadata={**document.metadata, **split.metadata}
            )
            chunks = self._text_splitter.split_documents([temp_doc])
            final_chunks.extend(chunks)

        return final_chunks

    def get_stats(self, chunks: List[Document]) -> dict:
        """
        Retorna estatísticas dos chunks.

        Args:
            chunks: Lista de chunks

        Returns:
            Dicionário com estatísticas
        """
        if not chunks:
            return {"total_chunks": 0}

        lengths = [len(c.page_content) for c in chunks]

        return {
            "total_chunks": len(chunks),
            "avg_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_characters": sum(lengths),
        }
