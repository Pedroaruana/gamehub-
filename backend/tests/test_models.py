import pytest
from pydantic import ValidationError

from main import ItemCarrinho, CheckoutData


def test_item_com_preco_positivo_e_valido():
    item = ItemCarrinho(title="Elden Ring", price=99.9)

    assert item.title == "Elden Ring"
    assert item.price == 99.9


def test_item_preco_zero_e_invalido():
    with pytest.raises(ValidationError):
        ItemCarrinho(title="Elden Ring", price=0)


def test_item_preco_negativo_e_invalido():
    with pytest.raises(ValidationError):
        ItemCarrinho(title="Elden Ring", price=-10)


def test_item_titulo_e_arredondado_para_duas_casas():
    item = ItemCarrinho(title="GTA V", price=59.999)

    assert item.price == 60.0


def test_item_titulo_com_espacos_e_removido():
    item = ItemCarrinho(title="  GTA V  ", price=59.9)

    assert item.title == "GTA V"


def test_item_titulo_vazio_e_invalido():
    with pytest.raises(ValidationError):
        ItemCarrinho(title="   ", price=59.9)


def test_item_titulo_e_truncado_em_200_caracteres():
    item = ItemCarrinho(title="A" * 300, price=10)

    assert len(item.title) == 200


def test_checkout_com_carrinho_vazio_e_invalido():
    with pytest.raises(ValidationError):
        CheckoutData(metodo_pagamento="pix", itens=[])


def test_checkout_com_mais_de_50_itens_e_invalido():
    itens = [{"title": "Jogo", "price": 10} for _ in range(51)]

    with pytest.raises(ValidationError):
        CheckoutData(metodo_pagamento="pix", itens=itens)


def test_checkout_com_metodo_pagamento_invalido():
    with pytest.raises(ValidationError):
        CheckoutData(
            metodo_pagamento="cartao_credito_fake",
            itens=[{"title": "Jogo", "price": 10}],
        )


def test_checkout_valido():
    data = CheckoutData(
        metodo_pagamento="pix",
        itens=[{"title": "Jogo", "price": 10}],
    )

    assert data.metodo_pagamento == "pix"
    assert len(data.itens) == 1
