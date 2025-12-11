# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-12-11

### Adicionado

- ✨ Sistema RAG completo com suporte a múltiplos documentos
- ✨ Interface web interativa usando Gradio
- ✨ Suporte para múltiplos formatos: PDF, DOCX, XLSX, TXT, MD
- ✨ Integração com OpenAI (GPT-4o) e Anthropic (Claude Sonnet)
- ✨ Vector Store usando FAISS para busca semântica rápida
- ✨ Formato TOON para economia de tokens (30-60%)
- ✨ Persistência automática de dados em pastas locais
- ✨ Rastreamento preciso de fontes e metadados
- ✨ Docker e Docker Compose para deploy fácil
- ✨ Sistema de contextos para múltiplas bases de documentos (cond_169, etc.)
- ✨ Metadados JSON para cada contexto
- ✨ Gerenciador de contextos com CRUD completo

### Funcionalidades Principais

#### Core RAG
- Carregamento e processamento de documentos
- Divisão inteligente de texto (chunking)
- Geração de embeddings com OpenAI
- Índice vetorial persistente com FAISS
- Pipeline RAG com múltiplos LLMs

#### Interface
- Upload de múltiplos documentos
- Seleção de LLM em tempo real
- Busca com rastreamento de fontes
- Status do sistema em tempo real
- Suporte a dark/light mode

#### Sistema de Contextos
- Criar novos contextos (cond_169, cond_170, etc.)
- Carregar/trocar contextos facilmente
- Índices independentes por contexto
- Metadados persistentes por contexto
- Deletar contextos com segurança

#### Infraestrutura
- Containerização Docker completa
- Health checks implementados
- Volumes persistentes configurados
- Arquivo .env para variáveis sensíveis
- Configuração centralizada em TOML

### Documentação

- README.md com guia completo
- GUIA_DADOS.md com instruções visuais
- PERSISTENCIA_DADOS.md com detalhes técnicos
- ANALISE_PROJETO.md com visão geral
- CONTRIBUTING.md com diretrizes
- Licença MIT

### Testes

- Testes básicos de RAG implementados
- Script de teste de chaves API
- Validação de formatos de documento

---

## Próximas Versões (Roadmap)

### [1.1.0] - Planejado

- [ ] Histórico de conversação persistente
- [ ] API REST para integração
- [ ] Dashboard de analytics
- [ ] Sistema de tags e categorias
- [ ] Suporte a mais formatos (HTML, CSV, JSON)
- [ ] Cache de consultas

### [1.2.0] - Planejado

- [ ] Novos provedores de LLM (Groq, Gemini, DeepSeek)
- [ ] Sistema de roles e permissões
- [ ] Webhooks para eventos
- [ ] Exportação de conversas
- [ ] Integração com databases SQL

### [2.0.0] - Planejado

- [ ] Arquitetura de microserviços
- [ ] Sistema de fila de processamento
- [ ] Machine Learning para ranking de documentos
- [ ] Interface mobile responsiva
- [ ] Sistema de plugins

---

## Guia de Versionamento

### Como reportar um problema

Se você encontrar um problema ou bug, por favor abra uma [issue no GitHub](https://github.com/ronwsv/RAG-new/issues).

### Como contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais informações.

### Política de suporte

- **Versão atual**: Suporte completo
- **Versão anterior**: Suporte limitado
- **Versões antigas**: Não suportadas

---

**Última atualização:** 11 de Dezembro de 2025
