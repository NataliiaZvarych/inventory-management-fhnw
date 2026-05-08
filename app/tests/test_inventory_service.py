import pytest

from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService


def test_stock_in_increases_quantity(session, base_data):
    service = InventoryService(session)
    product = base_data["product"]
    user = base_data["user"]

    movement = service.stock_in(product.id, user.id, 3, note="Restock")
    updated_product = ProductService(session).get_product_by_id(product.id)

    assert movement.movement_type == "in"
    assert updated_product.quantity == 13


def test_stock_out_decreases_quantity(session, base_data):
    service = InventoryService(session)
    product = base_data["product"]
    user = base_data["user"]

    movement = service.stock_out(product.id, user.id, 4, note="Shipment")
    updated_product = ProductService(session).get_product_by_id(product.id)

    assert movement.movement_type == "out"
    assert updated_product.quantity == 6


def test_stock_out_more_than_available_raises_error(session, base_data):
    service = InventoryService(session)
    product = base_data["product"]
    user = base_data["user"]

    with pytest.raises(ValueError, match="Not enough stock"):
        service.stock_out(product.id, user.id, 999)


def test_get_low_stock_products_returns_expected_items(session, base_data):
    service = InventoryService(session)
    product = base_data["product"]
    user = base_data["user"]

    service.stock_out(product.id, user.id, 8)
    low_stock_products = service.get_low_stock_products()

    assert len(low_stock_products) == 1
    assert low_stock_products[0].id == product.id
    assert low_stock_products[0].status == "low_stock"
