from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from src import app, conn
from src.forms import LoginForm
from src.user import User


@app.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm(conn)
    if form.validate_on_submit():

        user = User.from_email(conn, email=form.email.data, password=form.password.data)

        if user is None:
            return redirect(url_for("login"))
        
        login_user(user)
        
        return redirect(url_for("index"))

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
