from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import DecimalField, FileField, StringField
from wtforms.validators import DataRequired


class GigsUpload(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    picture = FileField("Picture", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
