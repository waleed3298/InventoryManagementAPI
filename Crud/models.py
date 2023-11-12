from pydantic import BaseModel
from sqlalchemy import DateTime,Float,Column, String, Integer,Boolean,ForeignKey,ARRAY
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime as dt

class Category(Base):
    __tablename__ = "Categories"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index = True)
    products = relationship("Product",back_populates = "category")

class Product(Base):
    __tablename__ = "Products"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    brand = Column(String,index=True)
    price = Column(String,index=True)
    is_active = Column(Boolean,index=True)
    inventory = relationship("Inventory",back_populates="product")
    category_id = Column(Integer,ForeignKey("Categories.id"))
    category = relationship("Category",back_populates = "products",foreign_keys=[category_id])
    sales = relationship("Sales",back_populates="product")

class Inventory(Base):
    __tablename__ = "Inventory"
    
    id = Column(Integer,primary_key = True)
    product_id = Column(Integer,ForeignKey("Products.id"))
    product = relationship("Product",back_populates="inventory",foreign_keys=[product_id])
    quantity = Column(Integer,index= True)

class Sales(Base):
    __tablename__ = "Sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(Integer)
    sale_date = Column(DateTime, default=dt.utcnow)
    revenue = Column(Float)

    product = relationship("Product", back_populates="sales")
    
    class Config:
        arbitrary_types_allowed = True

