name: Feature Request
description: Solicitar uma nova feature ou melhoria
title: "[FEATURE] "
labels: ["enhancement"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Obrigado por sua sugestão! Descreva sua ideia abaixo.

  - type: textarea
    id: description
    attributes:
      label: Descrição da Feature
      description: Descreva claramente qual é sua sugestão
      placeholder: "Gostaria de adicionar..."
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problema que Resolve
      description: Qual problema essa feature resolve?
      placeholder: "Atualmente, é difícil... porque..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Solução Proposta
      description: Como você gostaria que funcione?
      placeholder: "Deveria funcionar assim..."
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternativas Consideradas
      description: Existem outras formas de resolver isso?
      placeholder: "Outras possibilidades..."
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: Prioridade
      options:
        - Baixa
        - Média
        - Alta
        - Crítica
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Busquei em issues existentes
          required: true
        - label: Isso não é um duplicate
          required: true
