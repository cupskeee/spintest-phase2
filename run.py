from app import app

app.run(
    host=app.config["APP_HOST"],
    port=app.config["APP_PORT"],
    debug=app.config["APP_DEBUG"]
)