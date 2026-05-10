import pytest


def test_get_user_success(session, services, base_data):
    user_service = services["user"]

    user = user_service.get_user(
        session,
        base_data["user"].user_id,
    )

    assert user.name == "admin"


def test_get_user_not_found_raises_error(session, services):
    user_service = services["user"]

    with pytest.raises(ValueError, match="User not found"):
        user_service.get_user(session, 999)


def test_login_success(session, services, base_data):
    user_service = services["user"]

    user = user_service.login(
        session,
        name="admin",
        password="password123",
    )

    assert user.name == "admin"


def test_login_wrong_password_raises_error(session, services, base_data):
    user_service = services["user"]

    with pytest.raises(ValueError, match="Incorrect password"):
        user_service.login(
            session,
            name="admin",
            password="wrongpassword",
        )


def test_change_role_success(session, services, base_data):
    user_service = services["user"]

    user = user_service.change_role(
        session,
        base_data["user"].user_id,
        "manager",
    )

    assert user.role == "manager"


def test_change_role_invalid_role_raises_error(session, services, base_data):
    user_service = services["user"]

    with pytest.raises(ValueError, match="is not allowed"):
        user_service.change_role(
            session,
            base_data["user"].user_id,
            "invalid_role",
        )
