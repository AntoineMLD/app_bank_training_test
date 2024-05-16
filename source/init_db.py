from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from source.bank import Base


def setup_database():
    engine = create_engine('sqlite:///bdd_bank.db')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))
    return session
