from typing import List
from sqlmodel import Session
from app.models import Category, Product
from app.data_access.dao import CategoryDAO, ProductDAO


class CategoryServices:

        def __init__(self, category_dao: CategoryDAO, product_dao: ProductDAO):
                self.category_dao = category_dao
                self.product_dao = product_dao

        def create_category(self, session: Session, category_data: dict) -> Category:
                """
                Create a new category after validating required fields.
                """
                if not category_data.get("name"):
                        raise ValueError("Category name is required")

                category = Category(**category_data)

                return self.category_dao.create(session, category)

        def get_category(self, session: Session, category_id: int) -> Category:
                """
                Get a category by its ID.
                """
                category = self.category_dao.get(session, category_id)

                if not category:
                        raise ValueError("Category not found")

                return category

        def get_all_categories(self, session: Session) -> List[Category]:
                """
                Get all categories from the database.
                """
                return self.category_dao.get_all(session)

        def update_category(
                self,
                session: Session,
                category_id: int,
                data: dict
        ) -> Category:
                """
                Update a category by its ID.
                """
                existing = self.category_dao.get(session, category_id)

                if not existing:
                        raise ValueError("Category not found")

                if "name" in data and not str(data["name"]).strip():
                        raise ValueError("Category name is required")

                category = self.category_dao.update(
                        session,
                        category_id,
                        data,
                )

                if not category:
                        raise ValueError("Update failed")

                return category

        def delete_category(
                self,
                session: Session,
                category_id: int
        ) -> bool:
                """
                Delete a category only if no products are assigned to it.
                """
                category = self.category_dao.get(session, category_id)

                if not category:
                        raise ValueError("Category not found")

                products = self.product_dao.get_by_category_id(
                        session,
                        category_id,
                )

                if products:
                        raise ValueError(
                                "Category cannot be deleted because products are assigned to it"
                        )

                result = self.category_dao.delete(
                        session,
                        category_id,
                )

                if not result:
                        raise ValueError("Delete failed")

                return result

        def get_products_by_category(
                self,
                session: Session,
                category_id: int
        ) -> List[Product]:
                """
                Get all products for a specific category using DAO method.
                """
                category = self.category_dao.get(
                        session,
                        category_id,
                )

                if not category:
                        raise ValueError("Category not found")

                return self.product_dao.get_by_category_id(
                        session,
                        category_id,
                )
