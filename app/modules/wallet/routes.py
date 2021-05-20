import uuid
from flask import Blueprint, jsonify, request, abort, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.helpers import (
    insufficient_balance,
    target_not_found
)

from app.models import (
    Users,
    Wallets,
    TopUpHistory,
    TransferHistory,
    PaymentHistory,
    Tasks
)
from .forms import *

wallet = Blueprint('wallet', __name__, url_prefix='/wallet')


@wallet.route('/', methods=["GET"])
@jwt_required()
def balance():
    user = Users.objects(phone_number=get_jwt_identity()).first()
    wallet = Wallets.objects(user=user).first()
    return jsonify({"result": "success", "bal": str(wallet.balance)})


@wallet.route('/topup', methods=["POST"])
@jwt_required()
def topup():
    form = TopUp(request.form)
    if form.validate():
        user = Users.objects(phone_number=get_jwt_identity()).first()
        wallet = Wallets.objects(user=user).first()
        old_balance = wallet.balance
        new_balance = old_balance + form.amount.data
        wallet.update(balance=new_balance)
        wallet["balance"] = new_balance
        topup = TopUpHistory(_id=str(uuid.uuid4()), amount=form.amount.data, wallet=wallet, balance_before=old_balance,
                             balance_after=new_balance).save()
        return jsonify({"status": "success", "result": topup.serialize()})
    else:
        return abort(400, form.errors), 400


@wallet.route('/transfer', methods=["POST"])
@jwt_required()
def transfer():
    form = Transfer(request.form)
    if form.validate():
        user = Users.objects(phone_number=get_jwt_identity()).first()
        wallet = Wallets.objects(user=user).first()
        target_user = Users.objects(_id=form.target_user.data).first()
        if not target_user:
            return target_not_found()
        target_wallet = Wallets.objects(user=target_user).first()
        if not target_wallet:
            return target_not_found()
        if wallet.balance < form.amount.data:
            return insufficient_balance()
        rq_job = current_app.task_queue.enqueue('app.modules.wallet.tasks.transfer',
                                                **{"wallet": target_wallet, "amount": form.amount.data})
        Tasks(task_id=rq_job.get_id(), name='app.modules.wallet.tasks.transfer',
              description="Transfer from {} to {}".format(user.phone_number, target_user.phone_number),
              user=user).save()
        old_balance = wallet.balance
        new_balance = wallet.balance - form.amount.data
        wallet.update(balance=new_balance)
        wallet["balance"] = new_balance
        transfer = TransferHistory(_id=str(uuid.uuid4()),
                                   amount=form.amount.data,
                                   wallet=wallet,
                                   target=target_wallet,
                                   balance_before=old_balance,
                                   balance_after=new_balance,
                                   remarks=form.remarks.data
                                   ).save()
        return jsonify({"status": "success", "result": transfer.serialize()})
    else:
        return abort(400, form.errors), 400


@wallet.route('/payment', methods=["POST"])
@jwt_required()
def payment():
    form = Payment(request.form)
    if form.validate():
        user = Users.objects(phone_number=get_jwt_identity()).first()
        wallet = Wallets.objects(user=user).first()
        if wallet.balance < form.amount.data:
            return insufficient_balance()
        old_balance = wallet.balance
        new_balance = wallet.balance - form.amount.data
        wallet.update(balance=new_balance)
        wallet["balance"] = new_balance

        payment = PaymentHistory(_id=str(uuid.uuid4()),
                                 amount=form.amount.data,
                                 wallet=wallet,
                                 balance_before=old_balance,
                                 balance_after=new_balance,
                                 remarks=form.remarks.data
                                 ).save()
        return jsonify({"status": "success", "result": payment.serialize()})
    else:
        return abort(400, form.errors), 400


@wallet.route('/test', methods=["GET"])
@jwt_required()
def test():
    user = Users.objects(phone_number=get_jwt_identity()).first()
    pipeline = [
        {
            '$match': {
                'user': user.id
            }
        }, {
            '$lookup': {
                'from': 'transfer_history',
                'localField': '_id',
                'foreignField': 'wallet',
                'as': 'transfer_history'
            }
        }, {
            '$lookup': {
                'from': 'payment_history',
                'localField': '_id',
                'foreignField': 'wallet',
                'as': 'payment_history'
            }
        }, {
            '$lookup': {
                'from': 'top_up_history',
                'localField': '_id',
                'foreignField': 'wallet',
                'as': 'top_up_history'
            }
        }
    ]
    test = Wallets.objects().aggregate(pipeline)
    data = []
    print(list(test)[0])
    # data.append(test.payment_history)
    # data.append(test.top_up_history)
    # data.append(test.transfer_history)
    # print(data)
