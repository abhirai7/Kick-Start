from __future__ import annotations

import sqlite3

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, Length


class EditProfileForm(FlaskForm):
    def __init__(self, connection: sqlite3.Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = connection

    first_name = StringField("First Name", validators=[DataRequired(), Length(max=32)])
    last_name = StringField("Last Name", validators=[Length(max=32)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=128)])
    phone = TelField("Phone", validators=[Length(max=10)])
    address = StringField("Address", validators=[Length(max=128)])

    skills = StringField("Skills")
    experience = StringField("Experience")
    website = StringField("Website", validators=[Length(max=128)])

    language = StringField("Language", validators=[Length(max=32)])
    timezone = StringField("Timezone", validators=[Length(max=32)])

    submit = SubmitField("Update Profile")
