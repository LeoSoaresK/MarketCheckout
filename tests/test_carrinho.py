import pytest

from src.carrinho import (
    calcular_total, adicionar_item, remover_item, aplicar_desconto,
    processar_pagamento, limpar_carrinho, gerar_recibo, buscar_item,
    consultar_estoque, baixar_estoque, repor_estoque
)

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

def test_pagamento_exato_retorna_troco_zero():
    assert processar_pagamento(50.0, 50.0) == 0.0

def test_pagamento_com_dinheiro_a_mais_retorna_troco_correto():
    assert processar_pagamento(50.0, 70.0) == 20.0

def test_pagamento_com_valor_insuficiente_lanca_erro():
    with pytest.raises(ValueError, match="Valor insuficiente para pagamento"):
        processar_pagamento(50.0, 40.0)

def test_pagamento_com_valor_negativo_lanca_erro():
    with pytest.raises(ValueError, match="O valor pago não pode ser negativo"):
        processar_pagamento(50.0, -10.0)

def test_limpar_carrinho_com_itens():
    carrinho = [{"nome": "La-Yu Chili Oil", "preco": 20.0, "quantidade": 2}]
    atualizado = limpar_carrinho(carrinho)
    assert len(atualizado) == 0

def test_limpar_carrinho_ja_vazio():
    carrinho = []
    atualizado = limpar_carrinho(carrinho)
    assert len(atualizado) == 0

def test_buscar_item_existente_no_carrinho():
    carrinho = [
        {"nome": "Crunchy Garlic S&B", "preco": 35.0, "quantidade": 1},
        {"nome": "Arroz", "preco": 25.0, "quantidade": 2}
    ]
    item = buscar_item(carrinho, "Crunchy Garlic S&B")
    assert item is not None
    assert item["preco"] == 35.0

def test_buscar_item_inexistente_retorna_none():
    carrinho = [{"nome": "Arroz", "preco": 25.0, "quantidade": 2}]
    item = buscar_item(carrinho, "Feijão")
    assert item is None

def test_gerar_recibo_carrinho_vazio():
    carrinho = []
    assert gerar_recibo(carrinho) == "Carrinho vazio"

def test_gerar_recibo_lista_nomes_dos_produtos():
    carrinho = [
        {"nome": "Crunchy Garlic S&B", "preco": 35.0, "quantidade": 1},
        {"nome": "La-Yu Chili Oil", "preco": 20.0, "quantidade": 1}
    ]
    recibo = gerar_recibo(carrinho)
    assert "Crunchy Garlic S&B" in recibo
    assert "La-Yu Chili Oil" in recibo

def test_consultar_estoque_produto_existente():
    estoque = {"Whey Protein Isolado": 5}
    assert consultar_estoque(estoque, "Whey Protein Isolado") == 5

def test_consultar_estoque_produto_inexistente_retorna_zero():
    estoque = {"Whey Protein Isolado": 5}
    assert consultar_estoque(estoque, "Corda de Guitarra 0.9") == 0

def test_baixar_estoque_com_sucesso():
    estoque = {"Whey Protein Isolado": 10}
    baixar_estoque(estoque, "Whey Protein Isolado", 2)
    assert estoque["Whey Protein Isolado"] == 8

def test_baixar_estoque_quantidade_exata_zera_produto():
    estoque = {"Corda de Guitarra 0.9": 3}
    baixar_estoque(estoque, "Corda de Guitarra 0.9", 3)
    assert estoque["Corda de Guitarra 0.9"] == 0

def test_baixar_estoque_insuficiente_lanca_erro():
    estoque = {"Whey Protein Isolado": 2}
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        baixar_estoque(estoque, "Whey Protein Isolado", 5)

def test_baixar_estoque_produto_inexistente_lanca_erro():
    estoque = {"Corda de Guitarra 0.9": 5}
    with pytest.raises(KeyError, match="Produto não cadastrado no estoque"):
        baixar_estoque(estoque, "Toldo Náutico", 1)

def test_baixar_estoque_quantidade_negativa_lanca_erro():
    estoque = {"Whey Protein Isolado": 5}
    with pytest.raises(ValueError, match="Quantidade a baixar deve ser maior que zero"):
        baixar_estoque(estoque, "Whey Protein Isolado", -1)

def test_repor_estoque_produto_existente():
    estoque = {"Corda de Guitarra 0.9": 2}
    repor_estoque(estoque, "Corda de Guitarra 0.9", 3)
    assert estoque["Corda de Guitarra 0.9"] == 5

def test_repor_estoque_novo_produto():
    estoque = {}
    repor_estoque(estoque, "Transformador de Voltagem", 10)
    assert estoque["Transformador de Voltagem"] == 10

def test_repor_estoque_quantidade_negativa_lanca_erro():
    estoque = {"Corda de Guitarra 0.9": 5}
    with pytest.raises(ValueError, match="Quantidade a repor deve ser maior que zero"):
        repor_estoque(estoque, "Corda de Guitarra 0.9", -2)