from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, MetaData
from sqlalchemy.orm import relationship
from init_db import *
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///bdd_bank.db')
session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"
    account_id = Column("account_id",Integer, primary_key=True)
    balance = Column("balance",Float)
    transactions = relationship("Transaction", back_populates="account")

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
    
    def __repr__(self):
        return f"<Account(account_id='{self.account_id}, balance='{self.balance}')"


    def create_account(self):
        new_account = Account(account_id=self.account_id, balance=self.balance)
        session.add(new_account)

    def get_balance(self):
        return self.balance




class Transaction(Base):
    __tablename__ = "transaction"
    transaction_id = Column("transaction_id",Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    amount = Column("amount",Float)
    _type = Column("_type",String)
    timestamp = Column("timestamp",DateTime, default=datetime.now)
    account = relationship("Account", back_populates="transactions")
    

    def __init__(self,transaction_id, _type, amount):
        self.transaction_id = transaction_id
        self.amount = amount
        self.type = _type

    def deposit(self):
        pass


    def withdraw(self):
        pass


    def transfer(self):
        pass



Base.metadata.create_all(engine)