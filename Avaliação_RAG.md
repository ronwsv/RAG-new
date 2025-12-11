Para testar melhor o seu RAG de condomínio, monte um “plano de prova de fogo” com casos reais de uso (perguntas típicas de moradores/síndico) + métricas simples de qualidade (se recuperou o documento certo, se a resposta está fiel e completa).  Assim você valida tanto a recuperação quanto a geração e descobre onde ajustar embedding, chunking, prompt e filtros.[1][2][3][4][5]

## 1. Definir cenários reais do condomínio  
Comece listando os tipos de perguntas que o chat precisa responder bem.[2][4]
- Perguntas factuais diretas: “Pode fazer festa no salão até que horas?”, “Qual é a multa por barulho depois das 22h?”.  
- Perguntas de exceção/edge cases: “E se a festa for no Ano Novo?”, “Visitante pode usar vaga de garagem?”.  
- Perguntas ambíguas ou mal formuladas: “Pode som alto à noite?”, “Posso alugar meu apê no Airbnb?”.  

Para cada pergunta, registre também: resposta correta (texto curto, na sua visão de ‘gabarito’) e de qual documento/artigo essa resposta deveria vir (regulamento, convenção, ata X).[4][5]

## 2. Testar recuperação (antes da resposta)  
Você, como dev, deveria olhar primeiro se o RAG está trazendo o contexto certo.[3][5]
- Logue para cada pergunta:  
  - Quais chunks/documentos foram retornados.  
  - De qual documento (regulamento, convenção, etc) e qual artigo/seção.  
- Marque manualmente:  
  - “Relevante” ou “não relevante” para cada contexto.  
  - Se há pelo menos um trecho que contém a resposta correta (isso é um “recall” mínimo).[5][3]

Se frequentemente não aparece nenhum trecho com a resposta correta, ajuste: tamanho do chunk, janela de contexto, tipo de embedding, quantidade de documentos retornados (top_k).[2][4]

## 3. Testar a resposta gerada (fidelidade e utilidade)  
Agora olhe a saída final do chat em cima desses mesmos casos de teste.[5][2]
Para cada pergunta, avalie com notas simples (0/1 ou 0–2):  
- Correção factual: a resposta está de acordo com o regulamento/convenção?  
- Fidelidade às fontes: a resposta só usa o que está nos documentos, sem “inventar regras”?[6][3][5]
- Completude: respondeu tudo que o morador precisa saber (condições, exceções importantes)?[2][5]

Guarde isso numa planilha (pergunta → documentos recuperados → resposta → notas). Com 30–50 perguntas já dá para enxergar padrões de erro bem claros.[4][2]

## 4. Criar casos “maliciosos” e de stress  
Monte um bloco só de testes de stress, pensando em condomínio do mundo real.[3][2]
- Perguntas fora do escopo: “Posso fazer financiamento pela Caixa?” → o bot deve dizer que não tem essa informação no regulamento, em vez de chutar.[6][3]
- Conflitos de documento (ex: ata antiga x nova): ver se a resposta menciona que há conflito ou que vale o documento mais recente.[3]
- Perguntas muito longas ou com ruído: “Oi, tudo bem, moro na torre B e queria saber se rola de usar a churrasqueira depois das 23h se for só família, porque já vi vizinho usando, sabe me dizer?”.  

Isso ajuda a ver se o sistema sabe dizer “não sei” ou “não está claro” quando os documentos não sustentam uma resposta segura.[6][3]

## 5. Usar um “LLM juiz” automático (opcional, mas forte)  
Você pode automatizar parte da avaliação usando o próprio modelo como juiz, tipo pipeline interno:[7][3][6]
- Depois da resposta, passe para outro passo:  
  - Entrada: pergunta + documentos recuperados + resposta gerada.  
  - Tarefa: “Verificar se a resposta está totalmente baseada nos documentos, apontar qualquer trecho que não esteja nas fontes ou contradiga os textos.”[3][6]
- Use isso para marcar automaticamente possíveis alucinações ou omissões graves.[7][3]

Para produção, esse juiz pode rodar só em perguntas de maior risco (ex: multas, processos, uso indevido de áreas).[7][3]

## 6. Boas práticas específicas para condomínio  
Adaptando as métricas gerais ao seu caso:[8][5][2]
- Sempre citar a fonte na resposta: “Conforme Regulamento Interno, art. X…” → isso força o modelo a se apoiar nos documentos.[9][8]
- Prompt de sistema bem restritivo:  
  - Responder apenas com base nos documentos do condomínio.  
  - Se a informação não estiver em nenhum documento, dizer explicitamente que não consta.[9][6]
- Diferenciar “informação jurídica” x “orientação prática”: em coisas mais sensíveis (por ex. discussões de assembleia, direito de vizinhança), incentive respostas conservadoras (“consulte o síndico ou administradora”).[10][8]

Se quiser, no próximo passo dá para desenhar juntos:  
- Um formato de planilha de testes (colunas) para você alimentar com as perguntas do condomínio.  
- Um mini-script (Python ou JS) que rode sua suíte de perguntas contra a API do seu RAG e gere estatísticas básicas (acurácia, recall de contexto, etc.).
