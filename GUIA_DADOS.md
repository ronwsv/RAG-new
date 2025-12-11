# 🎯 GUIA RÁPIDO: Onde estão meus dados?

## 📍 LOCALIZAÇÃO DOS DADOS

```
📁 SEU_PROJETO/
└── 📁 data/
    ├── 📁 documents/        ← Documentos originais (opcional)
    └── 📁 faiss_index/      ← ⭐ SEUS DADOS INDEXADOS ⭐
        ├── 📄 index.faiss   ← Base vetorial (busca)
        └── 📄 index.pkl     ← Metadados (conteúdo + fontes)
```

## ✅ DADOS SÃO PERMANENTES!

```
┌─────────────────────────────────────────┐
│  VOCÊ PODE:                             │
├─────────────────────────────────────────┤
│  ✅ Reiniciar o Docker                  │
│  ✅ Desligar o computador               │
│  ✅ Fazer docker compose down/up        │
│  ✅ Atualizar o código                  │
│  ✅ Fazer backup dos arquivos           │
│  ✅ Ver os arquivos no Explorer         │
└─────────────────────────────────────────┘

         ⬇️ SEUS DADOS PERMANECEM! ⬇️
```

## 🔍 COMO VERIFICAR OS DADOS

### Método 1: Windows Explorer
```
1. Abra o explorador de arquivos
2. Navegue até a pasta do projeto
3. Entre em: data\faiss_index\
4. Você verá: index.faiss e index.pkl
```

### Método 2: PowerShell
```powershell
# Ver arquivos e tamanhos
ls ./data/faiss_index/

# Ver última modificação
Get-ChildItem ./data/faiss_index/*.faiss | Select-Object Name, Length, LastWriteTime
```

### Método 3: Interface Web
```
1. Acesse: http://localhost:7860
2. Clique em "📊 Atualizar Status"
3. Veja: quantos documentos, tamanho, localização
```

## 📊 ENTENDENDO OS ARQUIVOS

```
┌─────────────────────────────────────────────────────────┐
│  index.faiss (700-800 KB)                               │
├─────────────────────────────────────────────────────────┤
│  • Vetores numéricos de cada chunk                     │
│  • Permite busca semântica rápida                       │
│  • Cresce ~1 MB por 1.000 documentos                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  index.pkl (70-80 KB)                                   │
├─────────────────────────────────────────────────────────┤
│  • Texto original de cada chunk                         │
│  • Nome dos arquivos fonte                              │
│  • Números de página                                    │
│  • Outros metadados                                     │
└─────────────────────────────────────────────────────────┘
```

## 🔄 FLUXO DE DADOS

```
1️⃣ INDEXAÇÃO
   📄 Upload arquivo (PDF, DOCX, etc.)
        ↓
   ✂️ Divisão em chunks
        ↓
   🔢 Geração de embeddings
        ↓
   💾 Salvamento em ./data/faiss_index/
        ↓
   ✅ PERMANENTE!

2️⃣ CONSULTA
   ❓ Sua pergunta
        ↓
   🔍 Busca em index.faiss
        ↓
   📚 Recupera dados de index.pkl
        ↓
   🤖 Envia para LLM (GPT-4)
        ↓
   ✨ Resposta com fontes
```

## 💾 BACKUP DOS DADOS

### Backup Manual (Windows)
```powershell
# Criar backup com data/hora
$backupName = "faiss_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Recurse ./data/faiss_index "./$backupName"
```

### Backup Automático (Script)
```powershell
# Criar script backup_rag.ps1
$source = ".\data\faiss_index"
$dest = ".\backups\faiss_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Recurse $source $dest
Write-Host "Backup criado em: $dest"
```

### Restaurar Backup
```powershell
# Restaurar backup específico
Copy-Item -Recurse ".\faiss_backup_20251210_143000\*" ".\data\faiss_index\" -Force
```

## 🗑️ LIMPANDO OS DADOS

### Opção 1: Pelo Explorer
```
1. Navegue até data/faiss_index/
2. Selecione index.faiss e index.pkl
3. Pressione Delete
4. Próxima indexação criará novo índice
```

### Opção 2: PowerShell
```powershell
# Limpar apenas o índice (manter estrutura)
Remove-Item ./data/faiss_index/index.* -Force

# Verificar
ls ./data/faiss_index/
```

### Opção 3: Interface Web
```
Não há botão de limpar (por segurança)
Use os métodos acima para limpar manualmente
```

## ⚠️ IMPORTANTE

### ✅ FAÇA:
- ✅ Backup antes de grandes mudanças
- ✅ Verifique o tamanho regularmente
- ✅ Mantenha o .gitignore atualizado
- ✅ Teste restauração de backups

### ❌ NÃO FAÇA:
- ❌ Editar index.faiss ou index.pkl manualmente
- ❌ Copiar índices entre projetos diferentes
- ❌ Misturar embeddings de modelos diferentes
- ❌ Commitar arquivos grandes no Git

## 📈 TAMANHO ESPERADO

```
┌────────────────────────────────────────────┐
│  Documentos    │  Chunks   │  Tamanho      │
├────────────────────────────────────────────┤
│  1 arquivo     │  ~50      │  ~50 KB       │
│  10 arquivos   │  ~500     │  ~500 KB      │
│  100 arquivos  │  ~5.000   │  ~5 MB        │
│  1.000 arquivos│  ~50.000  │  ~50 MB       │
└────────────────────────────────────────────┘
```

## 🎯 RESUMO

```
╔════════════════════════════════════════════════╗
║  🎉 SEUS DADOS ESTÃO SEGUROS E VISÍVEIS!      ║
╠════════════════════════════════════════════════╣
║                                                ║
║  📂 Localização: ./data/faiss_index/          ║
║  💾 Persistência: PERMANENTE                   ║
║  👁️ Visibilidade: TOTAL                       ║
║  🔄 Backup: FÁCIL (copiar pasta)              ║
║  🗑️ Limpeza: SIMPLES (deletar arquivos)      ║
║                                                ║
╚════════════════════════════════════════════════╝
```

## 🆘 PROBLEMAS COMUNS

### "Não encontro os arquivos"
```
Solução: Verifique se está na pasta correta do projeto
         Use: cd caminho/do/projeto
         Depois: ls ./data/faiss_index/
```

### "Dados desapareceram após reiniciar"
```
Solução: Isso NÃO deveria acontecer!
         1. Verifique se os arquivos existem em ./data/faiss_index/
         2. Verifique o docker-compose.yml (deve usar ./data)
         3. Se usar volumes nomeados, migre para pastas locais
```

### "Índice muito grande"
```
Solução: 
         1. Faça backup do índice atual
         2. Limpe com: Remove-Item ./data/faiss_index/index.*
         3. Reindexe apenas documentos necessários
```

### "Erro ao carregar índice"
```
Solução:
         1. Índice pode estar corrompido
         2. Restaure backup: Copy-Item backup/* ./data/faiss_index/
         3. Ou reindexe os documentos
```

---

📅 **Última atualização:** 10/12/2025  
🔖 **Versão:** 1.0  
📧 **Suporte:** [seu-email@exemplo.com]
