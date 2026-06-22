def calcular_total(carrinho):
    total = 0.0
    for item in carrinho:
        if item["quantidade"] < 0:
            raise ValueError("A quantidade nao pode ser negativa")
        total += item["preco"] * item["quantidade"]
    return total

def adicionar_item(carrinho, novo_item):
    if novo_item["quantidade"] <= 0:
        raise ValueError("Quantidade deve ser maior que zero")
        
    for item in carrinho:
        if item["nome"] == novo_item["nome"]:
            item["quantidade"] += novo_item["quantidade"]
            return carrinho
            
    carrinho.append(novo_item)
    return carrinho

def remover_item(carrinho, nome_item):
    for i, item in enumerate(carrinho):
        if item["nome"] == nome_item:
            carrinho.pop(i)
            return carrinho
            
    raise KeyError("Item nao encontrado")

def aplicar_desconto(total, percentual):
    if percentual < 0 or percentual > 100:
        raise ValueError("Desconto deve ser entre 0 e 100")
        
    desconto = total * (percentual / 100)
    return total - desconto

def processar_pagamento(total_compra, valor_pago):
    if valor_pago < 0:
        raise ValueError("O valor pago não pode ser negativo")
    if valor_pago < total_compra:
        raise ValueError("Valor insuficiente para pagamento")
    return valor_pago - total_compra

def limpar_carrinho(carrinho):
    carrinho.clear()
    return carrinho

def buscar_item(carrinho, nome_item):
    for item in carrinho:
        if item["nome"] == nome_item:
            return item
    return None

def gerar_recibo(carrinho):
    if not carrinho:
        return "Carrinho vazio"
    
    linhas_recibo = ["--- RECIBO ---"]
    for item in carrinho:
        linhas_recibo.append(f"{item['quantidade']}x {item['nome']} - R$ {item['preco']}")
    return "\n".join(linhas_recibo)

def consultar_estoque(estoque, produto):
    return estoque.get(produto, 0)

def baixar_estoque(estoque, produto, quantidade):
    if quantidade <= 0:
        raise ValueError("Quantidade a baixar deve ser maior que zero")
    if produto not in estoque:
        raise KeyError("Produto não cadastrado no estoque")
    if estoque[produto] < quantidade:
        raise ValueError("Estoque insuficiente")
    
    estoque[produto] -= quantidade
    return estoque

def repor_estoque(estoque, produto, quantidade):
    if quantidade <= 0:
        raise ValueError("Quantidade a repor deve ser maior que zero")
    
    if produto in estoque:
        estoque[produto] += quantidade
    else:
        estoque[produto] = quantidade
    return estoque