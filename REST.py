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
        url = "http://cs302.kiwi.land/api/ping"

        #create request and open it into a response object
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)

        #read and process the received bytes
        data = response.read() 
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close() #be a tidy kiwi


        JSON_object = json.loads(data.decode(encoding))
        print(type(JSON_object))
        return(data)

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