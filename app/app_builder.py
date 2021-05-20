from flask import Flask

from .extensions import (
    db,
    jwt
)

app = Flask(__name__)
app.config.from_object('config')
db.init_app()
jwt.init_app(app)