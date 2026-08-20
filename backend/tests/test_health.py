def test_root_returns_status_online(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "GameHub backend online"}


def test_head_root_returns_200(client):
    response = client.head("/")

    assert response.status_code == 200
