from __future__ import annotations

from typing import TYPE_CHECKING

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src import app
from src import conn as db_connection
from src.forms import EditProfileForm
from src.user import User

if TYPE_CHECKING:
    assert isinstance(current_user, User)


@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form: EditProfileForm = EditProfileForm(
        connection=db_connection
    )  # Pass the SQLite connection
    if form.validate_on_submit():
        # Update the profile in the database
        cursor = db_connection.cursor()
        print(
            form.first_name.data,
            form.last_name.data,
            form.email.data,
            form.phone.data,
            form.address.data,
            form.skills.data,
            form.experience.data,
            form.website.data,
            form.language.data,
            form.timezone.data,
            current_user.id,
        ),
        cursor.execute(
            """
            INSERT OR REPLACE INTO PROFILES 
        """,
            (
                current_user.id,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.phone.data,
                form.address.data,
                form.skills.data,
                form.experience.data,
                form.website.data,
                form.language.data,
                form.timezone.data,
            ),
        )
        db_connection.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("edit_profile"))

    return render_template(
        "edit_profile.html",
        form=form,
        name=f"{form.first_name.data} {form.last_name.data}",
    )
