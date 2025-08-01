from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder="../../frontend/templates",
        static_folder="../../frontend/static"
    )
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .auth.routes import auth_bp
    from .main.routes import main_bp
    from .routes.stocks import stocks_bp
    from .routes.crypto import crypto_bp
    from .routes.scraping_bulk_deals import bulk_deals_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(stocks_bp, url_prefix="/stocks")
    app.register_blueprint(crypto_bp, url_prefix="/crypto")
    app.register_blueprint(bulk_deals_bp, url_prefix="/bulk_deals")

    return app
