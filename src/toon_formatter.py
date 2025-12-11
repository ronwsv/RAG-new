"""TOON Formatter - Serialização de contexto em formato TOON para economia de tokens."""

from typing import List, Dict, Any, Optional

try:
    import toons
    TOONS_AVAILABLE = True
except ImportError:
    TOONS_AVAILABLE = False
    import json

from langchain_core.documents import Document


class ToonFormatter:
    """
    Formata contexto recuperado em formato TOON para envio ao LLM.

    TOON (Token-Oriented Object Notation) economiza 30-60% de tokens
    comparado a JSON, ideal para maximizar contexto em prompts de LLM.
    """

    def __init__(self, use_toon: bool = True):
        """
        Inicializa o formatter.

        Args:
            use_toon: Se True, usa TOON. Se False ou indisponível, usa JSON.
        """
        self.use_toon = use_toon and TOONS_AVAILABLE

        if use_toon and not TOONS_AVAILABLE:
            print("Aviso: biblioteca 'toons' não disponível. Usando JSON como fallback.")

    def format_documents(
        self,
        documents: List[Document],
        include_metadata: bool = True,
        max_content_length: Optional[int] = None,
    ) -> str:
        """
        Formata lista de Documents para contexto do LLM.

        Args:
            documents: Lista de Documents recuperados
            include_metadata: Se True, inclui metadados (source, etc)
            max_content_length: Limite de caracteres por conteúdo

        Returns:
            String formatada em TOON ou JSON
        """
        sources = []

        for i, doc in enumerate(documents):
            content = doc.page_content

            if max_content_length and len(content) > max_content_length:
                content = content[:max_content_length] + "..."

            source_data = {
                "id": i + 1,
                "content": content,
            }

            if include_metadata:
                source_data["file"] = doc.metadata.get("source", "unknown")

                # Adiciona chunk info se disponível
                if "chunk_index" in doc.metadata:
                    source_data["chunk"] = f"{doc.metadata['chunk_index'] + 1}/{doc.metadata.get('total_chunks', '?')}"

            sources.append(source_data)

        context = {"sources": sources}

        return self._serialize(context)

    def format_with_scores(
        self,
        results: List[tuple],  # List[(Document, float)]
        include_scores: bool = True,
    ) -> str:
        """
        Formata resultados de busca com scores de similaridade.

        Args:
            results: Lista de tuplas (Document, score)
            include_scores: Se True, inclui scores na saída

        Returns:
            String formatada em TOON ou JSON
        """
        sources = []

        for i, (doc, score) in enumerate(results):
            source_data = {
                "id": i + 1,
                "content": doc.page_content,
                "file": doc.metadata.get("source", "unknown"),
            }

            if include_scores:
                source_data["relevance"] = round(1 - score, 3)  # Converte distância para similaridade

            sources.append(source_data)

        context = {"sources": sources}

        return self._serialize(context)

    def format_query_context(
        self,
        query: str,
        documents: List[Document],
    ) -> str:
        """
        Formata query e contexto juntos para o prompt.

        Args:
            query: Pergunta do usuário
            documents: Documentos recuperados

        Returns:
            String formatada com query e contexto
        """
        sources = []

        for i, doc in enumerate(documents):
            sources.append({
                "id": i + 1,
                "content": doc.page_content,
                "file": doc.metadata.get("source", "unknown"),
            })

        data = {
            "query": query,
            "context": {"sources": sources},
        }

        return self._serialize(data)

    def _serialize(self, data: Dict[str, Any]) -> str:
        """Serializa dados para TOON ou JSON."""
        if self.use_toon:
            return toons.dumps(data)
        else:
            return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def estimate_token_savings(json_str: str, toon_str: str) -> dict:
        """
        Estima economia de tokens entre JSON e TOON.

        Args:
            json_str: String em formato JSON
            toon_str: String em formato TOON

        Returns:
            Dicionário com estatísticas de economia
        """
        json_chars = len(json_str)
        toon_chars = len(toon_str)

        # Estimativa aproximada: ~4 caracteres por token
        json_tokens_est = json_chars / 4
        toon_tokens_est = toon_chars / 4

        savings_pct = ((json_chars - toon_chars) / json_chars) * 100 if json_chars > 0 else 0

        return {
            "json_chars": json_chars,
            "toon_chars": toon_chars,
            "json_tokens_est": round(json_tokens_est),
            "toon_tokens_est": round(toon_tokens_est),
            "savings_percent": round(savings_pct, 1),
        }

    @property
    def format_type(self) -> str:
        """Retorna o tipo de formato em uso."""
        return "TOON" if self.use_toon else "JSON"
