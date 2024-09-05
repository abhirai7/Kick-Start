from __future__ import annotations

from flask import redirect, render_template, session, url_for
from flask_login import current_user, login_required

from src import app


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", current_user=current_user, session=session)


@app.route("/home")
def home():
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name="RITIK", current_user=current_user)