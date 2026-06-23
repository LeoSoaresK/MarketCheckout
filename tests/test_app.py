import pytest
import app as app_module


@pytest.fixture(autouse=True)
def resetar_estado_global():
    app_module.carrinho_atual.clear()
    app_module.desconto_atual = 0.0
    app_module.ultimo_recibo = None
    app_module.estoque_atual = {
        "Arroz 5kg": 10,
        "Feijão 1kg": 10,
        "Crunchy Garlic S&B": 5,
        "Kit Pratos 12 Peças": 3,
        "Corda de Guitarra 0.9": 8
    }


@pytest.fixture
def client():
    return app_module.app.test_client()


def test_index_retorna_200(client):
    resposta = client.get('/')
    assert resposta.status_code == 200


def test_adicionar_item_com_estoque_disponivel(client):
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})
    assert app_module.carrinho_atual[0]['nome'] == 'Arroz 5kg'
    assert app_module.carrinho_atual[0]['quantidade'] == 1


def test_adicionar_item_acima_do_estoque_e_bloqueado(client):
    for _ in range(3):
        client.post('/adicionar', data={'nome': 'Kit Pratos 12 Peças', 'preco': '120.0'})

    resposta = client.post('/adicionar', data={'nome': 'Kit Pratos 12 Peças', 'preco': '120.0'}, follow_redirects=True)

    assert app_module.carrinho_atual[0]['quantidade'] == 3
    assert "Estoque insuficiente" in resposta.get_data(as_text=True)


def test_pagar_baixa_estoque_dos_itens_comprados(client):
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})

    client.post('/pagar', data={'valor_pago': '50.0'})

    assert app_module.estoque_atual['Arroz 5kg'] == 8
    assert app_module.carrinho_atual == []


def test_remover_item_existente_no_carrinho(client):
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})

    client.post('/remover', data={'nome': 'Arroz 5kg'})

    assert app_module.carrinho_atual == []


def test_remover_item_inexistente_mostra_erro(client):
    resposta = client.post('/remover', data={'nome': 'Arroz 5kg'}, follow_redirects=True)

    assert "Item nao encontrado" in resposta.get_data(as_text=True)


def test_desconto_valido_e_aplicado(client):
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})

    client.post('/desconto', data={'percentual': '10'})

    assert app_module.desconto_atual == 10.0


def test_desconto_invalido_mostra_erro(client):
    client.post('/adicionar', data={'nome': 'Arroz 5kg', 'preco': '25.0'})

    resposta = client.post('/desconto', data={'percentual': '150'}, follow_redirects=True)

    assert app_module.desconto_atual == 0.0
    assert "Desconto deve ser entre 0 e 100" in resposta.get_data(as_text=True)
