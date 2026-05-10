import pytest


def test_create_product_success(session, services, base_data):
    product_service = services["product"]

    product = product_service.create_product(
        session,
        {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "quantity": 5,
            "minimum_stock": 1,
            "status": "active",
            "category_id": base_data["category"].category_id,
            "storage_location_id": base_data["location"].storage_location_id,
        },
    )

    assert product.product_id is not None
    assert product.name == "Keyboard"
    assert product.quantity == 5


def test_create_product_with_invalid_category_raises_error(session, services, base_data):
    product_service = services["product"]

    with pytest.raises(ValueError, match="Category not found"):
        product_service.create_product(
            session,
            {
                "name": "Mouse",
                "description": "Wireless mouse",
                "quantity": 3,
                "minimum_stock": 1,
                "status": "active",
                "category_id": 999,
                "storage_location_id": base_data["location"].storage_location_id,
            },
        )


def test_check_availability_returns_true(session, services, base_data):
    product_service = services["product"]

    result = product_service.check_availability(
        session,
        base_data["product"].product_id,
    )

    assert result is True


def test_delete_product_success(session, services, base_data):
    product_service = services["product"]

    result = product_service.delete_product(
        session,
        base_data["product"].product_id,
    )

    assert result is True
