import os, flask
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from web import app

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard/index.tpl')
