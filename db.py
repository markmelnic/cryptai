from os import getenv

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_ENGINE = create_engine(getenv('DB_URI'))
DB_SESSION = sessionmaker(
    bind=DB_ENGINE,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

DB_BASE = declarative_base()

def get_db():
    return DB_SESSION()

class Coin(DB_BASE):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String)
    name = Column(String)
    symbol = Column(String)

    def __repr__(self) -> str:
        return f'{self.symbol} - {self.name}'

    def __str__(self) -> str:
        return f'{self.symbol} - {self.name}'

DB_BASE.metadata.create_all(DB_ENGINE)
