from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///bdd_bank.db", echo=True)


Session = sessionmaker(bind=engine)