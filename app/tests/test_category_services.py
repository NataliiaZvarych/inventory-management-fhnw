import pytest


def test_create_category_success(session, services):
    category_service = services["category"]

    category = category_service.create_category(
        session,
        {"name": "Furniture", "type": "sale"},
    )

    assert category.category_id is not None
    assert category.name == "Furniture"


def test_create_category_without_name_raises_error(session, services):
    category_service = services["category"]

    with pytest.raises(ValueError, match="Category name is required"):
        category_service.create_category(session, {"type": "sale"})


def test_get_category_success(session, services, base_data):
    category_service = services["category"]

    category = category_service.get_category(
        session,
        base_data["category"].category_id,
    )

    assert category.name == "Electronics"


def test_update_category_success(session, services, base_data):
    category_service = services["category"]

    updated = category_service.update_category(
        session,
        base_data["category"].category_id,
        {"name": "Updated Electronics"},
    )

    assert updated.name == "Updated Electronics"


def test_delete_category_success(session, services):
    category_service = services["category"]

    category = category_service.create_category(
        session,
        {"name": "Temporary", "type": "sale"},
    )

    result = category_service.delete_category(session, category.category_id)

    assert result is True
