def calcular_total(carrinho):
    total = 0.0
    for item in carrinho:
        total += item["preco"] * item["quantidade"]
    return total