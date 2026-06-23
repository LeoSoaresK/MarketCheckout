from flask import Flask, render_template, request, redirect, url_for, flash
import secrets
from src.carrinho import calcular_total, adicionar_item, remover_item, limpar_carrinho, processar_pagamento

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

@app.route('/')
def index():
    total = calcular_total(carrinho_atual)
    return render_template('index.html', produtos=PRODUTOS_MERCADO, carrinho=carrinho_atual, total=total)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    preco = float(request.form.get('preco'))
    adicionar_item(carrinho_atual, {"nome": nome, "preco": preco, "quantidade": 1})
    return redirect(url_for('index'))

@app.route('/remover', methods=['POST'])
def remover():
    nome = request.form.get('nome')
    try:
        remover_item(carrinho_atual, nome)
    except KeyError as e:
        flash(str(e), "erro")
    return redirect(url_for('index'))

@app.route('/pagar', methods=['POST'])
def pagar():
    valor_pago_str = request.form.get('valor_pago')
    if not valor_pago_str:
        flash("Por favor, informe o valor pago.", "erro")
        return redirect(url_for('index'))
    
    valor_pago = float(valor_pago_str)
    total = calcular_total(carrinho_atual)
    
    try:
        # Usa a função do nosso TDD!
        troco = processar_pagamento(total, valor_pago)
        limpar_carrinho(carrinho_atual)
        flash(f"Compra finalizada com sucesso! Troco: R$ {troco:.2f}", "sucesso")
    except ValueError as e:
        # Captura os erros que programamos (ex: valor negativo, insuficiente)
        flash(str(e), "erro")
        
    return redirect(url_for('index'))

@app.route('/limpar', methods=['POST'])
def limpar():
    limpar_carrinho(carrinho_atual)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)