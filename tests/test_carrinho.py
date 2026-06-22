from src.carrinho import calcular_total
import pytest

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