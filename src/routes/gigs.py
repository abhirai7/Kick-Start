from __future__ import annotations

from typing import TYPE_CHECKING

from flask import redirect, render_template, url_for, session
from flask_login import current_user, login_required

from src import app
from src.forms import GigsUpload, GigReview

if TYPE_CHECKING:
    from src.user import User

    assert isinstance(current_user, User)


@app.route("/gigs/add")
@login_required
def gigs_add():
    form: GigsUpload = GigsUpload()

    if form.validate_on_submit():
        gig = current_user.add_gig(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            picture=form.picture.data.read(),
        )
        session["gig"] = gig
        return redirect(url_for("home"))

    return render_template("add.html", current_user=current_user)


@app.route("/gigs/<int:id>/review/add")
@login_required
def gigs_review_add(id: int):
    gig = current_user.get_gig(id)

    if gig is None:
        return redirect(url_for("home"))

    return render_template("review.html", gig=gig, current_user=current_user)