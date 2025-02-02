from app import app
from flask import render_template
from app.models import User, Role


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')
