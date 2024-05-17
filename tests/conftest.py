import pytest
from source.bank import Account, Base
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine





@pytest.fixture(scope="function")
def session():
    engine = create_engine('sqlite:///:memory:')
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock()
    Base.metadata.create_all(engine)
    yield session
    session.rollback()

@pytest.fixture
def account_factory(session):
    def make_account(account_id, balance):
        account = Account(account_id=account_id, balance=balance, session=session)
        session.add(account)
        session.commit()
        return account
    return make_account
        


