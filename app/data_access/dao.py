

from typing import List, Optional
from sqlmodel import Session, select
from sqlmodel import Engine
from app.models import Product, Category, StorageLocation, StockMovement, User

# This is a base class for all DAOs
# It stores the database engine and can open a session
class BaseDAO:
    """Base class holding the SQLAlchemy/SQLModel engine."""
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def session(self) -> Session:
        """Create a new database session."""
        return Session(self.engine)

    
# This class helps you work with Product objects in the database
class ProductDAO(BaseDAO):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    # Create a new product in the database
    def create(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    # Get one product by its id
    def get(self, session: Session, product_id: int) -> Optional[Product]:
        return session.get(Product, product_id)

    # Get all products
    def get_all(self, session: Session) -> List[Product]:
        statement = select(Product)
        return session.exec(statement).all()

    # Update a product by its id
    def update(self, session: Session, product_id: int, data: dict) -> Optional[Product]:
        product = session.get(Product, product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    # Delete a product by its id
    def delete(self, session: Session, product_id: int) -> bool:
        product = session.get(Product, product_id)
        if not product:
            return False
        session.delete(product)
        session.commit()
        return True


# This class helps you work with Category objects in the database
class CategoryDAO(BaseDAO):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def create(self, session: Session, category: Category) -> Category:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    def get(self, session: Session, category_id: int) -> Optional[Category]:
        return session.get(Category, category_id)

    def get_all(self, session: Session) -> List[Category]:
        statement = select(Category)
        return session.exec(statement).all()

    def update(self, session: Session, category_id: int, data: dict) -> Optional[Category]:
        category = session.get(Category, category_id)
        if not category:
            return None
        for key, value in data.items():
            setattr(category, key, value)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    def delete(self, session: Session, category_id: int) -> bool:
        category = session.get(Category, category_id)
        if not category:
            return False
        session.delete(category)
        session.commit()
        return True


# This class helps you work with StorageLocation objects in the database
class StorageLocationDAO(BaseDAO):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def create(self, session: Session, location: StorageLocation) -> StorageLocation:
        session.add(location)
        session.commit()
        session.refresh(location)
        return location

    def get(self, session: Session, location_id: int) -> Optional[StorageLocation]:
        return session.get(StorageLocation, location_id)

    def get_all(self, session: Session) -> List[StorageLocation]:
        statement = select(StorageLocation)
        return session.exec(statement).all()

    def update(self, session: Session, location_id: int, data: dict) -> Optional[StorageLocation]:
        location = session.get(StorageLocation, location_id)
        if not location:
            return None
        for key, value in data.items():
            setattr(location, key, value)
        session.add(location)
        session.commit()
        session.refresh(location)
        return location

    def delete(self, session: Session, location_id: int) -> bool:
        location = session.get(StorageLocation, location_id)
        if not location:
            return False
        session.delete(location)
        session.commit()
        return True


# This class helps you work with StockMovement objects in the database
class StockMovementDAO(BaseDAO):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def create(self, session: Session, movement: StockMovement) -> StockMovement:
        session.add(movement)
        session.commit()
        session.refresh(movement)
        return movement

    def get(self, session: Session, movement_id: int) -> Optional[StockMovement]:
        return session.get(StockMovement, movement_id)

    def get_all(self, session: Session) -> List[StockMovement]:
        statement = select(StockMovement)
        return session.exec(statement).all()

    def update(self, session: Session, movement_id: int, data: dict) -> Optional[StockMovement]:
        movement = session.get(StockMovement, movement_id)
        if not movement:
            return None
        for key, value in data.items():
            setattr(movement, key, value)
        session.add(movement)
        session.commit()
        session.refresh(movement)
        return movement

    def delete(self, session: Session, movement_id: int) -> bool:
        movement = session.get(StockMovement, movement_id)
        if not movement:
            return False
        session.delete(movement)
        session.commit()
        return True


# This class helps you work with User objects in the database
class UserDAO(BaseDAO):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def create(self, session: Session, user: User) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get(self, session: Session, user_id: int) -> Optional[User]:
        return session.get(User, user_id)

    def get_all(self, session: Session) -> List[User]:
        statement = select(User)
        return session.exec(statement).all()

    def update(self, session: Session, user_id: int, data: dict) -> Optional[User]:
        user = session.get(User, user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def delete(self, session: Session, user_id: int) -> bool:
        user = session.get(User, user_id)
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True

    # Create a new product in the database
    def create(self, session: Session, product: Product) -> Product:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    # Get one product by its id
    def get(self, session: Session, product_id: int) -> Optional[Product]:
        return session.get(Product, product_id)

    # Get all products
    def get_all(self, session: Session) -> List[Product]:
        statement = select(Product)
        return session.exec(statement).all()

    # Update a product by its id
    def update(self, session: Session, product_id: int, data: dict) -> Optional[Product]:
        product = session.get(Product, product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    # Delete a product by its id
    def delete(self, session: Session, product_id: int) -> bool:
        product = session.get(Product, product_id)
        if not product:
            return False
        session.delete(product)
        session.commit()
        return True

