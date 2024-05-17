from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import time
import threading

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"
    account_id = Column("account_id", Integer, primary_key=True)
    balance = Column("balance", Float)
    transactions = relationship("Transaction", back_populates="account")

    def __init__(self, account_id, balance, session):
        self.account_id = account_id
        self.balance = balance
        self.session = session
        

    def create_transaction(self, amount, transaction_type):
        transaction = Transaction(amount=amount, _type=transaction_type, timestamp=datetime.now(), account=self)
        return transaction

    def get_balance(self):
        
        return self.balance

    def withdraw(self, amount):
        
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.balance < amount:
            raise ValueError("No credits")
        self.balance -= amount
        new_transaction = self.create_transaction(amount=amount, transaction_type="withdraw")
        self.session.add(new_transaction)
        self.session.commit()
        return True

    def deposit(self, amount):
        
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        self.balance += amount
        new_transaction = self.create_transaction(amount=amount, transaction_type="deposit")
        self.session.add(new_transaction)
        self.session.commit()
        return True
            

    def transfer(self, target_account, amount):
        if self.balance < amount:
            return False
        self.withdraw(amount)
        target_account.deposit(amount)
        return True


class Transaction(Base):
    __tablename__ = "transaction"
    transaction_id = Column("transaction_id", Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    amount = Column("amount", Float)
    _type = Column("_type", String)
    timestamp = Column("timestamp", DateTime, default=datetime.now)
    account = relationship("Account", back_populates="transactions")
