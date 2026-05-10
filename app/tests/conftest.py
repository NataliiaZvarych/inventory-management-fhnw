import hashlib
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.models import Category, StorageLocation, Product, User
from app.data_access.dao import CategoryDAO, ProductDAO, StorageLocationDAO, UserDAO
from app.services.category_services import CategoryServices
from app.services.location_services import LocationServices
from app.services.product_services import ProductServices
from app.services.user_service import UserService


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture
def services(engine):
    category_dao = CategoryDAO(engine)
    product_dao = ProductDAO(engine)
    location_dao = StorageLocationDAO(engine)
    user_dao = UserDAO(engine)

    return {
        "category": CategoryServices(category_dao, product_dao),
        "location": LocationServices(location_dao),
        "product": ProductServices(product_dao, category_dao, location_dao),
        "user": UserService(user_dao),
    }


@pytest.fixture
def base_data(session):
    category = Category(name="Electronics", type="sale")
    location = StorageLocation(name="Main Warehouse", shelf_number="A1")

    password_hash = hashlib.sha256("password123".encode()).hexdigest()
    user = User(name="admin", role="admin", password_hash=password_hash)

    session.add(category)
    session.add(location)
    session.add(user)
    session.commit()

    session.refresh(category)
    session.refresh(location)
    session.refresh(user)

    product = Product(
        name="Laptop",
        description="Dell laptop",
        quantity=10,
        minimum_stock=2,
        status="active",
        category_id=category.category_id,
        storage_location_id=location.storage_location_id,
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    return {
        "category": category,
        "location": location,
        "user": user,
        "product": product,
    }
