from app import app, db
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms.editUserDetails import EditUserDetails
from app.forms.changePassword import ChangePassword

# Settings page
@app.route("/settings")
@login_required
def settings():
    return render_template('/settings/settings.html', title='Settings', user=current_user)

# User's profile page
@app.route("/settings/profile")
@login_required
def profile():
    return render_template('/settings/user_profile.html', title='My Profile', user=current_user)

# Edit user's details page
@app.route("/settings/profile/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditUserDetails()

    if form.validate_on_submit():
        # CHange details if user inputs
        current_user.displayname = form.display_name.data
        current_user.email = form.email.data

        
        db.session.commit()
        flash("Your details have been updated successfully!", "success")
        return redirect(url_for("profile"))

    # Fill form with user details
    form.display_name.data = current_user.displayname
    form.email.data = current_user.email

    return render_template("settings/edit_details.html", form=form, title='Edit Details', user=current_user)


# Change Password page
@app.route("/settings/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassword()

    if form.validate_on_submit():
        # Check if the current password is correct
        if not  current_user.check_password(form.current_password.data):
            flash("Incorrect current password.", "danger")
        elif form.new_password.data != form.confirm_password.data:
            flash("New passwords do not match.", "danger")
        elif len(form.new_password.data) < 8:
            flash("New password must be 8 characters or longer.", "danger")
        else:
            # If all correct update password
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Your password has been changed successfully!", "success")
            return redirect(url_for("settings"))

    return render_template('/settings/change_password.html', form=form, title='Change Password', user=current_user)
