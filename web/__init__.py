import os

# Import flask and template operators
from flask import Flask, render_template

# modules
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.assets import Environment, Bundle

WEB_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the WSGI application object
app = Flask(__name__, template_folder=os.path.join(WEB_DIR, 'views/'), static_folder=os.path.join(WEB_DIR, 'static/'), static_url_path='/static')

# Configurations
app.config.from_object('config')

# init sql alchemy
db = SQLAlchemy(app)
 
# init login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# init web assets
assets = Environment(app)

assets.load_path = [
    os.path.join(WEB_DIR, 'static', 'css'),
    os.path.join(WEB_DIR, 'static', 'js'),
    os.path.join(WEB_DIR, 'static', 'vendor'),
]

assets.register(
    'app_js',
    Bundle(
        'jquery/dist/jquery.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        Bundle(
            'application.js',
            filters=['jsmin']
        ),
        output='build/app.js'
    )
)

assets.register(
    'app_css',
    Bundle(
        'bootstrap/dist/css/bootstrap.min.css',
        'fontawesome/css/font-awesome.min.css',
        'application.css',
        output='build/app.css'
    )
)

# Import a module / component using its blueprint handler variable (mod_auth)
#from app.mod_auth.controllers import mod_auth as auth_module

from web.controllers import auth
from web.controllers import dashboard

# Register blueprint(s)
#app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.tpl'), 404
