import pytest
from src.carrinho import calcular_total, adicionar_item, remover_item, aplicar_desconto

def test_calcular_total_carrinho_vazio():
    carrinho = []
    resultado = calcular_total(carrinho)
    assert resultado == 0.0

def test_calcular_total_com_um_item():
    carrinho = [
        {"nome": "Maçã", "preco": 2.50, "quantidade": 1}
    ]
    resultado = calcular_total(carrinho)
    assert resultado == 2.50

def test_calcular_total_com_quantidade_negativa_deve_lancar_erro():
    carrinho = [
        {"nome": "Maçã", "preco": 2.50, "quantidade": -1}
    ]
    with pytest.raises(ValueError, match="A quantidade nao pode ser negativa"):
        calcular_total(carrinho)

def test_adicionar_item_em_carrinho_vazio():
    carrinho = []
    novo_item = {"nome": "Banana", "preco": 3.00, "quantidade": 2}
    atualizado = adicionar_item(carrinho, novo_item)
    assert len(atualizado) == 1
    assert atualizado[0]["nome"] == "Banana"

def test_adicionar_item_existente_soma_quantidade():
    carrinho = [{"nome": "Banana", "preco": 3.00, "quantidade": 2}]
    novo_item = {"nome": "Banana", "preco": 3.00, "quantidade": 3}
    atualizado = adicionar_item(carrinho, novo_item)
    assert len(atualizado) == 1
    assert atualizado[0]["quantidade"] == 5

def test_adicionar_item_com_quantidade_invalida_lanca_erro():
    carrinho = []
    item_invalido = {"nome": "Banana", "preco": 3.00, "quantidade": 0}
    with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
        adicionar_item(carrinho, item_invalido)

def test_remover_item_existente():
    carrinho = [
        {"nome": "Banana", "preco": 3.00, "quantidade": 2}, 
        {"nome": "Uva", "preco": 5.00, "quantidade": 1}
    ]
    atualizado = remover_item(carrinho, "Banana")
    assert len(atualizado) == 1
    assert atualizado[0]["nome"] == "Uva"

def test_remover_item_inexistente_lanca_erro():
    carrinho = [{"nome": "Banana", "preco": 3.00, "quantidade": 2}]
    with pytest.raises(KeyError, match="Item nao encontrado"):
        remover_item(carrinho, "Uva")

def test_aplicar_desconto_percentual_valido():
    assert aplicar_desconto(100.0, 10) == 90.0

def test_aplicar_desconto_invalido_lanca_erro():
    with pytest.raises(ValueError, match="Desconto deve ser entre 0 e 100"):
        aplicar_desconto(100.0, 110)