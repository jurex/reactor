import os, flask
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort, g
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.wtf import Form, RecaptchaField
from wtforms import fields, TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email, InputRequired, ValidationError
from wtforms import fields

from reactor.models.user import User
from web import app, db,login_manager

class LoginForm(Form):
    username = fields.StringField(validators=[InputRequired()])
    password = fields.StringField(validators=[InputRequired()])

    # WTForms supports "inline" validators
    # which are methods of our `Form` subclass
    # with names in the form `validate_[fieldname]`.
    # This validator will run after all the
    # other validators have passed.
    def validate_password(form, field):
        try:
            user = db.session.query(User).filter(User.username == form.username.data).one()
        except (MultipleResultsFound, NoResultFound):
            flash("Invalid username or password")
            raise ValidationError("Invalid user")
        if user is None:
            flash("Invalid username or password")
            raise ValidationError("Invalid user")
        if not user.check_password_hash(form.password.data):
            flash("Invalid username or password")
            raise ValidationError("Invalid password")

        # Make the current user available
        # to calling code.
        form.user = user

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.tpl')

    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Let Flask-Login know that this user
        # has been authenticated and should be
        # associated with the current session.
        login_user(form.user)
        #flash("Logged in successfully.")
        return redirect(url_for("dashboard"))

    #flash_errors(form)
    return render_template('auth/login.tpl', form=form)

@app.route('/logout/')
@login_required
def logout():
    # Tell Flask-Login to destroy the
    # session->User connection for this session.
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('login'))
