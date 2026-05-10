import pytest


def test_create_location_success(session, services):
    location_service = services["location"]

    location = location_service.create_location(
        session,
        {"name": "Second Warehouse", "shelf_number": "B2"},
    )

    assert location.storage_location_id is not None
    assert location.name == "Second Warehouse"


def test_create_location_without_name_raises_error(session, services):
    location_service = services["location"]

    with pytest.raises(ValueError, match="Location name is required"):
        location_service.create_location(session, {"shelf_number": "C3"})


def test_get_location_success(session, services, base_data):
    location_service = services["location"]

    location = location_service.get_location(
        session,
        base_data["location"].storage_location_id,
    )

    assert location.name == "Main Warehouse"


def test_update_location_success(session, services, base_data):
    location_service = services["location"]

    updated = location_service.update_location(
        session,
        base_data["location"].storage_location_id,
        {"name": "Updated Warehouse"},
    )

    assert updated.name == "Updated Warehouse"


def test_delete_location_success(session, services):
    location_service = services["location"]

    location = location_service.create_location(
        session,
        {"name": "Temporary Location", "shelf_number": "T1"},
    )

    result = location_service.delete_location(
        session,
        location.storage_location_id,
    )

    assert result is True
