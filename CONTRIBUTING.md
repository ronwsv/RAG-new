# Contribuindo para RAG Simple

Obrigado por considerar contribuir para o RAG Simple! Este documento fornece diretrizes e instruções para contribuir ao projeto.

## 🤝 Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug, verifique o histórico de issues, pois o problema pode já ter sido informado. Se encontrar um bug que não foi reportado, abra uma nova issue fornecendo as seguintes informações:

- **Use um título claro e descritivo**
- **Descreva os passos exatos para reproduzir o problema**
- **Forneça exemplos específicos para demonstrar as etapas**
- **Descreva o comportamento observado e aponte qual é o problema**
- **Explique qual comportamento você esperava ver**
- **Inclua logs ou screenshots se possível**
- **Sua configuração**: SO, versão do Python, versão do Docker, etc.

### Sugerindo Melhorias

Sugestões de melhorias são sempre bem-vindas! Ao criar uma sugestão de melhoria, forneça:

- **Use um título claro e descritivo** para a sugestão
- **Forneça uma descrição detalhada** da melhoria sugerida
- **Descreva o comportamento atual** e cite alguns exemplos
- **Descreva o comportamento esperado** e cite alguns exemplos
- **Explique por que essa melhoria seria útil** para a maioria dos usuários

## 🔧 Processo de Desenvolvimento

### Setup Local

1. **Fork o repositório**
   ```bash
   git clone https://github.com/SEU_USERNAME/RAG-new.git
   cd RAG-new
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate   # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8  # Dev dependencies
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite .env com suas chaves API
   ```

5. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/sua-feature-incrivel
   ```

### Desenvolvendo

- Siga o estilo de código do projeto
- Use type hints quando possível
- Mantenha o código limpo e legível
- Adicione comentários para lógica complexa

### Testando

```bash
# Rodar testes
pytest tests/

# Verificar estilo de código
flake8 src/

# Formatar código
black src/ app.py
```

### Commitando

Use mensagens de commit claras e descritivas:

```bash
git commit -m "Add feature: descrição da feature"
git commit -m "Fix: descrição do bug corrigido"
git commit -m "Docs: atualização de documentação"
```

Formato recomendado:
- `feat:` Nova feature
- `fix:` Correção de bug
- `docs:` Mudanças de documentação
- `style:` Formatação, sem mudança de lógica
- `refactor:` Refatoração sem mudança de comportamento
- `perf:` Melhoria de performance
- `test:` Adição ou modificação de testes

### Push e Pull Request

1. **Push para seu fork**
   ```bash
   git push origin feature/sua-feature-incrivel
   ```

2. **Crie um Pull Request**
   - Use um título claro e descritivo
   - Descreva as mudanças realizadas
   - Referencie issues relacionadas (#123)
   - Se houver mudanças visuais, inclua screenshots

## 📋 Checklist para Pull Request

- [ ] Código segue o estilo do projeto
- [ ] Testes foram adicionados/modificados
- [ ] Testes passam localmente
- [ ] Documentação foi atualizada
- [ ] Nenhuma quebra de mudança foi introduzida
- [ ] Commit messages são claras e descritivas

## 🎯 Áreas para Contribuir

### Alto Impacto
- Suporte para mais formatos de documento (HTML, CSV, JSON)
- Novos provedores de LLM (Groq, Gemini, etc.)
- Sistema de histórico de conversação
- API REST

### Médio Impacto
- Dashboard de analytics
- Sistema de tags e categorias
- Melhorias na interface
- Performance optimizations

### Baixo Impacto
- Correções de typos
- Melhorias de documentação
- Testes unitários adicionais
- Exemplos de código

## 📚 Recursos Úteis

- [LangChain Documentation](https://python.langchain.com/docs/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Gradio Docs](https://www.gradio.app/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 💬 Comunidade

- Issues para bugs e features
- Discussions para perguntas e ideias
- Wikis para documentação comunitária

## 📝 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.

---

**Obrigado por contribuir! 🎉**
