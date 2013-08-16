#!/usr/bin/env python

# Run this with
# Serves by default at
#from django_import import *
from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.autoreload
import tornado.web
import tornado.wsgi
import os
import sys
from django.conf import settings

pwd = os.getcwd()
sys.path.insert(0, os.path.join(pwd, "libs"))
sys.path.insert(0, os.path.join(pwd, "ui_framework"))
print sys.argv

define('port', type=int, default=int(sys.argv[1]))

#The following is a must, otherwise, admin for each app will not be loaded in tonado server.
from django_setup import gen_spec
gen_spec(settings, {"includes":[], "include_files":[]})

def main():
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(settings.RUNNING_PATH, "static")}),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    if True:
        print "Starting tornado server on: %d"%int(sys.argv[1])
        tornado.ioloop.IOLoop.instance().start()
    else:
        loop=tornado.ioloop.IOLoop.instance() 
        tornado.autoreload.start(loop)
        print "Starting server on: %d"%int(sys.argv[1])
        loop.start()

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rootapp.settings")
    main()