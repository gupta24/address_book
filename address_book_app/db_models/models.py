from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from address_book_app.core.sqlite_db_connection import Base


class AddressBook(Base):
    __tablename__ = "address_book"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, nullable=False)
    x_coordinates = Column(Float, nullable=False)
    y_coordinates = Column(Float, nullable=False)
