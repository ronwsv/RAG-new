"""Document Loader - Carregamento de documentos multi-formato com OCR."""

from pathlib import Path
from typing import List, Optional
from datetime import datetime
import io

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    TextLoader,
)

# OCR imports (opcional)
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class DocumentLoader:
    """Carrega documentos de diversos formatos com detecção automática."""

    SUPPORTED_EXTENSIONS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "docx",
        ".xlsx": "xlsx",
        ".xls": "xlsx",
        ".txt": "text",
        ".md": "text",
        ".markdown": "text",
    }

    def __init__(self):
        self._loaders = {
            "pdf": self._load_pdf,
            "docx": self._load_docx,
            "xlsx": self._load_xlsx,
            "text": self._load_text,
        }

    def load(self, file_path: str | Path) -> List[Document]:
        """
        Carrega um documento e retorna lista de Documents do LangChain.

        Args:
            file_path: Caminho para o arquivo

        Returns:
            Lista de Documents com conteúdo e metadados
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Formato não suportado: {extension}. "
                f"Formatos suportados: {list(self.SUPPORTED_EXTENSIONS.keys())}"
            )

        doc_type = self.SUPPORTED_EXTENSIONS[extension]
        loader_func = self._loaders[doc_type]

        documents = loader_func(path)

        # Enriquece metadados
        for doc in documents:
            doc.metadata.update({
                "source": str(path.name),
                "file_path": str(path.absolute()),
                "file_type": extension,
                "loaded_at": datetime.now().isoformat(),
            })

        return documents

    def load_directory(
        self,
        directory: str | Path,
        recursive: bool = True
    ) -> List[Document]:
        """
        Carrega todos os documentos de um diretório.

        Args:
            directory: Caminho para o diretório
            recursive: Se True, busca em subdiretórios

        Returns:
            Lista de Documents de todos os arquivos
        """
        dir_path = Path(directory)

        if not dir_path.is_dir():
            raise NotADirectoryError(f"Não é um diretório: {directory}")

        all_documents = []
        pattern = "**/*" if recursive else "*"

        for file_path in dir_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    docs = self.load(file_path)
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"Erro ao carregar {file_path}: {e}")

        return all_documents

    def _load_pdf(self, path: Path) -> List[Document]:
        """Carrega arquivo PDF com fallback para OCR se necessário."""
        # Tenta extração normal primeiro
        loader = PyPDFLoader(str(path))
        documents = loader.load()

        # Verifica se extraiu texto
        total_text = sum(len(doc.page_content.strip()) for doc in documents)

        # Se tem pouco texto, tenta OCR
        if total_text < 50 and OCR_AVAILABLE:
            ocr_documents = self._load_pdf_with_ocr(path)
            if ocr_documents:
                return ocr_documents

        return documents

    def _load_pdf_with_ocr(self, path: Path) -> List[Document]:
        """Carrega PDF usando OCR (para PDFs digitalizados)."""
        if not OCR_AVAILABLE:
            return []

        try:
            # Converte PDF para imagens
            images = convert_from_path(str(path), dpi=200)

            documents = []
            for i, image in enumerate(images):
                # Extrai texto da imagem usando Tesseract
                text = pytesseract.image_to_string(image, lang='por+eng')

                if text.strip():
                    doc = Document(
                        page_content=text,
                        metadata={
                            "page": i,
                            "source": str(path.name),
                            "extraction_method": "ocr",
                        }
                    )
                    documents.append(doc)

            return documents

        except Exception as e:
            print(f"Erro no OCR de {path}: {e}")
            return []

    def _load_docx(self, path: Path) -> List[Document]:
        """Carrega arquivo DOCX/DOC."""
        loader = Docx2txtLoader(str(path))
        return loader.load()

    def _load_xlsx(self, path: Path) -> List[Document]:
        """Carrega arquivo XLSX/XLS."""
        loader = UnstructuredExcelLoader(str(path), mode="elements")
        return loader.load()

    def _load_text(self, path: Path) -> List[Document]:
        """Carrega arquivo TXT/MD."""
        loader = TextLoader(str(path), encoding="utf-8")
        return loader.load()

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Retorna lista de extensões suportadas."""
        return list(cls.SUPPORTED_EXTENSIONS.keys())
