"""Context Manager - Gerencia múltiplos contextos independentes."""

import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime


class ContextManager:
    """Gerencia múltiplos contextos (ex: cond_169, cond_170)."""

    CONTEXTS_DIR = Path("data/faiss_index")

    def __init__(self):
        """Inicializa o gerenciador de contextos."""
        self.CONTEXTS_DIR.mkdir(parents=True, exist_ok=True)

    def list_contexts(self) -> List[str]:
        """Lista todos os contextos disponíveis."""
        contexts = []
        for item in self.CONTEXTS_DIR.iterdir():
            if item.is_dir():
                # Contexto válido se tem index.faiss OU metadata.json
                has_index = (item / "index.faiss").exists()
                has_metadata = (item / "metadata.json").exists()
                if has_index or has_metadata:
                    contexts.append(item.name)
        return sorted(contexts)

    def create_context(self, context_name: str, description: str = "") -> bool:
        """
        Cria um novo contexto (pasta para índice).

        Args:
            context_name: Nome do contexto (ex: cond_169)
            description: Descrição opcional

        Returns:
            True se criado, False se já existe
        """
        context_path = self.CONTEXTS_DIR / context_name

        if context_path.exists():
            return False

        context_path.mkdir(parents=True, exist_ok=True)

        # Salva metadados iniciais
        metadata = {
            "name": context_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "indexed_files": [],
            "total_documents": 0,
            "last_updated": None,
        }

        metadata_file = context_path / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return True

    def get_context_path(self, context_name: str) -> Path:
        """Retorna o caminho do contexto."""
        return self.CONTEXTS_DIR / context_name

    def context_exists(self, context_name: str) -> bool:
        """Verifica se um contexto existe (mesmo sem índice)."""
        context_path = self.get_context_path(context_name)
        return context_path.exists()

    def has_index(self, context_name: str) -> bool:
        """Verifica se um contexto tem índice FAISS."""
        context_path = self.get_context_path(context_name)
        return (context_path / "index.faiss").exists()

    def get_context_metadata(self, context_name: str) -> Optional[Dict]:
        """Retorna metadados do contexto."""
        metadata_file = self.get_context_path(context_name) / "metadata.json"

        if not metadata_file.exists():
            return None

        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_context_metadata(
        self,
        context_name: str,
        indexed_files: List[str],
        total_documents: int,
    ) -> None:
        """Atualiza metadados do contexto após indexação."""
        context_path = self.get_context_path(context_name)
        metadata_file = context_path / "metadata.json"

        # Carrega metadados existentes ou cria novos
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        else:
            metadata = {
                "name": context_name,
                "description": "",
                "created_at": datetime.now().isoformat(),
            }

        # Atualiza campos
        metadata["indexed_files"] = indexed_files
        metadata["total_documents"] = total_documents
        metadata["last_updated"] = datetime.now().isoformat()

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def delete_context(self, context_name: str) -> bool:
        """Deleta um contexto completamente."""
        context_path = self.get_context_path(context_name)

        if not context_path.exists():
            return False

        try:
            shutil.rmtree(context_path)
            return True
        except Exception as e:
            print(f"Erro ao deletar contexto: {e}")
            return False

    def rename_context(self, old_name: str, new_name: str) -> bool:
        """Renomeia um contexto."""
        old_path = self.get_context_path(old_name)
        new_path = self.get_context_path(new_name)

        if not old_path.exists() or new_path.exists():
            return False

        try:
            old_path.rename(new_path)

            # Atualiza nome no metadata
            metadata = self.get_context_metadata(new_name)
            if metadata:
                metadata["name"] = new_name
                metadata_file = new_path / "metadata.json"
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)

            return True
        except Exception:
            return False

    def get_stats(self) -> Dict:
        """Retorna estatísticas gerais de todos os contextos."""
        contexts = self.list_contexts()
        total_docs = 0
        total_files = 0

        contexts_info = []
        for context_name in contexts:
            metadata = self.get_context_metadata(context_name)
            if metadata:
                ctx_docs = metadata.get("total_documents", 0)
                ctx_files = len(metadata.get("indexed_files", []))
                total_docs += ctx_docs
                total_files += ctx_files
                contexts_info.append({
                    "name": context_name,
                    "documents": ctx_docs,
                    "files": ctx_files,
                    "last_updated": metadata.get("last_updated"),
                })

        return {
            "total_contexts": len(contexts),
            "contexts": contexts_info,
            "total_documents": total_docs,
            "total_files": total_files,
        }

    def clear_context_index(self, context_name: str) -> bool:
        """Limpa apenas o índice de um contexto, mantendo o contexto."""
        context_path = self.get_context_path(context_name)

        if not context_path.exists():
            return False

        try:
            # Remove arquivos de índice
            index_files = ["index.faiss", "index.pkl"]
            for file_name in index_files:
                file_path = context_path / file_name
                if file_path.exists():
                    file_path.unlink()

            # Reseta metadados
            self.update_context_metadata(context_name, [], 0)

            return True
        except Exception as e:
            print(f"Erro ao limpar índice: {e}")
            return False
