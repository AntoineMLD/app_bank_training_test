from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
import init_db as init
from init_db import engine
from datetime import datetime

Base = declarative_base()

class Account(Base):
    __tablename__ = "account"
    account_id = Column("account_id",Integer, primary_key=True)
    balance = Column("balance",Float)
    account = relationship("Transaction", back_populates="transactions")


    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance



    def create_account(self):
        account = Account(account_id=self.account_id, balance=self.balance)
        return account


    def get_balance(self):
        return self.balance




class Transation(Base):
    __tablename__ = "transaction"
    transaction_id = Column("transaction_id",Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    amount = Column("amount",Float)
    type = Column("type",String)
    timestamp = Column("timestamp",DateTime, default=datetime.now)


    def __init__(self,transaction_id, type, amount):
        self.transaction_id = transaction_id
        self.amount = amount
        self.type = type

    def deposit(self):
        pass


    def withdraw(self):
        pass


    def transfer(self):
        pass



session = init.Session()
Base.metadata.create_all(bind=engine)