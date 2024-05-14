from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine
import datetime

class Base(DeclarativeBase):
    pass





engine = create_engine("sqlite://", echo=True)

