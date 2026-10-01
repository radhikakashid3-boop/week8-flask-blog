import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates")
    )

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix="/posts")

    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp, url_prefix="/comments")

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "404.html",
            title="Page Not Found"
        ), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()

        return render_template(
            "500.html",
            title="Server Error"
        ), 500

    return app