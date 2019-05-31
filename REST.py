import random
import string
import urllib.request
import json

import cherrypy
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200" 
    cherrypy.response.headers["Access-Control-Allow-Headers"] = \
    "content-type, Authorization, X-Requested-With"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = 'GET, POST'

@cherrypy.expose
class StringGeneratorWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return "Hello"

    def POST(self, length=8):
        return "Hello"

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.CORS.on': True,
        }
    }
    cherrypy.tree.mount(StringGeneratorWebService(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()