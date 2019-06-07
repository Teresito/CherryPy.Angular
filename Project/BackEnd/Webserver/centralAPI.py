import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
import nacl.pwhash
import urllib.request
import json
import base64
import time
import helper

HOST = "http://cs302.kiwi.land/api"

def ping(apikey,username,privateKey):
    url = HOST + '/ping'
    if(apikey == None and username == None and privateKey == None):
        
        return(helper.Request(url, None, None))
    else:

        header = {
            'X-username': username,
            'X-apikey': apikey,
            'Content-Type': 'application/json'
        }

        signing_key = nacl.signing.SigningKey(privateKey, encoder=nacl.encoding.HexEncoder)

        pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
        pubkey_hex_str = pubkey_hex.decode('utf-8')
        signed = signing_key.sign(bytes(pubkey_hex_str,'utf-8'), encoder=nacl.encoding.HexEncoder)
        signature_hex_str = signed.signature.decode('utf-8')

        payload = {
            'pubkey':pubkey_hex_str,
            'signature':signature_hex_str
        }
        
        payload_b = bytes(json.dumps(payload), 'utf-8')

        return(helper.Request(url, payload_b, header))
    


def add_privatedata(apikey,username,userData,privateKey):
    url = HOST + "/add_privatedata"

    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type':'application/json'
    }
    serverRecord = get_loginserver_record(apikey,username)['loginserver_record']
    timeNow = str(time.time())
    # Signature 
    signing_key = nacl.signing.SigningKey(privateKey, encoder=nacl.encoding.HexEncoder)
    message_bytes = bytes(userData + serverRecord + timeNow, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')    

    payload = {
        'privatedata': userData,
        'loginserver_record': serverRecord,
        'client_saved_at': timeNow,
        'signature': signature_hex_str
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url,payload_b,header))

# Returns private, public key back to server
def add_pubkey(apikey, username):
    url = HOST + "/add_pubkey"
    # PRIVATE KEY
    hex_key = nacl.signing.SigningKey.generate().encode(encoder=nacl.encoding.HexEncoder)
    signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
    # PUBLIC KEY
    pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
    pubkey_hex_str = pubkey_hex.decode('utf-8')
    # SIGNATURE
    message_bytes = bytes(pubkey_hex_str + username, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type':'application/json'
    }
    # PAYLOAD
    payload = {
        "pubkey": pubkey_hex_str,
        "username": username,
        "signature": signature_hex_str,
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')

    keyGen = {
        'private_key': hex_key,
        'public_key': pubkey_hex_str
    }

    server_response = helper.Request(url, payload_b, header)['response']
    print(server_response)
    if(server_response == 'ok'):
        return(keyGen)
    else:
        return("Request Error")


def check_pubkey(apikey, pubkey, username):
    url = HOST + "/check_pubkey?pubkey=" + pubkey
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type': 'application/json'
    }
    return(helper.Request(url, None, header))

# Returns API key to server


def load_new_apikey(username, password):
    url = HOST + "/load_new_apikey"
    # CREDENTIALS
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type': 'application/json; charset=utf-8',
    }
    return(helper.Request(url, None, headers))


def report(apikey, username, address, location, pubkey, status):
    url = HOST + "/report"
    print('------------------------')
    print('REPORTING USER %s AS %s' % (username, status))
    print('------------------------')
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type': 'application/json'
    }
    payload = {
        "connection_address": address,
        "connection_location": location,
        "incoming_pubkey": pubkey,
        "status": status
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, header))


def get_loginserver_record(apikey, username):
    url = HOST + "/get_loginserver_record"
    header = {
        'X-username': username,
        'X-apikey': apikey
    }
    return(helper.Request(url, None, header))


def list_users(apikey, username):
    url = HOST + "/list_users"
    header = {
           'X-username': username,
           'X-apikey': apikey,
           'Content-Type': 'application/json'
    }
    return(helper.Request(url, None, header))


def list_apis():
    url = HOST + "/list_apis"
    return(helper.Request(url, None, None))

def loginserver_pubkey():
    url = HOST + "/loginserver_pubkey"
    return(helper.Request(url, None, None))

def rx_broadcast(apikey,username,message,time,privkey):
    url = HOST + "/rx_broadcast"
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type': 'application/json'
    }

    serverRecord = get_loginserver_record(apikey,username)

    signing_key = nacl.signing.SigningKey(privkey, encoder=nacl.encoding.HexEncoder)    
    message_bytes = bytes(serverRecord + message +
                          time, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    payload = {
        "loginserver_record":serverRecord, 
        "message": message,
        "sender_created_at": time,
        "signature": signature_hex_str
    }

    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, header))

def get_privatedata(apikey,username):
    url = HOST + '/get_privatedata'
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type': 'application/json'
    }
    return(helper.Request(url, None, header))



def rx_privatemessage(apikey,username,serverRecord,time,message,privkey,targetKey,target):
    url = HOST + "/rx_privatemessage"
    header = {
        'X-username': username,
        'X-apikey': apikey,
        'Content-Type': 'application/json'
    }
    # ENCRYPTING MESSAGE
    message = bytes(message,'utf-8')
    verifykey = nacl.signing.VerifyKey(targetKey, encoder=nacl.encoding.HexEncoder)
    publickey = verifykey.to_curve25519_public_key()
    sealed_box = nacl.public.SealedBox(publickey)
    encrypted = sealed_box.encrypt(message, encoder=nacl.encoding.HexEncoder)
    message_hex_str = encrypted.decode('utf-8')

    signing_key = nacl.signing.SigningKey(privkey, encoder=nacl.encoding.HexEncoder)    
    message_bytes = bytes(serverRecord + targetKey + target + message_hex_str + time, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    payload = {
        "loginserver_record" : serverRecord,
        "target_pubkey" : targetKey,
        "target_username" : target,
        "encrypted_message" : message_hex_str,
        "sender_created_at" : time,
        "signature": signature_hex_str
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, header))

if __name__ == '__main__':
    name = 'tmag741'
    password = 'Teresito_419588351'
    APIkey = load_new_apikey(name, password)['api_key']
