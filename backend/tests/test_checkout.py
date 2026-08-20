import main

PAYLOAD_VALIDO = {
    "metodo_pagamento": "pix",
    "itens": [{"title": "Elden Ring", "price": 99.9}],
}


def test_checkout_sem_header_authorization_retorna_401(client):
    response = client.post("/checkout", json=PAYLOAD_VALIDO)

    assert response.status_code == 401


def test_checkout_com_header_mal_formado_retorna_401(client):
    response = client.post(
        "/checkout",
        json=PAYLOAD_VALIDO,
        headers={"Authorization": "Token abc123"},
    )

    assert response.status_code == 401


def test_checkout_com_token_invalido_retorna_401(client, monkeypatch, fake_auth_response):
    monkeypatch.setattr(main.httpx, "get", lambda *a, **k: fake_auth_response(401))

    response = client.post(
        "/checkout",
        json=PAYLOAD_VALIDO,
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401


def test_checkout_com_payload_invalido_retorna_422(client, monkeypatch, fake_auth_response):
    monkeypatch.setattr(
        main.httpx, "get", lambda *a, **k: fake_auth_response(200, {"id": "user-1"})
    )

    response = client.post(
        "/checkout",
        json={"metodo_pagamento": "pix", "itens": []},
        headers={"Authorization": "Bearer token-valido"},
    )

    assert response.status_code == 422


def test_checkout_com_sucesso_cria_pedido(client, monkeypatch, fake_auth_response, fake_supabase):
    monkeypatch.setattr(
        main.httpx, "get", lambda *a, **k: fake_auth_response(200, {"id": "user-1"})
    )
    monkeypatch.setattr(main, "supabase", fake_supabase([{"id": 42}]))

    response = client.post(
        "/checkout",
        json=PAYLOAD_VALIDO,
        headers={"Authorization": "Bearer token-valido"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["pedido_id"] == 42


def test_checkout_quando_insert_falha_retorna_erro_tratado(client, monkeypatch, fake_auth_response, fake_supabase):
    monkeypatch.setattr(
        main.httpx, "get", lambda *a, **k: fake_auth_response(200, {"id": "user-1"})
    )
    monkeypatch.setattr(main, "supabase", fake_supabase([]))

    response = client.post(
        "/checkout",
        json=PAYLOAD_VALIDO,
        headers={"Authorization": "Bearer token-valido"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
