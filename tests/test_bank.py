import pytest 


def test_new_account(account_factory):
    new_account = account_factory(account_id=5, balance=0)
    new_account.deposit(2000)
    
    assert new_account.balance == 2000
