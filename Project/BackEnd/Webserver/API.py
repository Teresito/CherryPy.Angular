import time
import centralAPI
import clientAPI
import helper
import json
import cherrypy

class Interface(object):

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Interface.index(self)

    @cherrypy.expose
    def index(self):
        response = {'response': 'error', 'message': 'Invalid access point'}
        response_JSON = json.dumps(response)
        return response_JSON


    @cherrypy.expose
    def ping_check(self):
        ##### FURTHER FILTER FOR ONLINE USERS BY RECIEVED PAYLOAD
        ###### MAKE IT DUAL (MAKE FRONT END SEND USERNAME)###########
        rawbody = cherrypy.request.body.read(None,None)
        body = json.loads(rawbody)
        print(body)
        payload = {
            'response': 'ok',
            'message': 'N/A',
            'my_time': str(time.time()),
            'my_active_usernames': 'N/A',
        }
        #return bytes(json.dumps(payload), 'utf-8')
        return json.dumps(payload)

    @cherrypy.expose
    def rx_privatemessage(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))

        payload = {
            'response': 'ok',
            'message': 'N/A'
        }

        return bytes(json.dumps(payload), 'utf-8')        
