from app import app, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms.editUserDetails import EditUserDetails

# Settings page
@app.route("/settings")
@login_required
def settings():
    return render_template('/profile/settings.html', title='Settings', user=current_user)

# User's profile page
@app.route("/profile")
@login_required
def profile():
    return render_template('/profile/user_profile.html', title='My Profile', user=current_user)

# Edit user's details page
@app.route("/profile/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditUserDetails()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        # CHange password if user inputs
        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash("Your details have been updated successfully!", "success")
        return redirect(url_for("profile"))

    # Fill form with user details
    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template("profile/edit_details.html", form=form, title='Edit Details', user=current_user)
