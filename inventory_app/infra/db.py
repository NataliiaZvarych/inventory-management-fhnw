from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///inventory.db"

engine = create_engine(DATABASE_URL, echo=True)

# Create session factory (keeps objects usable after commit)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return SessionLocal()