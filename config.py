# App Settings
APP_HOST = "0.0.0.0"
APP_PORT = 5000
APP_DEBUG = True
# This Secret key is a Base64 form of 'spintest'
SECRET_KEY = 'c3BpbnRlc3Q='
JWT_SECRET_KEY = 'c3BpbnRlc3Q='
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Flask-MongoEngine
MONGODB_SETTINGS = {
    'db': 'spintestdb',
    'host': '127.0.0.1',
    'port': 27017
}

# Flask-WTF Settings
WTF_CSRF_CHECK_DEFAULT = False