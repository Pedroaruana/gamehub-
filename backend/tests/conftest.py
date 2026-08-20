from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


class FakeAuthResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json


@pytest.fixture
def fake_auth_response():
    return FakeAuthResponse


@pytest.fixture
def fake_supabase():
    def _build(pedidos_data):
        mock = MagicMock()

        def table_side_effect(name):
            table_mock = MagicMock()
            data = pedidos_data if name == "pedidos" else []
            table_mock.insert.return_value.execute.return_value = MagicMock(data=data)
            return table_mock

        mock.table.side_effect = table_side_effect
        return mock

    return _build
