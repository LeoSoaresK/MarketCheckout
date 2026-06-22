import pytest
from src.carrinho import (
    calcular_total, adicionar_item, remover_item, aplicar_desconto,
    processar_pagamento, limpar_carrinho, gerar_recibo,
    consultar_estoque, baixar_estoque, repor_estoque
)

def test_fluxo_compra_completa_com_sucesso():
    carrinho = []
    estoque = {"Arroz": 10, "Feijão": 5}
    
    carrinho = adicionar_item(carrinho, {"nome": "Arroz", "preco": 20.0, "quantidade": 2})
    carrinho = adicionar_item(carrinho, {"nome": "Feijão", "preco": 10.0, "quantidade": 1})
    
    baixar_estoque(estoque, "Arroz", 2)
    baixar_estoque(estoque, "Feijão", 1)
    
    total = calcular_total(carrinho)
    assert total == 50.0
    
    troco = processar_pagamento(total, 50.0)
    assert troco == 0.0
    
    assert consultar_estoque(estoque, "Arroz") == 8
    assert consultar_estoque(estoque, "Feijão") == 4

def test_fluxo_compra_com_desconto_e_troco():
    carrinho = []
    carrinho = adicionar_item(carrinho, {"nome": "Azeite Extra Virgem", "preco": 40.0, "quantidade": 1})
    
    # Calcula total inicial
    total_inicial = calcular_total(carrinho)
    
    total_com_desconto = aplicar_desconto(total_inicial, 10)
    assert total_com_desconto == 36.0
    
    troco = processar_pagamento(total_com_desconto, 50.0)
    assert troco == 14.0

def test_fluxo_tentativa_de_compra_com_estoque_insuficiente():
    carrinho = []
    estoque = {"Leite Integral": 2}
    
    item_desejado = {"nome": "Leite Integral", "preco": 5.50, "quantidade": 3}
    
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        if consultar_estoque(estoque, item_desejado["nome"]) < item_desejado["quantidade"]:
            baixar_estoque(estoque, item_desejado["nome"], item_desejado["quantidade"])
            
    carrinho = limpar_carrinho(carrinho)
    assert len(carrinho) == 0
    assert consultar_estoque(estoque, "Leite Integral") == 2

def test_fluxo_desistencia_de_item_no_caixa():
    carrinho = []
    
    carrinho = adicionar_item(carrinho, {"nome": "Sabão em Pó", "preco": 15.0, "quantidade": 2})
    carrinho = adicionar_item(carrinho, {"nome": "Biscoito", "preco": 4.50, "quantidade": 1})
    
    carrinho = remover_item(carrinho, "Biscoito")
    
    total_final = calcular_total(carrinho)
    assert total_final == 30.0
    
    recibo = gerar_recibo(carrinho)
    assert "Sabão em Pó" in recibo
    assert "Biscoito" not in recibo

def test_fluxo_fechamento_de_caixa_e_impressao_de_recibo():
    carrinho = []
    carrinho = adicionar_item(carrinho, {"nome": "Chocolate Amargo", "preco": 8.0, "quantidade": 1})
    
    total = calcular_total(carrinho)
    processar_pagamento(total, 10.0)
    
    recibo = gerar_recibo(carrinho)
    
    assert "--- RECIBO ---" in recibo
    assert "1x Chocolate Amargo - R$ 8.0" in recibo
    
    carrinho = limpar_carrinho(carrinho)
    assert len(carrinho) == 0