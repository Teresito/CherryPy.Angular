import os
import os.path
import random
import string

import cherrypy


class Main(object):

    @cherrypy.expose
    def default(self):
        Main.index(self)

    @cherrypy.expose
    def index(self):
        return open('./public/bundled/index.html')

if __name__ == '__main__':
    conf = {
        'global': {'server.socket_host': '192.168.1.6',
                   'server.socket_port': 80,
                   'engine.autoreload.on': True,
                   'server.thread_pool': 8
                   },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(Main(), '/', conf)
