import pytest

from app.services.user_service import UserService


def test_create_user_success(session):
    service = UserService(session)

    user = service.create_user("employee1", "employee1@example.com")

    assert user.id is not None
    assert user.username == "employee1"
    assert user.email == "employee1@example.com"


def test_create_user_duplicate_email_raises_error(session):
    service = UserService(session)
    service.create_user("employee1", "employee1@example.com")

    with pytest.raises(ValueError, match="Email already exists"):
        service.create_user("employee2", "employee1@example.com")


def test_create_user_duplicate_username_raises_error(session):
    service = UserService(session)
    service.create_user("employee1", "employee1@example.com")

    with pytest.raises(ValueError, match="Username already exists"):
        service.create_user("employee1", "other@example.com")
