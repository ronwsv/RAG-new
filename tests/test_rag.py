"""Testes básicos para o RAG Simple."""

import sys
from pathlib import Path

# Adiciona diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.document_loader import DocumentLoader
from src.chunker import Chunker
from src.toon_formatter import ToonFormatter


def test_document_loader_formats():
    """Testa formatos suportados pelo DocumentLoader."""
    loader = DocumentLoader()
    formats = loader.get_supported_formats()

    assert ".pdf" in formats
    assert ".docx" in formats
    assert ".xlsx" in formats
    assert ".txt" in formats
    assert ".md" in formats

    print("✅ test_document_loader_formats passed")


def test_chunker_creation():
    """Testa criação do Chunker."""
    chunker = Chunker(chunk_size=512, chunk_overlap=50)

    assert chunker.chunk_size == 512
    assert chunker.chunk_overlap == 50

    print("✅ test_chunker_creation passed")


def test_toon_formatter():
    """Testa formatação TOON."""
    from langchain_core.documents import Document

    formatter = ToonFormatter(use_toon=False)  # Usa JSON como fallback

    docs = [
        Document(
            page_content="Conteúdo de teste",
            metadata={"source": "test.pdf"}
        )
    ]

    output = formatter.format_documents(docs)
    assert "Conteúdo de teste" in output
    assert "test.pdf" in output

    print("✅ test_toon_formatter passed")


def test_toon_formatter_type():
    """Testa tipo de formato do ToonFormatter."""
    formatter_json = ToonFormatter(use_toon=False)
    assert formatter_json.format_type == "JSON"

    print("✅ test_toon_formatter_type passed")


if __name__ == "__main__":
    test_document_loader_formats()
    test_chunker_creation()
    test_toon_formatter()
    test_toon_formatter_type()

    print("\n✅ Todos os testes passaram!")
