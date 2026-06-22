from flask import Flask, render_template, request, redirect, url_for
from src.carrinho import calcular_total, adicionar_item, limpar_carrinho

app = Flask(__name__)

PRODUTOS_MERCADO = [
    {"nome": "Arroz", "preco": 20.0},
    {"nome": "Feijão", "preco": 10.0},
    {"nome": "Chocolate Amargo", "preco": 8.0},
    {"nome": "La-Yu Chili Oil", "preco": 20.0},
    {"nome": "Whey Protein Isolado", "preco": 90.0}
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

@app.route('/limpar', methods=['POST'])
def limpar():
    limpar_carrinho(carrinho_atual)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)