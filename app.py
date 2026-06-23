from flask import Flask, render_template, request, redirect, url_for, flash
import secrets
from src.carrinho import calcular_total, adicionar_item, remover_item, aplicar_desconto, limpar_carrinho, processar_pagamento, gerar_recibo, consultar_estoque

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

PRODUTOS_MERCADO = [
    {"nome": "Arroz 5kg", "preco": 25.0},
    {"nome": "Feijão 1kg", "preco": 10.0},
    {"nome": "Crunchy Garlic S&B", "preco": 35.0},
    {"nome": "Kit Pratos 12 Peças", "preco": 120.0},
    {"nome": "Corda de Guitarra 0.9", "preco": 45.0}
]

carrinho_atual = []
desconto_atual = 0.0
ultimo_recibo = None
estoque_atual = {
    "Arroz 5kg": 10,
    "Feijão 1kg": 10,
    "Crunchy Garlic S&B": 5,
    "Kit Pratos 12 Peças": 3,
    "Corda de Guitarra 0.9": 8
}

@app.route('/')
def index():
    subtotal = calcular_total(carrinho_atual)
    total = aplicar_desconto(subtotal, desconto_atual)
    produtos_com_estoque = [
        {**produto, "estoque": consultar_estoque(estoque_atual, produto["nome"])}
        for produto in PRODUTOS_MERCADO
    ]
    return render_template(
        'index.html', produtos=produtos_com_estoque, carrinho=carrinho_atual,
        subtotal=subtotal, desconto=desconto_atual, total=total, recibo=ultimo_recibo
    )

@app.route('/adicionar', methods=['POST'])
def adicionar():
    global ultimo_recibo
    nome = request.form.get('nome')
    preco = float(request.form.get('preco'))
    adicionar_item(carrinho_atual, {"nome": nome, "preco": preco, "quantidade": 1})
    ultimo_recibo = None
    return redirect(url_for('index'))

@app.route('/remover', methods=['POST'])
def remover():
    nome = request.form.get('nome')
    try:
        remover_item(carrinho_atual, nome)
    except KeyError as e:
        flash(str(e), "erro")
    return redirect(url_for('index'))

@app.route('/desconto', methods=['POST'])
def desconto():
    global desconto_atual
    percentual_str = request.form.get('percentual')
    try:
        percentual = float(percentual_str)
        aplicar_desconto(100.0, percentual)  # valida o percentual antes de gravar
        desconto_atual = percentual
        flash(f"Desconto de {percentual:.0f}% aplicado!", "sucesso")
    except (TypeError, ValueError) as e:
        flash(str(e) or "Percentual de desconto inválido.", "erro")
    return redirect(url_for('index'))

@app.route('/pagar', methods=['POST'])
def pagar():
    global desconto_atual, ultimo_recibo
    valor_pago_str = request.form.get('valor_pago')
    if not valor_pago_str:
        flash("Por favor, informe o valor pago.", "erro")
        return redirect(url_for('index'))

    valor_pago = float(valor_pago_str)
    subtotal = calcular_total(carrinho_atual)
    total = aplicar_desconto(subtotal, desconto_atual)

    try:
        # Usa a função do nosso TDD!
        troco = processar_pagamento(total, valor_pago)
        ultimo_recibo = gerar_recibo(carrinho_atual)
        limpar_carrinho(carrinho_atual)
        desconto_atual = 0.0
        flash(f"Compra finalizada com sucesso! Troco: R$ {troco:.2f}", "sucesso")
    except ValueError as e:
        # Captura os erros que programamos (ex: valor negativo, insuficiente)
        flash(str(e), "erro")

    return redirect(url_for('index'))

@app.route('/limpar', methods=['POST'])
def limpar():
    global desconto_atual, ultimo_recibo
    limpar_carrinho(carrinho_atual)
    desconto_atual = 0.0
    ultimo_recibo = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)