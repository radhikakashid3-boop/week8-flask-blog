import pytest

from app import create_app, db
from app.models import User, Post


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_user_password(app):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com"
        )

        user.set_password("password123")

        assert user.check_password("password123")
        assert not user.check_password("wrongpassword")


def test_user_registration(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }
    )

    assert response.status_code == 302


def test_login(client):
    client.post(
        "/auth/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 302


def test_create_post(client, app):
    client.post(
        "/auth/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }
    )

    client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/posts/create",
        data={
            "title": "Test Post",
            "content": "This is a test blog post.",
            "published": "y"
        }
    )

    assert response.status_code == 302

    with app.app_context():
        post = Post.query.first()

        assert post is not None
        assert post.title == "Test Post"


def test_404_page(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404
    