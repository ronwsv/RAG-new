# 💾 Persistência de Dados - RAG System

## 📂 ONDE OS DADOS FICAM SALVOS

Todos os dados do sistema ficam armazenados **localmente** nas seguintes pastas:

```
RAG-new/
├── data/
│   ├── documents/          ← 📄 Seus documentos originais (opcional)
│   └── faiss_index/        ← 🔍 Índice vetorial (OBRIGATÓRIO)
│       ├── index.faiss     ← Base vetorial FAISS
│       └── index.pkl       ← Metadados dos documentos
```

## ✅ DADOS SÃO PERMANENTES

✅ **Os dados NÃO são perdidos** quando você:
- Reinicia o Docker
- Para e inicia o container novamente (`docker compose down/up`)
- Desliga o computador
- Atualiza o código da aplicação

❌ **Os dados SÃO perdidos** apenas se você:
- Deletar manualmente a pasta `data/faiss_index/`
- Rodar `docker compose down -v` (flag `-v` remove volumes)
- Apagar os arquivos `index.faiss` e `index.pkl`

## 🔍 VERIFICANDO OS DADOS SALVOS

### Pelo Windows Explorer:
1. Navegue até a pasta do projeto
2. Abra `data/faiss_index/`
3. Você verá os arquivos:
   - `index.faiss` (centenas de KB) - índice vetorial
   - `index.pkl` (dezenas de KB) - metadados

### Via PowerShell:
```powershell
# Ver tamanho dos arquivos
ls ./data/faiss_index/

# Ver detalhes do índice
Get-ChildItem ./data/faiss_index/ | Select-Object Name, Length, LastWriteTime
```

### Via Docker:
```bash
# Ver arquivos dentro do container
docker exec rag-simple ls -lh /app/data/faiss_index/
```

## 📊 ENTENDENDO O ÍNDICE

### `index.faiss` - Base Vetorial
- Contém os **embeddings** de todos os chunks de texto
- Tamanho cresce conforme você adiciona documentos
- Permite busca semântica ultrarrápida
- **~700KB** por 1.000 chunks (aproximadamente)

### `index.pkl` - Metadados
- Armazena informações sobre cada chunk:
  - Conteúdo do texto original
  - Nome do arquivo de origem
  - Número da página
  - Chunk ID
- Formato: Python Pickle serializado
- **~70KB** por 1.000 chunks (aproximadamente)

## 🔄 COMPORTAMENTO DO SISTEMA

### Ao Iniciar a Aplicação:
1. ✅ Sistema verifica se existe `data/faiss_index/`
2. ✅ Se existir, **carrega automaticamente** o índice
3. ✅ Você pode começar a fazer perguntas imediatamente
4. ℹ️ Se não existir, precisa indexar documentos primeiro

### Ao Indexar Novos Documentos:
1. 📄 Sistema processa os documentos
2. ➕ **Adiciona** ao índice existente (não sobrescreve!)
3. 💾 Salva automaticamente em `data/faiss_index/`
4. ✅ Dados ficam persistidos no disco

### Ao Fazer Perguntas:
1. 🔍 Sistema busca no índice local (`index.faiss`)
2. 📚 Recupera metadados de `index.pkl`
3. 🤖 Envia contexto para o LLM
4. ✨ Retorna resposta + fontes

## 🗑️ LIMPANDO OS DADOS

### Remover Índice Completamente:
```powershell
# Windows - Remove tudo
Remove-Item -Recurse -Force ./data/faiss_index/*

# Manter apenas o .gitkeep
Remove-Item ./data/faiss_index/index.* -Force
```

### Backup do Índice:
```powershell
# Criar backup
Copy-Item -Recurse ./data/faiss_index ./data/faiss_index_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')

# Restaurar backup
Copy-Item -Recurse ./data/faiss_index_backup_20251210_143000/* ./data/faiss_index/
```

## 📈 MONITORANDO O CRESCIMENTO

```powershell
# Tamanho total do índice
(Get-ChildItem ./data/faiss_index/ -File | Measure-Object -Property Length -Sum).Sum / 1MB

# Última atualização
Get-ChildItem ./data/faiss_index/index.faiss | Select-Object Name, LastWriteTime
```

## 🎯 BOAS PRÁTICAS

### ✅ Recomendado:
- Fazer backup periódico da pasta `faiss_index/`
- Verificar o tamanho do índice regularmente
- Manter um registro dos documentos indexados
- Testar restauração de backups

### ⚠️ Atenção:
- Não editar manualmente `index.faiss` ou `index.pkl`
- Não mover arquivos entre diferentes projetos RAG
- Não usar o mesmo índice para embeddings diferentes
- Cuidado ao usar Git com arquivos grandes (usar `.gitignore`)

## 🐳 DIFERENÇA: Volumes Docker vs Pastas Locais

### ❌ **ANTES** (Volumes Docker - ocultos):
```yaml
volumes:
  - rag-documents:/app/data/documents
  - rag-faiss:/app/data/faiss_index
```
- Dados ocultos no sistema interno do Docker
- Difícil de visualizar e fazer backup
- Localização: `/var/lib/docker/volumes/`

### ✅ **AGORA** (Pastas Locais - visíveis):
```yaml
volumes:
  - ./data/documents:/app/data/documents
  - ./data/faiss_index:/app/data/faiss_index
```
- Dados visíveis na pasta do projeto
- Fácil backup, visualização e controle
- Localização: `seu_projeto/data/`

## 🔧 TROUBLESHOOTING

### Problema: "Índice não encontrado"
**Solução:** Verifique se os arquivos existem:
```powershell
Test-Path ./data/faiss_index/index.faiss
Test-Path ./data/faiss_index/index.pkl
```

### Problema: "Permissões negadas"
**Solução:** Ajuste permissões (se no Linux/Mac):
```bash
chmod -R 755 ./data/faiss_index/
```

### Problema: "Índice corrompido"
**Solução:** Restaure do backup ou reindexe:
```powershell
# Remover índice corrompido
Remove-Item ./data/faiss_index/index.* -Force

# Reindexar documentos pela interface web
```

## 📞 SUPORTE

Para mais informações:
- Documentação LangChain: https://python.langchain.com/docs/
- FAISS Wiki: https://github.com/facebookresearch/faiss/wiki
- Issue do projeto: [criar link para seu repositório]

---

**Última atualização:** 10/12/2025  
**Versão:** 1.0
