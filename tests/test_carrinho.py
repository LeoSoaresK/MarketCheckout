from src.carrinho import calcular_total

def test_calcular_total_carrinho_vazio():
    carrinho = []
    resultado = calcular_total(carrinho)
    assert resultado == 0.0