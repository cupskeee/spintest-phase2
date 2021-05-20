import rq
from redis import Redis
from flask import Flask, jsonify

from .extensions import (
    db,
    jwt
)

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
jwt.init_app(app)
app.redis = Redis.from_url(app.config["REDIS_URL"])
app.task_queue = rq.Queue('spintest2', connection=app.redis)

@app.errorhandler(401)
@jwt.unauthorized_loader
def unauthorized(e):
    return jsonify({"status": "failed", "msg": "Unauthorized.", "desc": "The provided credentials does not match our "
                                                                        "records"}), 401


@jwt.invalid_token_loader
def invalid_token(e):
    return jsonify({"status": "failed", "msg": "Forbidden.", "desc": "You are not authorized to take this action"}), 403


@app.errorhandler(403)
def forbidden(e):
    return jsonify({"status": "failed", "msg": "Forbidden.", "desc": "You are not authorized to take this action"}), 403


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": "failed", "msg": "Oops...It looks like you're lost.", "desc": "We couldn't find this "
                                                                                            "resource",
                    "detail": str(e)}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"status": "failed", "msg": "There was a problem with your request", "desc": "Your client has "
                                                                                                "issued a malformed "
                                                                                                "or illegal request",
                    "detail": str(e)}), 400


@app.errorhandler(410)
def gone(e):
    return jsonify({"status": "failed", "msg": "Gone.", "desc": "The resource requested is no longer available and "
                                                                "will not be available again.", "detail": str(e)}), 410


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"status": "failed", "msg": "Oops...Something went wrong.", "desc": "Try to refresh this page or "
                                                                                       "feel free to contact us if "
                                                                                       "the problem presist",
                    "detail": str(e)}), 500