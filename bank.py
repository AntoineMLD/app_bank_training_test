from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine
from init_db import Base
import datetime

class Account(Base):
    __tablename__: str = "account"
    account_id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column()

    def __init__(self, account_id, initial_deposit):
        self.account_id = account_id
        self.initial_deposit = initial_deposit

    def create_account(self):
        pass


    def get_balance(self):
        pass



class Transation(Base):
    __tablename__ = "transaction"
    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"))
    amount: Mapped[float] = mapped_column()
    type: Mapped[str] = mapped_column(String(150))
    timestamp: Mapped[datetime] = mapped_column()

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


