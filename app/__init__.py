from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    # Set up login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import User  # Import User model for login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register Blueprints
    from app.routes.main import main
    from app.routes.auth import auth_bp
    from app.routes.repository import repo_bp
    from app.routes.file import file_bp

    app.register_blueprint(main)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(repo_bp, url_prefix="/repository")
    app.register_blueprint(file_bp, url_prefix="/file")

    return app