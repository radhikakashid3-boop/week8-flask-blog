from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError
)

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=64)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=128)
        ]
    )

    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Create Account")

    def validate_username(self, username):
        value = username.data.strip()

        user = User.query.filter_by(
            username=value
        ).first()

        if user is not None:
            raise ValidationError(
                "That username is already in use."
            )

    def validate_email(self, email):
        value = email.data.strip().lower()

        user = User.query.filter_by(
            email=value
        ).first()

        if user is not None:
            raise ValidationError(
                "That email is already registered."
            )


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    remember_me = BooleanField(
        "Remember Me"
    )

    submit = SubmitField("Login")


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6, max=128)
        ]
    )

    password2 = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Reset Password")
    