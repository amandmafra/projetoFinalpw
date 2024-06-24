from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    cpf=Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class OrderForm(BaseModel):
    name: str
    quantity: int