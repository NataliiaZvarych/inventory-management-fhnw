

from typing import List
from sqlmodel import Session
from app.models import StockMovement
from app.data_access.dao import ProductDAO, UserDAO, StockMovementDAO, StorageLocationDAO



class MovementService:

    def __init__(self, product_dao: ProductDAO, user_dao: UserDAO, movement_dao: StockMovementDAO, location_dao: StorageLocationDAO):
        # Save DAO objects for later use
        self.product_dao = product_dao
        self.user_dao = user_dao
        self.movement_dao = movement_dao
        self.location_dao = location_dao

    def create_movement(self, session: Session, movement_data: dict) -> StockMovement:
        """
        Create a new stock movement after validating product, user, and location.
        """
        product = self.product_dao.get(session, movement_data['product_id'])
        if not product:
            raise ValueError("Product not found")
        user = self.user_dao.get(session, movement_data['user_id'])
        if not user:
            raise ValueError("User not found")
        location = self.location_dao.get(session, movement_data['location_id'])
        if not location:
            raise ValueError("Location not found")
        movement = StockMovement(**movement_data)
        return self.movement_dao.create(session, movement)
    
    def get_movement(self, session: Session, movement_id: int) -> StockMovement:
        """
        Get a single movement by its ID.
        """
        movement = self.movement_dao.get(session, movement_id)
        if not movement:
            raise ValueError("Movement not found")
        return movement


    def get_all_movements(self, session: Session) -> List[StockMovement]:
        """
        Get all stock movements from the database.
        """
        return self.movement_dao.get_all(session)
    


    def get_product_history(self, session: Session, product_id: int) -> List[StockMovement]:
        """
        Get all movements for a specific product.
        """
        product = self.product_dao.get(session, product_id)
        if not product:
            raise ValueError("Product not found")
        return self.movement_dao.get_by_product(session, product_id)
    
    def move_product(self, session: Session, product_id: int, user_id: int, from_location_id: int, to_location_id: int, quantity: int) -> StockMovement:
        """
        Move a product from one location to another and record the movement.
        Checks business rules, then calls create_movement to save the record.
        """
        # Business rule: source and target locations must be different
        if from_location_id == to_location_id:
            raise ValueError("Source and target locations must be different")
        # Business rule: quantity must be positive
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        # Business rule: check stock availability at the source location
        product = self.product_dao.get(session, product_id)
        if not product:
            raise ValueError("Product not found")
        if getattr(product, "storage_location_id", None) != from_location_id:
            raise ValueError("Product is not located at the source location")
        if product.quantity < quantity:
            raise ValueError("Not enough stock at the source location")
        # Prepare movement data
        movement_data = {
            "product_id": product_id,
            "user_id": user_id,
            "location_id": to_location_id,  # destination becomes the new location
            "quantity": quantity,
            "movement_type": "move"
        }
        return self.create_movement(session, movement_data)
    
    def update_movement(self, session: Session, movement_id: int, update_data: dict) -> StockMovement:
        """
        Update an existing stock movement by its ID after validating existence.
        """
        # Get the movement to update
        movement = self.movement_dao.get(session, movement_id)
        if not movement:
            raise ValueError("Movement not found")
        # Optionally validate related fields if present in update_data
        if 'product_id' in update_data:
            product = self.product_dao.get(session, update_data['product_id'])
            if not product:
                raise ValueError("Product not found")
        if 'user_id' in update_data:
            user = self.user_dao.get(session, update_data['user_id'])
            if not user:
                raise ValueError("User not found")
        if 'from_location_id' in update_data:
            from_location = self.location_dao.get(session, update_data['from_location_id'])
            if not from_location:
                raise ValueError("Source location not found")
        if 'to_location_id' in update_data:
            to_location = self.location_dao.get(session, update_data['to_location_id'])
            if not to_location:
                raise ValueError("Target location not found")
        # Update the movement in the database
        updated = self.movement_dao.update(session, movement_id, update_data)
        if not updated:
            raise ValueError("Update failed")
        return updated
    
    def delete_movement(self, session: Session, movement_id: int) -> bool:
        """
        Delete a stock movement by its ID.
        """
        result = self.movement_dao.delete(session, movement_id)
        if not result:
            raise ValueError("Movement not found")
        return result
    
    def get_movements_by_user(self, session: Session, user_id: int) -> List[StockMovement]:
        """
        Get all movements performed by a specific user.
        """
        # Предполагается, что StockMovementDAO.get_all() возвращает все движения
        all_movements = self.movement_dao.get_all(session)
        return [m for m in all_movements if m.user_id == user_id]

    def get_movements_by_location(self, session: Session, location_id: int) -> List[StockMovement]:
        """
        Get all movements related to a specific storage location.
        """
        all_movements = self.movement_dao.get_all(session)
        # Предполагается, что location_id может быть как source, так и target (если есть from/to), иначе просто location_id
        return [m for m in all_movements if getattr(m, 'location_id', None) == location_id or getattr(m, 'from_location_id', None) == location_id or getattr(m, 'to_location_id', None) == location_id]

    def get_movements_by_date(self, session: Session, date) -> List[StockMovement]:
        """
        Get all movements for a specific date (date: datetime.date).
        """
        all_movements = self.movement_dao.get_all(session)
        return [m for m in all_movements if m.timestamp.date() == date]