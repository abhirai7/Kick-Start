from __future__ import annotations

from flask import redirect, render_template, url_for
from flask_login import current_user

from src import app


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/home")
def home():
    return redirect(url_for("index"))
