import time
import centralAPI
import clientAPI
import message_handler
import session_handler
import helper
import thread_tasks
import json
import threading
import cherrypy
import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
import nacl.pwhash
import main
##                              ##
# Responses:                     #
# 0 : Bad 1 : OK 2: LOG OUT USER #
##                              ##

# Endpoints for users using my webapp
@cherrypy.config(**{'tools.cors.on': True})
class Interface(object):
  
    # Bad access redirect
    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Interface.index(self)

    # Bad access redirect
    @cherrypy.expose
    def index(self):
        response = {'response':'error', 'message':'Invalid access point'}
        response_JSON = json.dumps(response)
        return response_JSON

    # Checks the body of the data send by client has user is logged in
    def isLoggedIn(self,user,typeCheck):
        if(session_handler.hasData()==True):# Session DB has no data
            return False

        if(typeCheck == 1): # User has logged in with a private key 
            if(session_handler.userCheck(user)==True): # Checks if user is in Session DB
                APIKey = session_handler.userAPIKey(user) # Retrieve user keys
                privateKey = session_handler.userKeys(user)[0][0] # Retrieve user keys
                centralResponse = centralAPI.ping(APIKey,user,privateKey) # Make ping call
                if(centralResponse == "error" or centralResponse['response'] == "error"):
                    return False
            else:
                return False
            return True
        elif(typeCheck == 0): # User has only logged in
            if(session_handler.userCheck(user) == False):
                return False
            return True
            

    # Retrieve user_list from central server
    @cherrypy.expose
    def user_list(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Check if user is logged in
        if (self.isLoggedIn(username, 1) == False):
            return '2'

        # Retrieve APIKey from Session DB
        APIKey = session_handler.userAPIKey(username)
        centralResponse = centralAPI.list_users(APIKey, username)

        # Exception occured and thus error
        if(centralResponse =="error"):
            return '0'

        # Will retrieve all the user list and make a new JSON body
        if (centralResponse['response'] == 'ok'):
            newList = []
            userList = centralResponse['users']

            jsonToSend = {}
            jsonToSend['amount'] = len(newList)
            jsonToSend['userList'] = userList
            responseBody = json.dumps(jsonToSend)
            return (responseBody)
        else:
            return '0'
    # User logging in endpoint

    @cherrypy.expose
    def login(self):
        # Read body sent by client
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        centralResponse = centralAPI.load_new_apikey(body_json['user'], body_json['pass'])
        
        # Exception occured and thus error
        if(centralResponse == 'error'):
            return '0'

        # If successful, will add user to the Session DB
        if (centralResponse['response'] == "ok"):
            session_handler.addUser(body_json['user'], centralResponse['api_key'])
            return '1'

    # Checking private if the user has one
    @cherrypy.expose
    def check_privatedata(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Check if user is logged in
        if (self.isLoggedIn(username,0) == False):
            return '2'
        
        time.sleep(3)
        APIKey = session_handler.userAPIKey(username)        
        centralResponse = centralAPI.get_privatedata(APIKey, username)

        # Exception occured and thus error
        if(centralResponse == "error"):
            return '0'

        # Update session DB with their keys
        if (centralResponse['response'] == "ok"):
            session_handler.updatePrivateData(username, centralResponse['privatedata'])
            return '1'
        else:
            return '0'

    # Retrieval of private messages sent to this user
    @cherrypy.expose
    def get_privateMessages(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Checks if user is logged in
        if (self.isLoggedIn(username, 0) == False):
            return '2'
        # Retrieves all the messages from messages DB
        message_list = message_handler.fetchPrivateMessages()
        private_key = session_handler.userKeys(username)[0][0]
        json_body = {}
        message_array = []
        # Iterate through and only append the messages that is to the user
        for message in message_list['private_messages']:
            # Check if the message is for the requested user
            if(message[0] == username):
                decrypted_message = helper.decryptMessage(message[1], private_key)
                tempTuple = (message[0], decrypted_message,
                             message[2], message[3], message[4], message[5], message[6])

                message_array.append(tempTuple)

        json_body['private_messages'] = message_array
        return json.dumps(json_body)

    # User sent a private message
    @cherrypy.expose
    def privateMessage(self):
        # Reads the body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        target_user = body_json['target_user']
        target_key = body_json['target_key']
        message = body_json['message']
        # Checks if the user is logged in
        if (self.isLoggedIn(username, 0) == False):
            return '2'

        APIkey = session_handler.userAPIKey(username)
        private_key = session_handler.userKeys(username)[0][0]

        # Encrypting the message
        encrypted_message = helper.encryptMessage(message,target_key)
        epoch = time.time()
        epoch_str = str(epoch)
        # Retrevial of Server record used for thread task
        server_record = centralAPI.get_loginserver_record(APIkey, username)['loginserver_record']
        signing_key = nacl.signing.SigningKey(private_key, encoder=nacl.encoding.HexEncoder)
        message_bytes = bytes(server_record + target_key + target_user + encrypted_message + epoch_str, encoding='utf-8')
        # Generate signature
        signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')
        # Make a thread job
        message_one = threading.Thread(target=thread_tasks.private_message, args=(server_record, encrypted_message, main.LOCATION_ADRESS, target_user, target_key, private_key))
        try:
            message_one.start() # Start a thread job
        except Exception as error:
            pass

        # Update message DB
        message_handler.updatePrivateMessages(target_user, encrypted_message, username, epoch, server_record, signature_hex_str,target_key)
        
        return '1'
       
    # User wants to unlock the private data
    @cherrypy.expose
    def unlock_privatedata(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        decryptKey = body_json['decryptionKey']
        # Checks if the user is logged in
        if (self.isLoggedIn(username, 0) == False):
            return '2'

        lockedData = session_handler.userPrivateData(username)
        time.sleep(2)
        unlockedData = helper.decryptData(lockedData, decryptKey)
        # If unlocked, it will return a 1 and update session DB
        if (unlockedData != "error"):
            privateKeyData = unlockedData['prikeys']
            privateKey = privateKeyData[0]
            publicKey = helper.generatePubKey(privateKey)
            EDKey = decryptKey
            # Update session DB
            session_handler.updatePrivateData(username, str(unlockedData))
            session_handler.updateKeys(username,privateKey,publicKey)
            session_handler.updateEDKey(username,EDKey)
            return '1'
        else:
            return '0'
    # 
    @cherrypy.expose
    def logout(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Checks if user is logged in
        if (self.isLoggedIn(username, 0) == False):
            return '2'

        # Retrieves user keys
        APIkey = session_handler.userAPIKey(username)
        EDKey = session_handler.userEDKey(username)
        private_key = session_handler.userKeys(username)[0][0]
        public_key = session_handler.userKeys(username)[0][1]
        userData = session_handler.userPrivateData(username)
        encrypted_data = helper.encryptData(userData, EDKey)
        # centralAPI.add_privatedata(APIkey, username, encrypted_data, private_key)
        # Report user is now offline       
        centralResponse = centralAPI.report(APIkey, username, main.LOCATION_ADRESS, main.WORLD_CONNECTION, public_key, "offline")
        # Delete user from session DB
        session_handler.deleteUser(username) 
        return '1'

    # User retrieves public messages stored in message DB
    @cherrypy.expose
    def get_publicMessages(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        if (self.isLoggedIn(username, 0) == False):
            return '2'        
        
        message_list = message_handler.fetchPublicMessages()
        return json.dumps(message_list)

      
    # User sent a broadcast
    @cherrypy.expose
    def broadcast(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Checks if user is logged in
        if (self.isLoggedIn(username, 1) == False):
            return '2'

        APIkey = session_handler.userAPIKey(username)
        private_key = session_handler.userKeys(username)[0][0]

        message = body_json['message']
        epoch = time.time()
        epoch_str = str(epoch)
        # Server record
        server_record = centralAPI.get_loginserver_record(APIkey, username)['loginserver_record']
        # Signature 
        signing_key = nacl.signing.SigningKey(private_key, encoder=nacl.encoding.HexEncoder)
        message_bytes = bytes(server_record + message + epoch_str, encoding='utf-8')
        signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')
        # Update public messages DB
        message_handler.updatePublicMessages(username, message, epoch, server_record, signature_hex_str)
        # Make a thread to send public broadcast in user_list
        message_everyone = threading.Thread(target=thread_tasks.broadcast, args=(server_record, message, private_key,main.LOCATION_ADRESS))
        try:
            message_everyone.start() # Start thread job
        except Exception as error:
            pass

        # Make a broadcast with central server as well
        centralResponse = centralAPI.rx_broadcast(APIkey,username, message, epoch_str, private_key)
        return '1'

    # User has no private data / choose to add a public key
    @cherrypy.expose
    def add_pubkey(self):
        # Read body of response 
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        # Checks if user is logged in
        if (self.isLoggedIn(username, 0) == False):
            return '2'

        private_data = {}
        APIkey = session_handler.userAPIKey(username)
        centralResponse = centralAPI.add_pubkey(APIkey, username)
        # Bad request thus error
        if (centralResponse == "error"):
            return '0'
        else: # Update session DB with their keys
            EDKey = body_json['encryptionKey']
            privateKey = centralResponse['private_key']
            publicKey = centralResponse['public_key']
            
            session_handler.updateKeys(username, privateKey, publicKey)
            session_handler.updateEDKey(username, EDKey)
            private_data['prikeys'] = [privateKey,"..."]
            session_handler.updatePrivateData(username, str(private_data))
            return '1'
    #  Report user every interval sent by the client
    @cherrypy.expose
    def report_user(self):
        # Read body of request
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        userStatus = body_json['userStatus']
        # Checks if user is logged in
        if (self.isLoggedIn(username, 1) == False):
            return '2'
        # Incase client sent an empty or None string
        if(userStatus == '' or userStatus == None):
            userStatus = 'online'
        

        APIkey = session_handler.userAPIKey(username)
        public_key = session_handler.userKeys(username)[0][1]
        # Update session DB of their status
        session_handler.updateStatus(username,userStatus)
        # Report the user of their updated status
        centralResponse = centralAPI.report(APIkey, username, main.LOCATION_ADRESS, main.WORLD_CONNECTION, public_key, userStatus)
        
        if (centralResponse != "error"):
            if(centralResponse['response'] == 'ok'):
                return '1'
            elif(centralResponse['response'] == "error"):  # Logs user out if report has error
                return '2'
        else:
            return '0'
