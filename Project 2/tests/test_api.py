import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["currency"] == "INR"

def test_list_products_and_pagination():
    response = client.get("/api/products?page=1&page_size=4")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 4
    assert data["page"] == 1

def test_product_detail_and_not_found():
    # Valid product detail
    response = client.get("/api/products/p1000000-0000-0000-0000-000000000001")
    assert response.status_code == 200
    assert response.json()["name"] == "AuraWave Pro ANC Wireless Headphones"

    # Non-existent product
    bad_res = client.get("/api/products/non-existent-product-id")
    assert bad_res.status_code == 404

def test_categories_listing():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert len(response.json()) >= 4

def test_unauthenticated_cart_access():
    # Attempting to access cart without auth token should return 401
    response = client.get("/api/cart")
    assert response.status_code == 401

def test_customer_cart_and_server_price_validation():
    # Using authenticated customer token
    headers = {"Authorization": "Bearer demo-token-customer"}
    
    # 1. Add item
    add_resp = client.post(
        "/api/cart/items",
        json={"product_id": "p1000000-0000-0000-0000-000000000001", "quantity": 1},
        headers=headers
    )
    assert add_resp.status_code == 200
    cart_data = add_resp.json()
    assert cart_data["subtotal"] > 0
    # Price is 4999.00 -> free shipping threshold 999.00 -> shipping is 0
    assert cart_data["free_shipping_achieved"] is True
    assert cart_data["shipping_fee"] == 0.0

def test_admin_authorization_enforcement():
    customer_headers = {"Authorization": "Bearer demo-token-customer"}
    admin_headers = {"Authorization": "Bearer demo-token-admin"}

    # Customer trying to view admin dashboard should get 403 Forbidden
    resp = client.get("/api/admin/dashboard", headers=customer_headers)
    assert resp.status_code == 403

    # Admin accessing dashboard should succeed
    admin_resp = client.get("/api/admin/dashboard", headers=admin_headers)
    assert admin_resp.status_code == 200
    assert "total_revenue" in admin_resp.json()
    assert "total_products" in admin_resp.json()

def test_invalid_token_handling():
    bad_headers = {"Authorization": "Bearer completely-invalid-malformed-token"}
    resp = client.get("/api/cart", headers=bad_headers)
    assert resp.status_code == 401
