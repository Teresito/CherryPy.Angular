import time
import centralAPI
import clientAPI
import helper
import json
import cherrypy
import message_handler

class Interface(object):

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Interface.index(self)

    @cherrypy.expose
    def index(self):
        print("====================")
        print("BAD ACCESS POINT")
        print("====================")
        response = {'response': 'error', 'message': 'Invalid access point'}
        response_JSON = json.dumps(response)
        return response_JSON

    @cherrypy.expose
    def rx_broadcast(self):
        print("====================")
        print("RX_BROADCAST MESSAGE CALLED")
        print("====================")
        rawbody = cherrypy.request.body.read()      

        try:
            body = json.loads(rawbody)
            if body['loginserver_record'] and body['message'] and body['sender_created_at'] and body['signature']:
                record_inparts = helper.splitServerRecord(body['loginserver_record'])
                message_handler.updatePublicMessages(
                    record_inparts[0], body['message'], body['sender_created_at'], body['loginserver_record'], body['signature'])
                payload = {
                    'response': 'ok'
                }
                print("====================")
                print("PUBLIC MESSAGE SUCCESS")
                print("====================")
            else:
                payload = {
                    'response': 'error',
                    'message': 'invalid body,  missing required parameters'
                }
        except Exception as error:
            payload = {
                'response': 'error',
                'message': 'invalid body,  missing required parameters'
            }
        #return bytes(json.dumps(payload), 'utf-8')
        return json.dumps(payload)

    @cherrypy.expose
    def ping_check(self):
        print("====================")
        print("PING_CHECK MESSAGE CALLED")
        print("====================")
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
                print("====================")
                print("PING_CHECK SUCCESS")
                print("====================")
            else:
                payload = {
                    'response':'error',
                    'message':'invalid body, missing required parameters'
                }
        except Exception as error:
            print("====================")
            print(error)
            print("====================")
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }
        return json.dumps(payload)

    @cherrypy.expose
    def rx_privatemessage(self):
        print("====================")
        print("RX_PRIVATE MESSAGE CALLED")
        print("====================")
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
                print("====================")
                print("PRIVATE MESSAGE SUCCESS")
                print("====================")
        except Exception as error:
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }

        return json.dumps(payload)
