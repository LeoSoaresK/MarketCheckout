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