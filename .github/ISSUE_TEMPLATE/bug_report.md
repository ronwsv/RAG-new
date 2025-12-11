name: Bug Report
description: Reportar um bug encontrado no projeto
title: "[BUG] "
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Obrigado por reportar um bug! Por favor preencha os detalhes abaixo para nos ajudar a resolver.

  - type: textarea
    id: description
    attributes:
      label: Descrição do Bug
      description: Descreva claramente qual é o problema
      placeholder: "O que está acontecendo?"
    validations:
      required: true

  - type: textarea
    id: reproduce
    attributes:
      label: Passos para Reproduzir
      description: Instruções passo a passo para reproduzir o comportamento
      placeholder: |
        1. Vá para '...'
        2. Clique em '...'
        3. Veja o erro
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Comportamento Esperado
      description: Qual comportamento você esperava?
      placeholder: "Deveria fazer..."
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Comportamento Atual
      description: Qual é o comportamento atual?
      placeholder: "Mas está fazendo..."
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Ambiente
      description: Qual é seu ambiente?
      options:
        - Docker (Linux)
        - Docker (Windows)
        - Docker (Mac)
        - Python Local (Windows)
        - Python Local (Linux)
        - Python Local (Mac)
    validations:
      required: true

  - type: textarea
    id: system-info
    attributes:
      label: Informações do Sistema
      description: "Inclua: SO, versão Python, versão Docker, etc."
      placeholder: |
        - OS: [e.g., Windows 11]
        - Python: [e.g., 3.11.0]
        - Docker: [e.g., 24.0.0]
        - Browser: [e.g., Chrome 120]
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: Logs e Screenshots
      description: "Inclua logs relevantes, error messages, ou screenshots"
      placeholder: "Paste log output or error message here"
      render: shell
    validations:
      required: false

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Busquei em issues existentes
          required: true
        - label: Testei com a versão mais recente
          required: true
