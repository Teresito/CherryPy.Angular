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
hex_key =bytes('fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6','utf-8')
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

def privateMessage():
    url = "http://cs302.kiwi.land/api/rx_privatemessage"
    

    record = serverRecordAPI()
    timeSaved = str(time.time())
    serverKey = loginPubKey()
    target_user = "admin"
    message = b'Check Pubkey API is it working?'

    verifykey = nacl.signing.VerifyKey(serverKey, encoder=nacl.encoding.HexEncoder)
    publickey = verifykey.to_curve25519_public_key()
    sealed_box = nacl.public.SealedBox(publickey)
    encrypted = sealed_box.encrypt(message, encoder=nacl.encoding.HexEncoder)
    message_hex_str = encrypted.decode('utf-8')

    #Signature
    message_bytes = bytes(record + serverKey + target_user + message_hex_str + timeSaved, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    payload = {
        "loginserver_record" : record,
        "target_pubkey" : serverKey,
        "target_username" : target_user,
        "encrypted_message" : message_hex_str,
        "sender_created_at" : timeSaved,
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

    JSON_object = json.loads(data.decode(encoding))
    print(JSON_object)



def loginPubKey():
    url = "http://cs302.kiwi.land/api/loginserver_pubkey"

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
    return JSON_object['pubkey']

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
    privateMessage()