import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing
import time
import nacl.secret
import nacl.utils
import nacl.pwhash

##                                                  ##
#               GLOBAL VARIABLES                     #
##                                                  ##
username = "tmag741"
password = "Teresito_419588351"
passwordBox = b"I like Python"
credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type': 'application/json; charset=utf-8',
}

# b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
# b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'

# PRIVATE KEY
hex_key = b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'
signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
verify_key = signing_key.verify_key
pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
pubkey_hex_str = pubkey_hex.decode('utf-8')

# SAFE BOX 
kdf = nacl.pwhash.argon2i.kdf # our key derivation function
salt = b'\x9b\xcb\xb6E\x1d\xc1\x06\xa2\xebg\x8e\xea>Q\x01^'
key = kdf(nacl.secret.SecretBox.KEY_SIZE, passwordBox, salt)
box = nacl.secret.SecretBox(key)        

##                                                  ##
#               END GLOBAL VARIABLES                 #
##                                                  ##

def privateData():
    url = "http://cs302.kiwi.land/api/add_privatedata"
    
    privateData = {
        "prikeys": ["...", "..."],
        "blocked_pubkeys": ["...", "..."],
        "blocked_usernames": ["...", "..."],
        "blocked_words": ["...", "..."],
        "blocked_message_signatures": ["...", "..."],
        "favourite_message_signatures": ["...", "..."],
        "friends_usernames": ["...", "..."]
    }

    JSON_Bytes = bytes(json.dumps(privateData),'utf-8')

    encrypted = box.encrypt(JSON_Bytes,encoder=nacl.encoding.HexEncoder) # Encrypting
    encrypted_hex_str = encrypted.decode('utf-8')
    #print(encrypted_hex_str)

    timeSaved = str(time.time())
    record = serverRecordAPI();

    #Signature
    message_bytes = bytes(encrypted_hex_str + record + timeSaved, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    payload = {
        "privatedata" : encrypted_hex_str,
        "loginserver_record" : record,
        "client_saved_at" : timeSaved,
        "signature": signature_hex_str
    }
    


    try:
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), 'utf-8'), headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()


    encrypted = box.encrypt(JSON_Bytes) # Encrypting
    content = base64.b64encode(encrypted).decode("ascii") # Into ASCII Base64    

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)

def getPrivateData():
    url = "http://cs302.kiwi.land/api/get_privatedata"

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object['response'])
    myData = box.decrypt(JSON_object['privatedata'],encoder=nacl.encoding.HexEncoder)
    print(myData.decode('utf-8'))

def serverRecordAPI():
    url = "http://cs302.kiwi.land/api/get_loginserver_record"

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        print(error.read())
        exit()

    JSON_object = json.loads(data.decode(encoding))
    return JSON_object['loginserver_record']
    

if __name__ == "__main__":
    privateData()
    getPrivateData()