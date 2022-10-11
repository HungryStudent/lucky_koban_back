from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Table, VARCHAR
from sqlalchemy.orm import relationship

from .database import Base

case_product = Table("case_product", Base.metadata,
                     Column("case_id", Integer(), ForeignKey("cases.id")),
                     Column("product_id", Integer(), ForeignKey("products.id")))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(VARCHAR(255), unique=True)
    password_hash = Column(VARCHAR(255))
    balance = Column(Integer)
    email = Column(VARCHAR(255), unique=True)
    is_confirm = Column(Boolean)


class Cases(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), unique=True)
    price = Column(Integer)

    products = relationship("Products", secondary=case_product)


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)


class Purchases(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key_id = Column(Integer, ForeignKey("keys.id"))

    user = relationship("Users")
    key = relationship("Keys")


class Keys(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    is_buy = Column(Boolean)

    product = relationship("Products")
