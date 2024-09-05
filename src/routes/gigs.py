from __future__ import annotations

from typing import TYPE_CHECKING

from flask import redirect, render_template, session, url_for
from flask_login import current_user, login_required

from src import app
from src.forms import GigReview, GigsUpload

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
    form: GigReview = GigReview()
    gig = current_user.get_gig(id)

    if gig is None:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        current_user.add_gig_review(
            gig, rating=form.rating.data, review=form.review.data
        )

    return render_template("review.html", gig=gig, current_user=current_user)


@app.route("/gigs/<int:id>/delete")
@login_required
def gigs_delete(id: int):
    current_user.delete_gig(id)

    return redirect(url_for("home"))


@app.route("/gigs/user/<int:id>/all")
@login_required
def gigs_user_all(id: int):
    gigs = current_user.get_gigs(id)

    return render_template("gigs.html", gigs=gigs, current_user=current_user)
