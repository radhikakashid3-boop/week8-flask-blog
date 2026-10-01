from email.message import EmailMessage
import smtplib
from urllib.parse import urlsplit

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app import db
from app.auth import bp
from app.auth.forms import (
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm
)
from app.models import User


def send_password_reset_email(recipient, reset_url):
    server = current_app.config.get("MAIL_SERVER")
    port = current_app.config.get("MAIL_PORT")
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    sender = current_app.config.get("MAIL_DEFAULT_SENDER")
    use_tls = current_app.config.get("MAIL_USE_TLS")

    if not server or not sender:
        current_app.logger.info(
            "Password reset link for %s: %s",
            recipient,
            reset_url
        )

        print("\n" + "=" * 70)
        print("PASSWORD RESET LINK")
        print(reset_url)
        print("=" * 70 + "\n")

        return

    message = EmailMessage()

    message["Subject"] = "Reset your My Personal Blog password"
    message["From"] = sender
    message["To"] = recipient

    message.set_content(
        f"""Hello,

We received a request to reset your password.

Use the following link to reset it:

{reset_url}

This link expires in 30 minutes.

If you did not request this, you can safely ignore this email.

Regards,
My Personal Blog
"""
    )

    try:
        with smtplib.SMTP(
            server,
            port,
            timeout=10
        ) as smtp:

            if use_tls:
                smtp.starttls()

            if username and password:
                smtp.login(
                    username,
                    password
                )

            smtp.send_message(message)

    except (OSError, smtplib.SMTPException) as error:
        current_app.logger.exception(
            "Unable to send password reset email: %s",
            error
        )

        if current_app.debug:
            print("\n" + "=" * 70)
            print("PASSWORD RESET LINK")
            print(reset_url)
            print("=" * 70 + "\n")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )

        user.set_password(
            form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Your account has been created successfully.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        title="Create Account",
        form=form
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data.strip()

        user = User.query.filter_by(
            username=username
        ).first()

        if user is None or not user.check_password(
            form.password.data
        ):
            flash(
                "Invalid username or password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(
            user,
            remember=form.remember_me.data
        )

        user.last_seen = db.func.now()
        db.session.commit()

        next_page = request.args.get("next")

        if (
            not next_page
            or urlsplit(next_page).netloc
        ):
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template(
        "auth/login.html",
        title="Login",
        form=form
    )


@bp.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()

        flash(
            "You have been logged out.",
            "info"
        )

    return redirect(
        url_for("main.index")
    )


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        user = User.query.filter_by(
            email=email
        ).first()

        if user is not None:

            token = user.get_reset_token()

            reset_url = url_for(
                "auth.reset_password",
                token=token,
                _external=True
            )

            send_password_reset_email(
                user.email,
                reset_url
            )

        flash(
            "If an account exists for that email, "
            "a password reset link has been generated.",
            "info"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/forgot_password.html",
        title="Forgot Password",
        form=form
    )


@bp.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    user = User.verify_reset_token(token)

    if user is None:

        flash(
            "The reset link is invalid or has expired.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.set_password(
            form.password.data
        )

        db.session.commit()

        flash(
            "Password reset successfully. "
            "You can now log in.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/reset_password.html",
        title="Reset Password",
        form=form
    )
    