import os
import os.path
import urllib.request
import json
import cherrypy
import base64
import nacl.encoding
import nacl.signing

LISTENING_IP = "193.168.1.13"
LISTENING_PORT = 80

api_key = 0
apiHeader = 0
username = 0
privateKey = 0
publicKey = 0


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

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return "YOU SHALL NOT PASS - Gandalf <br> Stop trying to access my endpoints via browser"

    @cherrypy.expose
    def endpoint(self):
        data = cherrypy.request.body.read()
        data_json = json.loads(data.decode('utf-8'))
        print("-----")
        print(data_json['a'])
        print("-----")
        return "Helo"

    @cherrypy.expose
    def check_privatedata(self):
        url = "http://cs302.kiwi.land/api/get_privatedata"

        try:
            req = urllib.request.Request(url, headers=apiHeader)
            response = urllib.request.urlopen(req)
            data = response.read()  # read the received bytes
            # load encoding if possible (default to utf-8)
            encoding = response.info().get_content_charset('utf-8')
            response.close()
        except urllib.error.HTTPError as error:
            error = error.read()
            error_json = json.loads(error.decode('utf-8'))
            return "0"

        JSON_object = json.loads(data.decode(encoding))
        return(JSON_object['response'])
        # return("error")

    @cherrypy.expose
    def newPrivateData(self):

        # GLOBALS
        url = "http://cs302.kiwi.land/api/add_pubkey"
        global privateKey
        global publicKey
        global username
        # PRIVATE KEY
        hex_key = nacl.signing.SigningKey.generate().encode(
            encoder=nacl.encoding.HexEncoder)
        signing_key = nacl.signing.SigningKey(
            hex_key, encoder=nacl.encoding.HexEncoder)
        # PUBLIC KEY
        pubkey_hex = signing_key.verify_key.encode(
            encoder=nacl.encoding.HexEncoder)
        pubkey_hex_str = pubkey_hex.decode('utf-8')
        # GLOBAL VARIABLES
        privateKey = hex_key
        publicKey = pubkey_hex_str
        # SIGNATURE
        message_bytes = bytes(pubkey_hex_str + username, encoding='utf-8')
        signed = signing_key.sign(
            message_bytes, encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')

        payload = {
            "pubkey": pubkey_hex_str,
            "username": username,
            "signature": signature_hex_str,
        }

        try:
            req = urllib.request.Request(url, data=bytes(
                json.dumps(payload), 'utf-8'), headers=apiHeader)
            response = urllib.request.urlopen(req)
            data = response.read()  # read the received bytes
            # load encoding if possible (default to utf-8)
            encoding = response.info().get_content_charset('utf-8')
            response.close()
        except urllib.error.HTTPError as error:
            print(error.read())

        return(Api.report(self,status="online"))

    def report(self, status):

        payload = {
            "connection_address": LISTENING_IP,
            "connection_location": "2",
            "incoming_pubkey": publicKey,
            "status": str(status)
        }
        url = "http://cs302.kiwi.land/api/report"
        try:
            req = urllib.request.Request(url, data=bytes(
                json.dumps(payload), 'utf-8'), headers=apiHeader)

            response = urllib.request.urlopen(req)
            data = response.read()  # read the received bytes
            # load encoding if possible (default to utf-8)
            encoding = response.info().get_content_charset('utf-8')
            response.close()
        except urllib.error.HTTPError as error:
            print("------------")
            print(error.read())
            print("------------")

        JSON_object = json.loads(data.decode(encoding))
        return(JSON_object['response'])

    @cherrypy.expose
    def ping(self):
        url = "http://cs302.kiwi.land/api/ping"

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)

        data = response.read()
        response.close()
        return(data)

    @cherrypy.expose
    def logout(self):
        global apiHeader
        global username
        global api_key

        print(apiHeader)
        print(username)
        print(api_key)
        apiHeader = 0
        username = 0
        api_key = 0
        return "1"

    @cherrypy.expose
    def login(self):
        global username
        global api_key
        data = cherrypy.request.body.read()
        data_json = json.loads(data.decode('utf-8'))
        print(data_json)
        username = data_json['user']

        url = "http://cs302.kiwi.land/api/load_new_apikey"

        credentials = ('%s:%s' % (data_json['user'], data_json['pass']))
        b64_credentials = base64.b64encode(credentials.encode('ascii'))
        headers = {
            'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
            'Content-Type': 'application/json; charset=utf-8',
        }

        try:
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            data = response.read()  # read the received bytes
            # load encoding if possible (default to utf-8)
            encoding = response.info().get_content_charset('utf-8')
            response.close()
        except urllib.error.HTTPError as error:
            error = error.read()
            error_json = json.loads(error.decode('utf-8'))
            return "0"

        JSON_object = json.loads(data.decode(encoding))
        api_key = JSON_object['api_key']
        Api.setAPIHeader(self)
        return "1"

    def setAPIHeader(self):
        global apiHeader
        apiHeader = {
            'X-username': username,
            'X-apikey': api_key
        }

config = {
    'global': {'server.socket_host': '127.0.0.1',
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
