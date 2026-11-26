import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database_models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()