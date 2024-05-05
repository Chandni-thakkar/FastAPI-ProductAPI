from sqlalchemy import Boolean,Column,Integer,String,Float
from database import Base

# Define the Product model
class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True)
    title=Column(String(255),nullable=False)
    description= Column(String(255))
    price=Column(Float,nullable=False)

class Users(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    username=Column(String(255),unique=True)
    hashed_password=Column(String)

