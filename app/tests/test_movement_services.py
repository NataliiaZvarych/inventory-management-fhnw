import pytest


def test_create_movement_success(session, services, base_data):
    movement_service = services["movement"]

    movement = movement_service.create_movement(
        session,
        {
            "product_id": base_data["product"].product_id,
            "user_id": base_data["user"].user_id,
            "location_id": base_data["location"].storage_location_id,
            "quantity": 3,
            "movement_type": "move",
            "note": "Test movement",
        },
    )

    assert movement.movement_id is not None
    assert movement.product_id == base_data["product"].product_id
    assert movement.user_id == base_data["user"].user_id
    assert movement.quantity == 3
    assert movement.movement_type == "move"


def test_create_movement_with_invalid_product_raises_error(session, services, base_data):
    movement_service = services["movement"]

    with pytest.raises(ValueError, match="Product not found"):
        movement_service.create_movement(
            session,
            {
                "product_id": 999,
                "user_id": base_data["user"].user_id,
                "location_id": base_data["location"].storage_location_id,
                "quantity": 3,
                "movement_type": "move",
            },
        )


def test_create_movement_with_invalid_user_raises_error(session, services, base_data):
    movement_service = services["movement"]

    with pytest.raises(ValueError, match="User not found"):
        movement_service.create_movement(
            session,
            {
                "product_id": base_data["product"].product_id,
                "user_id": 999,
                "location_id": base_data["location"].storage_location_id,
                "quantity": 3,
                "movement_type": "move",
            },
        )


def test_create_movement_with_invalid_location_raises_error(session, services, base_data):
    movement_service = services["movement"]

    with pytest.raises(ValueError, match="Location not found"):
        movement_service.create_movement(
            session,
            {
                "product_id": base_data["product"].product_id,
                "user_id": base_data["user"].user_id,
                "location_id": 999,
                "quantity": 3,
                "movement_type": "move",
            },
        )


def test_get_movement_success(session, services, base_data):
    movement_service = services["movement"]

    movement = movement_service.create_movement(
        session,
        {
            "product_id": base_data["product"].product_id,
            "user_id": base_data["user"].user_id,
            "location_id": base_data["location"].storage_location_id,
            "quantity": 2,
            "movement_type": "move",
        },
    )

    found = movement_service.get_movement(session, movement.movement_id)

    assert found.movement_id == movement.movement_id


def test_delete_movement_success(session, services, base_data):
    movement_service = services["movement"]

    movement = movement_service.create_movement(
        session,
        {
            "product_id": base_data["product"].product_id,
            "user_id": base_data["user"].user_id,
            "location_id": base_data["location"].storage_location_id,
            "quantity": 2,
            "movement_type": "move",
        },
    )

    result = movement_service.delete_movement(session, movement.movement_id)

    assert result is True


def test_move_product_same_location_raises_error(session, services, base_data):
    movement_service = services["movement"]

    with pytest.raises(ValueError, match="Source and target locations must be different"):
        movement_service.move_product(
            session,
            product_id=base_data["product"].product_id,
            user_id=base_data["user"].user_id,
            from_location_id=base_data["location"].storage_location_id,
            to_location_id=base_data["location"].storage_location_id,
            quantity=1,
        )


def test_move_product_not_enough_stock_raises_error(session, services, base_data):
    movement_service = services["movement"]

    second_location = services["location"].create_location(
        session,
        {"name": "Second Warehouse", "shelf_number": "B2"},
    )

    with pytest.raises(ValueError, match="Not enough stock"):
        movement_service.move_product(
            session,
            product_id=base_data["product"].product_id,
            user_id=base_data["user"].user_id,
            from_location_id=base_data["location"].storage_location_id,
            to_location_id=second_location.storage_location_id,
            quantity=999,
        )
