from __future__ import annotations

from src import conn, login_manager
from src.user import User


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    user_id = int(user_id)

    try:
        return User.get(conn, user_id)
    except ValueError:
        return None


@login_manager.request_loader
def load_user_from_request(request) -> User | None:
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:
        try:
            return User.from_email(conn, email=email, password=password)
        except ValueError:
            return None

    return None
