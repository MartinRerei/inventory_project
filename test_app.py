from unittest.mock import patch
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    res = client.get("/")
    assert res.status_code == 200

def test_get_inventory(client):
    res = client.get("/inventory")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_single_item(client):
    res = client.get("/inventory/1")
    assert res.status_code == 200
    assert res.get_json()["id"] == 1

@patch("app.fetch_from_openfoodfacts")
def test_create_item_with_mock(mock_fetch, client):
    mock_fetch.return_value = {
        "product_name": "Test Snack",
        "brands": "Test Brand",
        "ingredients_text": "Wheat, Salt"
    }
    res = client.post("/inventory", json={"barcode": "12345", "quantity": 5, "price": 1.99})
    assert res.status_code == 201
    assert res.get_json()["product_name"] == "Test Snack"

def test_patch_item(client):
    res = client.patch("/inventory/1", json={"price": 4.99})
    assert res.status_code == 200
    assert res.get_json()["price"] == 4.99

def test_delete_item(client):
    res = client.delete("/inventory/2")
    assert res.status_code == 200