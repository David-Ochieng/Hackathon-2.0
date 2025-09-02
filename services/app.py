from flask import Flask
from config import Config
from models import db
from flask_cors import CORS
import stripe

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Init DB
    db.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.entries import entries_bp
    from routes.payments import payments_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(entries_bp, url_prefix="/api/entries")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")

    # Initialize stripe module with key if present
    if app.config.get("STRIPE_SECRET_KEY"):
        stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route("/healthz")
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

