from __future__ import annotations

import sqlite3

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from src.user import User


class LoginForm(FlaskForm):
    def __init__(self, connection: sqlite3.Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = connection
        self.user: User | None = None

    email = EmailField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])

    submit = SubmitField("Login")

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False

        assert self.email.data and self.password.data

        try:
            user = User.from_email(
                self.conn, email=self.email.data, password=self.password.data
            )
        except ValueError:
            return False
        else:
            self.user = user

        return True
