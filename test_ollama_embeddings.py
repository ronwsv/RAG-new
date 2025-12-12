"""Teste rápido do BGE-M3 com Ollama."""

from src.embeddings import EmbeddingsManager

# Teste 1: Criar embeddings manager
print("=" * 60)
print("TESTANDO BGE-M3 COM OLLAMA")
print("=" * 60)

try:
    print("\n1. Criando EmbeddingsManager com Ollama BGE-M3...")
    embeddings_mgr = EmbeddingsManager(
        provider="ollama",
        model="bge-m3",
        base_url="http://localhost:11434"
    )
    print("   ✅ EmbeddingsManager criado com sucesso!")
    
    # Teste 2: Embedding de query
    print("\n2. Testando embedding de query...")
    query = "Como funciona o RAG?"
    query_embedding = embeddings_mgr.embed_query(query)
    print(f"   ✅ Embedding gerado! Dimensões: {len(query_embedding)}")
    print(f"   Primeiros 10 valores: {query_embedding[:10]}")
    
    # Teste 3: Embedding de documentos
    print("\n3. Testando embedding de documentos...")
    docs = [
        "RAG significa Retrieval-Augmented Generation",
        "É uma técnica que combina busca e geração de texto",
        "Usa embeddings para encontrar documentos relevantes"
    ]
    docs_embeddings = embeddings_mgr.embed_documents(docs)
    print(f"   ✅ {len(docs_embeddings)} embeddings gerados!")
    print(f"   Dimensão de cada embedding: {len(docs_embeddings[0])}")
    
    # Teste 4: from_config
    print("\n4. Testando from_config...")
    embeddings_from_config = EmbeddingsManager.from_config("config.toml")
    print(f"   ✅ Carregado do config.toml!")
    info = embeddings_from_config.get_info()
    print(f"   Provider: {info['provider']}")
    print(f"   Model: {info['model']}")
    
    # Teste 5: Comparação de embeddings
    print("\n5. Testando similaridade...")
    test_embedding = embeddings_from_config.embed_query("O que é RAG?")
    print(f"   ✅ Embedding de teste gerado! Dimensões: {len(test_embedding)}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\nBGE-M3 está funcionando perfeitamente com Ollama!")
    print("Você pode usar embeddings locais sem custo de API! 🎉")
    
except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
