import os, flask
from flask import render_template, request, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from web import app

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
  try:
    socketio_manage(request.environ, {'/test': TestNamespace}, request)
  except:
    app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
  return Response()

#@app.route('/socket.io/<path:path>')
#def run_socketio(path):
#  socketio_manage(
#    request.environ, {'/test': TestNamespace})
#  return ''

class TestNamespace(BaseNamespace, BroadcastMixin):
  def recv_connect(self):
    def sendhello():
      while True:
        self.emit('hello', {'world': True})
        gevent.sleep(0.1)

    self.spawn(sendhello)