from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.models import User
from app.forms.loginForm import LoginForm
from flask_login import login_user, current_user, logout_user


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Case sensetive email check
        user = User.query.filter(User.email.ilike(form.email.data)).first()

        # Successful login?
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            flash('Welcome back ' + user.username + '!', 'success')

            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Failed to login.', 'danger')


    return render_template("/auth/login.html", title='Login', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out.', 'success')
    return redirect(url_for('home'))
