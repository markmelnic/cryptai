from os import getenv

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DB_ENGINE = create_engine("sqlite:///.db")
DB_SES_LOCAL = sessionmaker(bind=DB_ENGINE, autocommit=False, autoflush=False,)
DB_BASE = declarative_base()

def get_db():
    return DB_SES_LOCAL()

class Coin(DB_BASE):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String)
    name = Column(String)
    symbol = Column(String)

DB_BASE.metadata.create_all(DB_ENGINE)
