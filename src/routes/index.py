from __future__ import annotations

from flask import redirect, render_template, session, url_for
from flask_login import current_user, login_required

from src import app, conn, services
from src.gig import Gig


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html", current_user=current_user, session=session, gigs=Gig.all(conn), services=services
    )


@app.route("/home")
def home():
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name="RITIK", current_user=current_user, services=services)


@app.route("/profile-tab")
def profile_tab():
    return render_template("profile-tab.html", current_user=current_user, services=services)