#prerequesesites
# Install the required packages using pip:
# pip install sqlalchemy psycopg2-binary
# Ensure you have a PostgreSQL server running and a database named 'db5785' created.

# your_models.py
# This file defines the SQLAlchemy models for a simple invoicing system.
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("postgresql://eliezer:admin@localhost:5432/db5785")
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    invoices = relationship("Invoice", back_populates="customer")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    invoices = relationship("Invoice", back_populates="product")
    def __str__(self):
        return self.name

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    customer = relationship("Customer", back_populates="invoices")
    product = relationship("Product", back_populates="invoices")
    def __str__(self):
        return f"Invoice {self.id} for {self.customer}"
# Uncomment the following line to create the tables in the database
# Note: This should be run only once to create the tables.    

# Create all tables in the database
# Base.metadata.create_all(engine)        