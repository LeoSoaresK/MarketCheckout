def calcular_total(carrinho):
    total = 0.0
    for item in carrinho:
        if item["quantidade"] < 0:
            raise ValueError("A quantidade nao pode ser negativa")
        total += item["preco"] * item["quantidade"]
    return total