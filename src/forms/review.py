from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import DataRequired


class ProjectReview(FlaskForm):
    rating = IntegerField("Rating", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])


class GigReview(FlaskForm):
    rating = IntegerField("Rating", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])


class ProfileReview(FlaskForm):
    rating = IntegerField("Rating", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])
