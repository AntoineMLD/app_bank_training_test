from bank import Account, Transaction
from init_db import setup_database

session = setup_database()
Session = session()


client1 = Account(account_id=1,balance=100,session=Session)
Session.add_all([client1])

client1.get_balance()
client2 = Account(account_id=2,balance=50,session=Session)
Session.add_all([client2])

client2.get_balance()
client1.transfer(client2,50)
