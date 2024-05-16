import pytest 
from datetime import datetime


def test_new_account(account_factory):
    new_account = account_factory(account_id=5, balance=0)
    new_account.deposit(2000)
    last_transaction = new_account.transactions[-1]
    assert new_account.balance == 2000
    assert last_transaction._type == ("deposit")
    assert (datetime.now() - last_transaction.timestamp).total_seconds() < 1
    assert new_account.session.commit.call_count == 2 # two because, first in account_factory and the deposit


def test_deposit_negative_amount(account_factory):
    new_account = account_factory(account_id=6, balance=0)
    with pytest.raises(ValueError):
        new_account.withdraw(-100)
    last_transaction = new_account.transactions
    assert new_account.balance == 0
    assert last_transaction == []
    assert new_account.session.commit.call_count == 1 # one commit because has in account_factory


def test_deposit_zero_amount(account_factory):
    new_account = account_factory(account_id=7, balance=0)
    new_account.deposit(0)
    last_transaction = new_account.transactions
    assert new_account.balance == 0
    assert last_transaction == []
    assert new_account.session.commit.call_count == 1 # one commit because has in account_factory


def test_withdraw_normal(account_factory):
    new_account = account_factory(account_id=8, balance=200)
    new_account.withdraw(100)
    last_transaction = new_account.transactions[-1]
    assert new_account.balance == 100
    assert last_transaction._type == ("withdraw")
    assert new_account.session.commit.call_count == 2 # two because, first in account_factory and the withdraw


def test_withdraw_insufficient_funds(account_factory):
    new_account = account_factory(account_id=9, balance=200)
    new_account.withdraw(300)
    last_transaction = new_account.transactions
    assert new_account.balance == 200
    assert last_transaction == []
    assert new_account.session.commit.call_count == 1 # one commit because has in account_factory


def test_withdraw_negative_amount(account_factory):
    new_account = account_factory(account_id=10, balance=100)
    with pytest.raises(ValueError):
        new_account.withdraw(-100)
    assert new_account.balance == 100
    assert new_account.transactions == []
    assert new_account.session.commit.call_count == 1 #one commit beacuse has in account_factory


def test_transfer_zero_amount(account_factory):
    new_account = account_factory(account_id=11, balance=100)
    other_account = account_factory(account_id=12, balance=100)
    with pytest.raises(ValueError):
        new_account.transfer(other_account,0)
    assert new_account.balance == 100
    assert other_account.balance == 100
    assert new_account.transactions == []
    assert other_account.transactions == []
    assert new_account.session.commit.call_count == 2 #one commit beacuse has in account_factory and other_account
    assert other_account.session.commit.call_count == 2 #one commit beacuse has in account_factory and other_account


def test_get_balance_initial(account_factory):
    new_account = account_factory(account_id=13, balance=100)
    new_account2 = account_factory(account_id=14, balance=0)
    last_transaction = new_account.transactions
    last_transaction2 = new_account2.transactions
    assert new_account.get_balance() == 100
    assert new_account2.get_balance() == 0
    assert new_account.transactions == []
    assert new_account2.transactions == []


def test_get_balance_after_deposit(account_factory):
    new_account = account_factory(account_id=15, balance=0)
    new_account.deposit(100)
    assert new_account.get_balance() == 100
    


def test_get_balance_after_withdrawal(account_factory):
    # Vérifier le solde après une tentative de retrait échouée due à un solde insuffisant
    

