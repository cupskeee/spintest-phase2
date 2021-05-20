from mongoengine import CASCADE
from .wallets import Wallets
from .users import Users


Users.register_delete_rule(Wallets, 'user', CASCADE)
