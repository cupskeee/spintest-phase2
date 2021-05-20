from app import app
from .auth import auth
# from .wallet import wallet

app.register_blueprint(auth)
# app.register_blueprint(wallet)