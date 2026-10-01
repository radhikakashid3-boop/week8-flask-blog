import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-this-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///blog.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 6

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.environ.get("MAIL_DEFAULT_SENDER")
        or os.environ.get("MAIL_USERNAME")
    )
    