import time
from ExternalAPIs import centralAPI
from ExternalAPIs import clientAPI
from ExternalAPIs import helper
import json
import cherrypy

class Interface(object):
    @cherrypy.expose
    def check_privatedata(self):
        if (self.isLoggedIn() == False):
            return '0'
        centralResponse = centralAPI.get_privatedata(self.apikey, self.username)
        if (centralResponse['response'] == "ok"):
            self.privateData = centralResponse['privatedata']
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def ping_check(self):
        ##### FURTHER FILTER FOR ONLINE USERS BY RECIEVED PAYLOAD
        ###### MAKE IT DUAL (MAKE FRONT END SEND USERNAME)###########
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))

        print("===============")
        print(body_json)
        print("===============")
        payload = {
            'response': 'ok',
            'message': 'N/A',
            'my_time': str(time.time()),
            'my_active_usernames': 'N/A',
        }
        return bytes(json.dumps(payload), 'utf-8')

    @cherrypy.expose
    def rx_privatemessage(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))

        payload = {
            'response': 'ok',
            'message': 'N/A'
        }

        return bytes(json.dumps(payload), 'utf-8')        