import pytest
from source.bank import Account
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from source.init_db import setup_database as setup_database


@pytest.fixture
def session():
    session = UnifiedAlchemyMagicMock()
    Session = session()
    return Session

@pytest.fixture
def account_factory(session):
    def make_account(account_id, balance):
        account = Account(account_id=account_id, balance=balance, session=session)
        session.add(account)
        session.commit()
       
        return account
    return make_account
        


