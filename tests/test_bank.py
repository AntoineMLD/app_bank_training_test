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
        new_account.deposit(-100)
    last_transaction = new_account.transactions
    assert new_account.balance == 0
    assert last_transaction == []
    assert new_account.session.commit.call_count == 1 # one commit because has in account_factory



def test_deposit_zero_amount(account_factory):
    new_account = account_factory(account_id=7, balance=0)
    with pytest.raises(ValueError):
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
    with pytest.raises(ValueError):
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
    new_account =account_factory(account_id=16, balance=20)
    new_account.withdraw(5)
    assert new_account.balance == 15



def test_get_balance_after_failed_withdrawal(account_factory):
    new_account =account_factory(account_id=17, balance=15)
    with pytest.raises(ValueError):
        new_account.withdraw(20)
    assert new_account.get_balance() == 15



def test_get_balance_after_transfer(account_factory):
    new_account =account_factory(account_id=18, balance=100)
    new_account2 =account_factory(account_id=19, balance=100)
    new_account.transfer(new_account2,50)
    assert new_account.get_balance() == 50
    assert new_account2.get_balance() == 150
    


# Bonus parametrize
@pytest.mark.parametrize("initial_balance, deposit_amount, expected_balance", [
    (100, 50, 150),
    (200, 100, 300),
    (0, 100, 100),
])
def test_deposit(account_factory, initial_balance, deposit_amount, expected_balance):
    account = account_factory(account_id=1, balance=initial_balance)
    account.deposit(deposit_amount)
    assert account.balance == expected_balance



@pytest.mark.parametrize("initial_balance, withdraw_amount, expected_balance", [
    (100, 50, 50),
    (200, 100, 100),
    (100, 100, 0),
])
def test_withdraw(account_factory, initial_balance, withdraw_amount, expected_balance):
    account = account_factory(account_id=2, balance=initial_balance)
    account.withdraw(withdraw_amount)
    assert account.balance == expected_balance
    
    

@pytest.mark.parametrize("initial_balance, transfer_amount, expected_balance", [
    (100, 50, 50),
    (200, 100, 100),
    (100, 100, 0),
])
def test_transfer(account_factory, initial_balance, transfer_amount, expected_balance):
    account1 = account_factory(account_id=3, balance=initial_balance)
    account2 = account_factory(account_id=4, balance=0)
    account1.transfer(account2, transfer_amount)
    assert account1.balance == expected_balance
    assert account2.balance == transfer_amount