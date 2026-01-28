from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_filename = Column(String, index=True)
    category = Column(String, index=True)  # Shirt, Pant, Shoe, Accessories
    color = Column(String, index=True)     # Detected color
    occasion = Column(String, index=True, nullable=True) # Formal, Casual, Party, Travel

    owner = relationship("User", back_populates="items")
