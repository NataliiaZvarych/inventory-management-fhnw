from sqlmodel import SQLModel, create_engine
from nicegui import ui

# Import all models so SQLModel metadata includes every table before create_all.
from models import Category, Location, Product, StockMovement, User
from views.dashboard import render_dashboard


DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
	SQLModel.metadata.create_all(engine)


if __name__ in {"__main__", "__mp_main__"}:
	create_db_and_tables()
	render_dashboard()
	ui.run(host="localhost", port=8080)
