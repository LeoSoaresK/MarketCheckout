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

def test_fluxo_tentativa_de_compra_com_estoque_insuficiente():
    """Cenário 3: Cliente tenta comprar mais unidades do que o disponível. 
    O sistema barra, o estoque permanece intacto e o carrinho é cancelado."""
    carrinho = []
    estoque = {"Leite Integral": 2}
    
    item_desejado = {"nome": "Leite Integral", "preco": 5.50, "quantidade": 3}
    
    # Integração entre verificação de estoque e tentativa de baixa
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        if consultar_estoque(estoque, item_desejado["nome"]) < item_desejado["quantidade"]:
            baixar_estoque(estoque, item_desejado["nome"], item_desejado["quantidade"])
            
    # Como a operação falhou por falta de estoque, o carrinho é limpo (compra cancelada)
    carrinho = limpar_carrinho(carrinho)
    assert len(carrinho) == 0
    assert consultar_estoque(estoque, "Leite Integral") == 2

def test_fluxo_desistencia_de_item_no_caixa():
    """Cenário 4: Cliente adiciona múltiplos itens, mas desiste de um deles 
    antes de finalizar. O total deve recalcular corretamente apenas para os itens restantes."""
    carrinho = []
    
    carrinho = adicionar_item(carrinho, {"nome": "Sabão em Pó", "preco": 15.0, "quantidade": 2})
    carrinho = adicionar_item(carrinho, {"nome": "Biscoito", "preco": 4.50, "quantidade": 1})
    
    # Cliente desiste do biscoito
    carrinho = remover_item(carrinho, "Biscoito")
    
    # O total deve considerar apenas o Sabão em Pó (2x15 = 30)
    total_final = calcular_total(carrinho)
    assert total_final == 30.0
    
    # Recibo não deve conter o item removido
    recibo = gerar_recibo(carrinho)
    assert "Sabão em Pó" in recibo
    assert "Biscoito" not in recibo

def test_fluxo_fechamento_de_caixa_e_impressao_de_recibo():
    """Cenário 5: Validação da estrutura de texto do recibo gerado após o 
    cálculo do total e esvaziamento correto do carrinho pós-venda."""
    carrinho = []
    carrinho = adicionar_item(carrinho, {"nome": "Chocolate Amargo", "preco": 8.0, "quantidade": 1})
    
    total = calcular_total(carrinho)
    processar_pagamento(total, 10.0)
    
    recibo = gerar_recibo(carrinho)
    
    # O recibo deve conter o cabeçalho e os detalhes de formatação do preço
    assert "--- RECIBO ---" in recibo
    assert "1x Chocolate Amargo - R$ 8.0" in recibo
    
    # Finaliza o atendimento limpando o carrinho para o próximo cliente
    carrinho = limpar_carrinho(carrinho)
    assert len(carrinho) == 0