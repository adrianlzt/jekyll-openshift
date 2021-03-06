#!/usr/bin/env python

import falcon
import os
from datetime import datetime
from wsgiref import simple_server

FILE="/tmp/app/web.md" # coger de venv

class EventReceiver(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = os.getenv("OPENSHIFT_BUILD_NAME")

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/plain'

        if not os.path.exists("/tmp/app"):
            os.mkdir("/tmp/app")

        body = str(req.stream.read())
        with open(FILE, "a") as fd:
            fd.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+body+"\n")
        resp.body = "Informacion guardada"

application = falcon.API()
application.add_route('/', EventReceiver())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
