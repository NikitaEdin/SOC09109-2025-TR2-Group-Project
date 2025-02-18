from flask import render_template

from app import app

@app.route("/wizard/plot", methods=['GET', 'POST'])
def wizard_plot():
    return render_template('/wizard/plot.html')

@app.route("/wizard/getting_started", methods=['GET', 'POST'])
def wizard_getting_started():
    return render_template('/wizard/getting_started.html')