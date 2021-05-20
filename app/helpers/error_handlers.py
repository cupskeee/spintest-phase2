from flask import jsonify


def duplicate_phone():
    return jsonify({"result": "failed", "msg": "There was a problem with your request", "desc": "That phone number is "
                                                                                                "already registered"})


def insufficient_balance():
    return jsonify({"result": "failed", "msg": "Insufficient balance",
                    "desc": "You have insufficient balance for this transaction."})


def target_not_found():
    return jsonify({"result": "failed", "msg": "uh oh.. We couldn't wind that user",
                    "desc": "We couldn't find a user with that id."})
