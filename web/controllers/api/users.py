from flask.ext.restful import Resource, fields, marshal_with
from flask.ext.login import current_user, login_required
from web import app, db, api, login_manager
from web.utils import json_response
from reactor.models.user import User
from flask import jsonify

from flask.ext.classy import FlaskView

# representation
class Users(FlaskView):
  route_prefix = '/api/'
  decorators = [json_response, login_required]

  def index(self):
    return User.query().all()

  def get(self, id):
    user = User.get(id)
    return user

# register api
Users.register(app)