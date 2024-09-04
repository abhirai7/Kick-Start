from __future__ import annotations

import sqlite3

from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from src.user import User


class RegisterForm(FlaskForm):
    def __init__(self, connection: sqlite3.Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = connection

    email = EmailField("", validators=[DataRequired(), Email()])
    password = PasswordField("", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "", validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Register")

    def validate_email(self, email: EmailField):
        assert email.data

        str_email = email.data.lower()

        if User.exists(self.conn, email=str_email):
            raise ValidationError("Email already registered")

        return True

    def validate_phone(self, phone: IntegerField):
        return self._validate_integer_len(
            phone, 10, "Phone number must be 10 digits long"
        )

    def validate_pincode(self, pincode: IntegerField):
        assert pincode.data

        return self._validate_integer_len(pincode, 6, "Pincode must be 6 digits long")

    def _validate_integer_len(
        self, field: IntegerField, hard_limit: int, error_message: str
    ):
        phone_str = str(field.data)
        if len(phone_str) != hard_limit:
            raise ValidationError(error_message)
        return True
