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

#LOCATION_ADRESS = "http://302cherrypy.mynetgear.com"
LOCATION_ADRESS = "122.60.172.73:80"
WORLD_CONNECTION = '2'

@cherrypy.config(**{'tools.cors.on': True})
class Interface(object):
  

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return Interface.index(self)

    @cherrypy.expose
    def index(self):
        response = {'response':'error', 'message':'Invalid access point'}
        response_JSON = json.dumps(response)
        return response_JSON
    # typeCheck 0 for just login/unlock_data/add_pubkey/check_privatedata 1 for everything else
    def isLoggedIn(self,user,typeCheck):
        if(session_handler.hasData()==True):# NO DATA
            return False

        if(typeCheck == 1):
            if(session_handler.userCheck(user)==True):
                APIKey = session_handler.userAPIKey(user)
                privateKey = session_handler.userKeys(user)[0][0]
                centralResponse = centralAPI.ping(APIKey,user,privateKey)
                if(centralResponse == "error" or centralResponse['response'] == "error"):
                    return False
            else:
                return False
            return True
        elif(typeCheck == 0):
            if(session_handler.userCheck(user) == False):
                return False
            return True
            

    # Using header to get IP, i can block their requests to this end point
    # One of the reasons is to minimise frontend pinging hammond/central server
    @cherrypy.expose
    def user_list(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        if (self.isLoggedIn(username, 1) == False):
            return '2'

        APIKey = session_handler.userAPIKey(username)

        centralResponse = centralAPI.list_users(APIKey, username)
        
        if(centralResponse =="error"):
            return '0'

        if (centralResponse['response'] == 'ok'):
            newList = []
            userList = centralResponse['users']
            # for user in userList:
            #     if (user['username'] != username):
            #         newList.append(user['username'])

            jsonToSend = {}
            jsonToSend['amount'] = len(newList)
            jsonToSend['userList'] = userList
            responseBody = json.dumps(jsonToSend)
            return (responseBody)
        else:
            return '0'

    @cherrypy.expose
    def login(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        centralResponse = centralAPI.load_new_apikey(body_json['user'], body_json['pass'])
        print(body_json['pass'])
        print(body_json['user'])
        if(centralResponse == 'error'):
            return '0'

        if (centralResponse['response'] == "ok"):
            session_handler.addUser(body_json['user'], centralResponse['api_key'])
            return '1'

    @cherrypy.expose
    def check_privatedata(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']

        if (self.isLoggedIn(username,0) == False):
            return '2'

        APIKey = session_handler.userAPIKey(username)
        
        centralResponse = centralAPI.get_privatedata(APIKey, username)
        if(centralResponse == "error"):
            return '0'

        if (centralResponse['response'] == "ok"):
            session_handler.updatePrivateData(username, centralResponse['privatedata'])
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def get_privateMessages(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']

        if (self.isLoggedIn(username, 0) == False):
            return '2'

        message_list = message_handler.fetchPrivateMessages()
        private_key = session_handler.userKeys(username)[0][0]
        json_body = {}
        message_array = []
        for message in message_list['private_messages']:
            
            if(message[0] == username):
                decrypted_message = helper.decryptMessage(message[1], private_key)
                tempTuple = (message[0], decrypted_message,
                             message[2], message[3], message[4], message[5], message[6])

                message_array.append(tempTuple)

        json_body['private_messages'] = message_array
        return json.dumps(json_body)


    @cherrypy.expose
    def privateMessage(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        target_user = body_json['target_user']
        target_key = body_json['target_key']
        message = body_json['message']

        if (self.isLoggedIn(username, 0) == False):
            return '2'

        APIkey = session_handler.userAPIKey(username)
        private_key = session_handler.userKeys(username)[0][0]

        # ENCRYPT
        encrypted_message = helper.encryptMessage(message,target_key)
        epoch = time.time()
        epoch_str = str(epoch)

        server_record = centralAPI.get_loginserver_record(APIkey, username)['loginserver_record']
        signing_key = nacl.signing.SigningKey(
            private_key, encoder=nacl.encoding.HexEncoder)
        message_bytes = bytes(server_record + target_key + target_user +
                              encrypted_message + epoch_str, encoding='utf-8')
        signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')

        message_one = threading.Thread(target=thread_tasks.private_message, args=(
            server_record, encrypted_message, LOCATION_ADRESS, target_user, target_key, private_key))
        try:
            message_one.start()
        except Exception as error:
            pass

        message_handler.updatePrivateMessages(
            target_user, encrypted_message, username, epoch, server_record, signature_hex_str,target_key)
        
        return '1'
       

    # Need to check if they're logged in
    @cherrypy.expose
    def unlock_privatedata(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        decryptKey = body_json['decryptionKey']
        
        if (self.isLoggedIn(username, 0) == False):
            return '2'

        lockedData = session_handler.userPrivateData(username)
        unlockedData = helper.decryptData(lockedData, decryptKey)

        if (unlockedData != "error"):
            privateKeyData = unlockedData['prikeys']
            privateKey = privateKeyData[0]
            publicKey = helper.generatePubKey(privateKey)
            EDKey = decryptKey

            session_handler.updatePrivateData(username, str(unlockedData))
            session_handler.updateKeys(username,privateKey,publicKey)
            session_handler.updateEDKey(username,EDKey)
            return '1'
        else:
            return '0'

    @cherrypy.expose
    def logout(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        if (self.isLoggedIn(username, 0) == False):
            return '2'
        # add to database
        # delete session
        APIkey = session_handler.userAPIKey(username)
        public_key = session_handler.userKeys(username)[0][1]
        centralResponse = centralAPI.report(APIkey, username, LOCATION_ADRESS, WORLD_CONNECTION, public_key, "offline")
        session_handler.deleteUser(username)
        return '1'

    @cherrypy.expose
    def get_publicMessages(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        if (self.isLoggedIn(username, 0) == False):
            return '2'        
        
        message_list = message_handler.fetchPublicMessages()
        return json.dumps(message_list)

      

    @cherrypy.expose
    def broadcast(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        if (self.isLoggedIn(username, 1) == False):
            return '2'

        APIkey = session_handler.userAPIKey(username)
        private_key = session_handler.userKeys(username)[0][0]

        message = body_json['message']
        epoch = time.time()
        epoch_str = str(epoch)

        server_record = centralAPI.get_loginserver_record(
            APIkey, username)['loginserver_record']
        signing_key = nacl.signing.SigningKey(
            private_key, encoder=nacl.encoding.HexEncoder)
        message_bytes = bytes(server_record + message +
                              epoch_str, encoding='utf-8')
        signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')

        message_handler.updatePublicMessages(username, message, epoch, server_record, signature_hex_str)

        message_everyone = threading.Thread(target=thread_tasks.broadcast, args=(
            server_record, message, private_key,LOCATION_ADRESS))
        try:
            message_everyone.start()
        except Exception as error:
            pass


        centralResponse = centralAPI.rx_broadcast(APIkey,username, message, epoch_str, private_key)
        return '1'


    @cherrypy.expose
    def add_pubkey(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']

        if (self.isLoggedIn(username, 0) == False):
            return '2'

        APIkey = session_handler.userAPIKey(username)
        centralResponse = centralAPI.add_pubkey(APIkey, username)
        if (centralResponse == "error"):
            return '0'
        else:
            EDKey = body_json['encryptionKey']
            privateKey = centralResponse['private_key']
            publicKey = centralResponse['public_key']
            
            session_handler.updateKeys(username, privateKey, publicKey)
            session_handler.updateEDKey(username, EDKey)
            return '1'

    @cherrypy.expose
    def report_user(self):
        body = cherrypy.request.body.read()
        body_json = json.loads(body.decode('utf-8'))
        username = body_json['username']
        userStatus = body_json['userStatus']

        if (self.isLoggedIn(username, 1) == False):
            return '2'
        
        if(userStatus == '' or userStatus == None):
            userStatus = 'online'
        

        APIkey = session_handler.userAPIKey(username)
        public_key = session_handler.userKeys(username)[0][1]
        session_handler.updateStatus(username,userStatus)
        centralResponse = centralAPI.report(APIkey, username, LOCATION_ADRESS, WORLD_CONNECTION, public_key, userStatus)

        if (centralResponse != "error"):
            if(centralResponse['response'] == 'ok'):
                return '1'
            elif(centralResponse['response']=="error"):
                return '2'
        else:
            return '0'
