from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from address_book_app.core.logger import logger
from configuration import SQLITE_DB_URI


# make the connection with database using sqlalchemy
SQLALCHEMY_DATABASE_URL = SQLITE_DB_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# use to seesion of database connection and access by db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()