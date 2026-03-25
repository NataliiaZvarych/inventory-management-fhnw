import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.models import Category, Location, Product, User


@pytest.fixture
def session() -> Session:
	"""Create a clean in-memory database session for each test."""
	engine = create_engine(
		"sqlite://",
		connect_args={"check_same_thread": False},
		poolclass=StaticPool,
	)
	SQLModel.metadata.create_all(engine)

	with Session(engine) as db_session:
		yield db_session


@pytest.fixture
def base_data(session: Session) -> dict:
	"""Insert minimum records needed by service tests."""
	category = Category(name="Electronics", description="Electronic devices")
	location = Location(name="Main Warehouse", description="Main storage")
	user = User(username="admin", email="admin@example.com", role="admin")

	session.add(category)
	session.add(location)
	session.add(user)
	session.commit()

	session.refresh(category)
	session.refresh(location)
	session.refresh(user)

	product = Product(
		name="Laptop",
		description="Dell",
		quantity=10,
		min_quantity=2,
		status="available",
		category_id=category.id,
		location_id=location.id,
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
