# MarketCheckout

[![CI Pipeline de Testes](https://github.com/LeoSoaresK/MarketCheckout/actions/workflows/ci.yml/badge.svg)](https://github.com/LeoSoaresK/MarketCheckout/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/LeoSoaresK/MarketCheckout/branch/main/graph/badge.svg)](https://codecov.io/gh/LeoSoaresK/MarketCheckout)

## Integrantes

- Léo Soares de Oliveira Júnior
- Matheus Guimarães Couto de Melo Afonso

## Sobre o sistema

O MarketCheckout é um sistema de ponto de caixa (PDV) simplificado para um mercado. Ele permite adicionar produtos a um carrinho, remover itens, aplicar descontos percentuais, controlar o estoque disponível (incluindo reposição), processar o pagamento com cálculo de troco e gerar o recibo da compra. A interface web expõe essas operações através de uma página única que reage às ações do usuário (adicionar, remover, aplicar desconto, repor estoque, pagar e cancelar a compra).

## Tecnologias utilizadas

- **Python 3.11**
- **Flask** — servidor web e rotas da aplicação (`app.py`)
- **HTML/CSS/Jinja2** — interface (`templates/`, `static/`)
- **pytest** — testes unitários e de integração
- **pytest-cov** — relatório de cobertura de testes
- **GitHub Actions** — pipeline de CI (executa os testes em Ubuntu, macOS e Windows)
- **Codecov** — publicação do relatório de cobertura

## Como executar os testes localmente

1. Instale as dependências:
   ```
   pip install -r requirements.txt pytest pytest-cov
   ```
2. Execute a suíte de testes a partir da raiz do projeto:
   ```
   python -m pytest
   ```
3. (Opcional) Para gerar o relatório de cobertura:
   ```
   python -m pytest --cov=src --cov-report=term-missing
   ```
