from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import current_user

from src import app, conn
from src.user import User
from src.forms import RegisterForm


@app.route("/register", methods=["GET", "POST"])
def register():
    form: RegisterForm = RegisterForm(conn)
    if form.validate_on_submit():

        email = form.email.data.lower()
        password = form.password.data

        User.create(conn, email=email, password=password)

        return redirect(url_for("login"))

    return render_template("register.html", form=form, current_user=current_user)
