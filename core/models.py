from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, Table, VARCHAR
from sqlalchemy.orm import relationship

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR(255), unique=True)
    password_hash = Column(VARCHAR(255))
    balance = Column(Integer)
    is_activate = Column(Boolean)
    code = Column(VARCHAR(5))


class Cases(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), unique=True)
    price = Column(Integer)
    old_price = Column(Integer)

    games = relationship("Games", secondary="case_games")


class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255), unique=True)


class CaseGame(Base):
    __tablename__ = "case_games"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    game_id = Column(Integer, ForeignKey("games.id"))


class Purchases(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    case_id = Column(Integer, ForeignKey("cases.id"))
    key_id = Column(Integer, ForeignKey("keys.id"))
    is_open = Column(Boolean)

    user = relationship("Users")
    key = relationship("Keys")
    case = relationship("Cases")


class Keys(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    code = Column(VARCHAR(255))
    is_buy = Column(Boolean)

    game = relationship("Games")
