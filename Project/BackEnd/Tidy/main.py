import os
import os.path
import urllib.request
import cherrypy
import json
import helper
import centralAPI 



LISTENING_IP = "192.168.1.6"

#LISTENING_IP = "http://302cherrypy.mynetgear.com/"
LISTENING_PORT = 80


def cors():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

def wat():
    print("WAT")
    return False

cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
cherrypy.tools.wat = cherrypy._cptools.HandlerTool('before_handler',wat)


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
        self.apikey = None
        self.privateData = None
        self.privateKey = None
        self.publicKey = None
        self.newData = None
        self.EDKey = None

    def isLoggedIn(self):
        if(self.apikey == None or self.username == None):
            print("-----------------------------------")
            print("NOT LOGGED IN")
            print("-----------------------------------")
            return False
        else:
            return True

    def isBodyEmpty(self, byteData):
        if(byteData != b''):
            return False
        else:
            return True
    # Using header to get IP, i can block their requests to this end point
    # One of the reasons is to minimise frontend pinging hammond/central server
    @cherrypy.expose
    def onlineUsers(self):
        if(self.isLoggedIn() == False):
            return '0'

        centralResponse = centralAPI.list_users(self.apikey,self.username)
        if(centralResponse['response'] == 'ok'):
            users = centralResponse['users']
            
            return json.dumps(centralResponse)
        else:
            return '0'


    @cherrypy.expose
    #@cherrypy.tools.allow(methods=['POST'])
    def login(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))

        centralResponse = centralAPI.load_new_apikey(body_json['user'], body_json['pass'])
        if(centralResponse['response'] == "ok"):
            self.apikey = centralResponse['api_key']
            self.username = body_json['user']
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def check_privatedata(self):
        if(self.isLoggedIn() == False):
            return '0'
        centralResponse = centralAPI.get_privatedata(self.apikey, self.username)
        if(centralResponse['response'] == "ok"):
            self.privateData = centralResponse['privatedata']
            return '1'
        else:
            return '0'

    # Need to check if they're logged in
    @cherrypy.expose
    def unlock_privatedata(self):
        if(self.isLoggedIn() == False):
            return '0'

        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        decryptKey = body_json['decryptionKey']
        unlockedData = helper.decryptData(self.privateData,decryptKey)
        if(unlockedData != "error"):
            self.privateData = unlockedData
            privateKeyData = unlockedData['prikeys']
            self.privateKey = privateKeyData[0]
            self.publicKey = helper.generatePubKey(self.privateKey)
            self.EDKey = decryptKey
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def logout(self):
        if(self.newData == True):
            userdata_ecrypted = helper.encryptData(self.privateData,self.EDKey)
            centralResponse = centralAPI.add_privatedata(self.apikey,self.username,userdata_ecrypted,self.privateKey)
            if(centralResponse['response']=="error"):
                return '0'
        centralResponse = centralAPI.report(self.apikey,self.username,"LOCATION N/A","2",self.publicKey,"offline")        
        self.username = None
        self.apikey = None
        self.privateData = None
        self.privateKey = None
        self.publicKey = None
        self.newData = None
        self.EDKey = None        
        return '1'
    @cherrypy.expose
    def add_pubkey(self):
        if(self.isLoggedIn() == False):
            return '0'

        self.newData = True
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        centralResponse = centralAPI.add_pubkey(self.apikey,self.username)
        if(centralResponse == "Request Error"):
            return '0'
        else:
            self.EDKey = body_json['encryptionKey']
            self.privateKey = centralResponse['private_key']
            self.publicKey = centralResponse['public_key']
            centralPing = centralAPI.ping()
            if(centralPing['response']=='ok'):
                return '1'
            else:
                return '0'


    @cherrypy.expose
    def report_user(self):
        if(self.isLoggedIn() == False):
            return '0'
        centralResponse = centralAPI.report(self.apikey,self.username,"LOCATION N/A","2",self.publicKey,"online")
        if(centralResponse['response']=='ok'):
            return '1'
        else:
            return '0'
config = {
    'global': {'server.socket_host': LISTENING_IP,
               'server.socket_port': LISTENING_PORT,
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
    # '/api':{
    # }
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
