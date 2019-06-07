import time
import centralAPI
import clientAPI
import helper
import json
import cherrypy
import database

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
    def rx_broadcast(self):
        rawbody = cherrypy.request.body.read()
        body = json.loads(rawbody)

        try:
            if body['loginserver_record'] and body['message'] and body['sender_created_at'] and body['signature']:
                record_inparts = helper.splitServerRecord(body['loginserver_record'])
                if(len(record_inparts) == 4):
                    if(record_inparts[3] == body['signature']):
                        database.updatePublicMessages(record_inparts[0], body['message'], body['sender_created_at'])
                        payload = {
                            'response': 'ok'
                        }
                    else:
                        payload = {
                            'response': 'error',
                            'message': 'invalid body, signature does not match'
                        }
                else:
                    payload = {
                        'response': 'error',
                        'message': 'invalid body, server record length'
                    }
        except KeyError as error:
            payload = {
                'response': 'error',
                'message': 'invalid body,  missing required parameters'
            }
        #return bytes(json.dumps(payload), 'utf-8')
        return json.dumps(payload)

    @cherrypy.expose
    def ping_check(self):
        ##### FURTHER FILTER FOR ONLINE USERS BY RECIEVED PAYLOAD
        ###### MAKE IT DUAL (MAKE FRONT END SEND USERNAME)###########
        rawbody = cherrypy.request.body.read()
        try:
            body = json.loads(rawbody)
        except:
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }
            return json.dumps(payload)
        try:
            if body['my_time'] and body['connection_address'] and body['connection_location']:
                payload = {
                    'response': 'ok',
                    'my_time': str(time.time()),
                }
        except KeyError as error:
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }
        #return bytes(json.dumps(payload), 'utf-8')
        return json.dumps(payload)

    @cherrypy.expose
    def rx_privatemessage(self):
        rawbody = cherrypy.request.body.read()
        try:
            body = json.loads(rawbody)
        except:
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }
            return json.dumps(payload)
        
        try:
            if body['loginserver_record'] and body['target_pubkey'] and body['target_username'] and body['encrypted_message'] and body['sender_created_at'] and body['signature']:
                payload = {
                    'response': 'ok',
                }
        except KeyError as error:
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }

        return json.dumps(payload)
