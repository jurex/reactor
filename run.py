#!/usr/bin/python

import sys

if __name__ == '__main__':

  if len(sys.argv) > 1 and sys.argv[1] == "web":

    # import
    from web import app
    app.run(host='0.0.0.0', port=5000, debug=True)

  else:
    # import
    from reactor.app import App

    # init
    app = App()
    app.run()

