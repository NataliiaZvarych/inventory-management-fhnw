import pytest

from app.services.product_service import ProductService


def test_create_product_success(session, base_data):
    service = ProductService(session)

    created = service.create_product(
        name="Keyboard",
        description="Mechanical keyboard",
        quantity=5,
        min_quantity=1,
        category_id=base_data["category"].id,
        location_id=base_data["location"].id,
    )

    assert created.id is not None
    assert created.name == "Keyboard"
    assert created.quantity == 5


def test_create_product_with_empty_name_raises_error(session, base_data):
    service = ProductService(session)

    with pytest.raises(ValueError, match="Product name cannot be empty"):
        service.create_product(
            name="  ",
            description="No name",
            quantity=1,
            min_quantity=0,
            category_id=base_data["category"].id,
            location_id=base_data["location"].id,
        )


def test_delete_product_removes_record(session, base_data):
    service = ProductService(session)
    product_id = base_data["product"].id

    service.delete_product(product_id)

    assert service.get_product_by_id(product_id) is None
