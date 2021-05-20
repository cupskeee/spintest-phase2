from mongoengine import CASCADE
from .tasks import Tasks
from .paymenthistory import PaymentHistory
from .transferhistory import TransferHistory
from .topuphistory import TopUpHistory
from .wallets import Wallets
from .users import Users


Users.register_delete_rule(Wallets, 'user', CASCADE)
