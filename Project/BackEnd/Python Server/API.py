import time
import centralAPI
import clientAPI
import helper
import json
import cherrypy
import message_handler

##                                                                 ##
#   Note that there are prints so I may be able to assist my peers  #
#   trying to connect to my server                                  #
##                                                                 ##

# External end points for my peers to connect to
class Interface(object):
    # Redirects for bad access point
    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Interface.index(self)
    # Peer bad access point
    @cherrypy.expose
    def index(self):
        print("====================")
        print("BAD ACCESS POINT")
        print("====================")
        response = {'response': 'error', 'message': 'Invalid access point'}
        response_JSON = json.dumps(response)
        return response_JSON

    # Peer sent a broadcast
    @cherrypy.expose
    def rx_broadcast(self):
        print("====================")
        print("RX_BROADCAST MESSAGE CALLED")
        print("====================")
        rawbody = cherrypy.request.body.read()

        try:
            body = json.loads(rawbody)
            # Checks if the body of the JSON sent has all the required parameters
            if body['loginserver_record'] and body['message'] and body['sender_created_at'] and body['signature']:
                record_inparts = helper.splitServerRecord(
                    body['loginserver_record'])
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
                print("====================")
                print("PUBLIC MESSAGE FAILED")
                print("====================")
        except Exception as error:
            payload = {
                'response': 'error',
                'message': 'invalid body,  missing required parameters'
            }
            print("====================")
            print("PUBLIC MESSAGE FAILED")
            print("====================")
        return json.dumps(payload)

    # Peer to ping_check my server
    @cherrypy.expose
    def ping_check(self):
        print("====================")
        print("PING_CHECK CALLED")
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

        try: # Checks if the body of the JSON sent is has all the parameters
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
                    'response': 'error',
                    'message': 'invalid body, missing required parameters'
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

    # Peer to private message a user
    @cherrypy.expose
    def rx_privatemessage(self):
        print("====================")
        print("RX_PRIVATE MESSAGE CALLED")
        print("====================")
        rawbody = cherrypy.request.body.read()

        try:
            body = json.loads(rawbody)
            # Checks if all the parameters are in the JSON sent
            if body['loginserver_record'] and body['target_pubkey'] and body['target_username'] and body['encrypted_message'] and body['sender_created_at'] and body['signature']:
                record_inparts = helper.splitServerRecord(
                    body['loginserver_record'])
                message_handler.updatePrivateMessages(
                    body['target_username'], body['encrypted_message'], record_inparts[0], body['sender_created_at'], body['loginserver_record'], body['signature'], body['target_pubkey'])
                payload = {
                    'response': 'ok',
                }
                print("====================")
                print("PRIVATE MESSAGE SUCCESS")
                print("====================")
            else:
                print("====================")
                print("PRIVATE MESSAGE FAILED")
                print("====================")
        except Exception as error:
            print(error)
            payload = {
                'response': 'error',
                'message': 'invalid body, missing required parameters'
            }
            print("====================")
            print("PRIVATE MESSAGE FAILED")
            print("====================")

        return json.dumps(payload)
