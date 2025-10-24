from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from fastapi import FastAPI


#"sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///../database/itguru_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
 
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders" 
    Id = Column(Integer, primary_key=True, index=True)
    Client_id = Column(Integer)
    Order_sum = Column(Integer)
    Created_at = Column(String)


class Product(Base):
    __tablename__ = "products" 
    Id = Column(Integer, primary_key=True, index=True)
    Count = Column(Integer)
    Price = Column(Integer)
    Category_id = Column(Integer)
    Name = Column(String)


class OrderProducts(Base):
    __tablename__ = "orderproducts" 
    Order_id = Column(Integer, primary_key=True, index=True)
    Product_id = Column(Integer, primary_key=True, index=True)
    Product_count = Column(Integer)


#SessionLocal = sessionmaker(autoflush=False, bind=engine)

    
