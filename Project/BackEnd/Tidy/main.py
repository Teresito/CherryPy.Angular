import os
import os.path
import urllib.request
import cherrypy
import loginAPI
import json
from cherrypy import _cperror



LISTENING_IP = "127.0.0.1"
LISTENING_PORT = 80
def cors():
    if cherrypy.request.method == 'OPTIONS':
        # preflign request
        # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers[
            'Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        # tell CherryPy no avoid normal handler
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)


class Main(object):

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Main.index(self)

    @cherrypy.expose
    def index(self):
        return open('./bundled/index.html')


@cherrypy.config(**{'tools.cors.on': True})
class Api:
    def __init__(self):
        self.username = None
        self.apikey= None
        self.privateData= None
        self.privateKey= None
        self.publicKey= None

    def isBodyEmpty(self, byteData):
        if(byteData != b''):
            return False
        else:
            return True
    # Using header to get IP, i can block their requests to this end point
    # One of the reasons is to minimise frontend pinging hammond/central server
    @cherrypy.expose
    #@cherrypy.tools.allow(methods=['POST'])
    def login(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        
        loginResponse = loginAPI.load_new_apikey(body_json['user'],body_json['pass'])
        if(loginResponse['response']=="ok"):
            Api.apikey = loginResponse['api_key']
            Api.username = loginResponse['user']
            print(Api.apikey)
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def check_privatedata(self);
        loginResponse = loginAPI.check_privatedata(Api.apikey,Api.username)
        if(loginResponse['response']=="ok"):
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def add_pubkey(self):

config = {
    'global': {'server.socket_host': LISTENING_IP,
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
        'tools.staticdir.dir': './bundled',
    },
}

if __name__ == '__main__':
    #cherrypy.quickstart(Api(), '/api', config)
    cherrypy.tree.mount(Main(), '/', config)
    cherrypy.quickstart(Api(), '/api', config)
    cherrypy.engine.signals.unsubscribe()
    # Start the web server
    cherrypy.engine.start()

    # And stop doing anything else. Let the web server take over.
    cherrypy.engine.block()
