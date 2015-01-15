from reactor import component
from reactor import utils
from reactor.models.plugin import Plugin
from reactor.event import Event

from gevent import monkey
import gevent

import socketio

print socketio.__version__

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

monkey.patch_all()

import os

import logging
logger = logging.getLogger("WebsocketPlugin")

class TestNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def sendhello():
            while True:
                self.emit('hello', {'world': True})
                gevent.sleep(0.1)

        self.spawn(sendcpu)


class SocketIOApplication(object):
    def __init__(self):
        self.buffer = []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/') or 'index.html'

        if path.startswith('static/') or path == 'index.html':
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("socket.io"):
            socketio_manage(environ, {'/test': TestNamespace})
        else:
            return not_found(start_response)

def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']

class WebsocketPlugin(Plugin):
    
  def __init__(self):
    Plugin.__init__(self, "@websocket")
    
  def run(self):

     # initialize
    self.init()
    logger.info("Plugin started. PID: " + str(os.getpid()))

    logger.debug('Listening on port http://0.0.0.0:3333 and on port 10843 (flash policy server)')

    SocketIOServer(('0.0.0.0', 3333), SocketIOApplication(),
      resource="socket.io", policy_server=True,
      policy_listener=('0.0.0.0', 10843)).serve_forever()

       
         