from flask import redirect, url_for
from werkzeug import Response

from src import login_manager
from src.models import User


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    user_id = int(user_id)

    try:
        return User.query.get(user_id)

    except ValueError:
        return None


@login_manager.unauthorized_handler
def unauthorized() -> Response:
    return redirect(url_for("login_route"))


@login_manager.request_loader
def load_user_from_request(request) -> User | None:
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:
        try:
            user = User.query.filter_by(email=email).first()
            return user
        except ValueError:
            return None

    return None
