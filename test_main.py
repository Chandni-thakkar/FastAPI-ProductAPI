from http.client import HTTPException

import fastapi
import pytest

import models
from database import SessionLocal
from main import app, create_product, read_products, read_product, update_product, delete_product, get_db, ProductBase


@pytest.fixture
def db():
    """Provides a database session for the tests."""
    with SessionLocal() as db_session:
        yield db_session

# Test product creation
def test_create_product(db):
    product_data = {"title": "Test Product", "description": "This is a test product", "price": 10.99}
    db_product = models.Product(**product_data)
    assert db_product.title == product_data["title"]
    assert db_product.description == product_data["description"]
    assert db_product.price == product_data["price"]


# Test product retrieval (all)
def test_read_products(db):
    products = read_products(db)
    assert len(products) >= 0  # Ensure at least no products or some products exist

# Test product retrieval (specific)
def test_read_product(db):
    product = create_product({"title": "Test Product", "description": "This is a test product", "price": 10.99}, db)
    retrieved_product = read_product(product.id, db)
    assert retrieved_product.id == product.id
    assert retrieved_product.title == product.title

# Test product update
def test_update_product_success(db):
    product = create_product({"title": "Test Product", "description": "This is a test product", "price": 10.99}, db)
    updated_data = ProductBase(title="Updated Title", description="Updated description", price=19.99)

    updated_product = update_product(product.id, updated_data, db)

    assert updated_product.title == "Updated Title"



def test_update_product_nonexistent(db):
    nonexistent_product_id = 100  # Assuming this ID doesn't exist
    updated_data = {"title": "Nonexistent Product", "price": 99.99}

    with pytest.raises(fastapi.exceptions.HTTPException) as exc:
        update_product(nonexistent_product_id, updated_data, db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Product not found"

# Test product deletion
def test_delete_product(db):
    product = create_product({"title": "Test Product", "description": "This is a test product", "price": 10.99}, db)
    delete_product(product.id, db)

    with pytest.raises(fastapi.exceptions.HTTPException) as exc:
        read_product(product.id, db)  # This will raise HTTPException

    assert exc.value.status_code == 404
    assert exc.value.detail == "Product not found"



