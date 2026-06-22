import pytest
from src.carrinho import (
    calcular_total, adicionar_item, remover_item, aplicar_desconto,
    processar_pagamento, limpar_carrinho, gerar_recibo,
    consultar_estoque, baixar_estoque, repor_estoque
)

def test_fluxo_compra_completa_com_sucesso():
    """Cenário 1: Cliente passa dois produtos no caixa, o estoque atualiza, 
    o total é calculado e o pagamento é feito sem troco."""
    carrinho = []
    estoque = {"Arroz": 10, "Feijão": 5}
    
    # 1. Cliente adiciona os produtos ao carrinho
    carrinho = adicionar_item(carrinho, {"nome": "Arroz", "preco": 20.0, "quantidade": 2})
    carrinho = adicionar_item(carrinho, {"nome": "Feijão", "preco": 10.0, "quantidade": 1})
    
    # 2. O sistema valida e baixa a quantidade do estoque
    baixar_estoque(estoque, "Arroz", 2)
    baixar_estoque(estoque, "Feijão", 1)
    
    # 3. Caixa calcula o total da compra (2x20 + 1x10 = 50)
    total = calcular_total(carrinho)
    assert total == 50.0
    
    # 4. Cliente paga o valor exato em dinheiro
    troco = processar_pagamento(total, 50.0)
    assert troco == 0.0
    
    # 5. Verifica se o estoque refletiu a venda corretamente
    assert consultar_estoque(estoque, "Arroz") == 8
    assert consultar_estoque(estoque, "Feijão") == 4

def test_fluxo_compra_com_desconto_e_troco():
    """Cenário 2: Compra de um item de valor alto, aplicação de cupom de desconto 
    e pagamento com dinheiro gerando troco."""
    carrinho = []
    carrinho = adicionar_item(carrinho, {"nome": "Azeite Extra Virgem", "preco": 40.0, "quantidade": 1})
    
    # Calcula total inicial
    total_inicial = calcular_total(carrinho)
    
    # Aplica um cupom de 10% de desconto (40.0 - 10% = 36.0)
    total_com_desconto = aplicar_desconto(total_inicial, 10)
    assert total_com_desconto == 36.0
    
    # Cliente paga com uma nota de R$ 50.00
    troco = processar_pagamento(total_com_desconto, 50.0)
    assert troco == 14.0