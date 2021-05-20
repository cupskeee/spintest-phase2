import datetime
import uuid

from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine.errors import NotUniqueError

from app.helpers import (
    duplicate_phone
)
from app.models import (
    Users,
    Wallets
)
from .forms import *

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=["POST"])
def register():
    # This is the register function
    form = Registration(request.form)
    result = {"status": "success", "msg": "User successfully registered, you can start logging in"}
    if form.validate():
        try:
            user = {
                "_id": str(uuid.uuid4()),
                "first_name": form.first_name.data,
                "last_name": form.last_name.data,
                "address": form.address.data,
                "phone_number": form.phone_number.data,
                "pin": form.pin.data
            }
            user = Users(**user).save()
            Wallets(_id=str(uuid.uuid4()), user=user).save()
            result["result"] = user.serialize()
        except NotUniqueError:
            return duplicate_phone(), 400
    else:
        return abort(400, form.errors)


@auth.route('/login', methods=["POST"])
def login():
    # This is the login function
    form = Login(request.form)
    if form.validate():
        user = Users.objects(phone_number=form.phone_number.data).first()
        if user:
            auth_success = user.check_pw_hash(form.pin.data)
            if not auth_success:
                return abort(401)
            else:
                expiry = datetime.timedelta(days=5)
                access_token = create_access_token(identity=str(user.phone_number), expires_delta=expiry)
                refresh_token = create_refresh_token(identity=str(user.phone_number))
                return jsonify({'status': "success", "response": {'access_token': access_token,
                                                                  'refresh_token': refresh_token,
                                                                  'logged_in_as': "{} {}".format(user.first_name,
                                                                                                 user.last_name)}})
        else:
            return abort(401)
    else:
        return abort(400, form.errors), 400
