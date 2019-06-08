import random
import nacl.encoding
import nacl.signing
import time
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64
import json
import urllib.request
import clientAPI

def encryptData(userData, encryptKey):
    # SALT
    salt = bytes(encryptKey, 'utf-8')*16
    salt = salt[0:16]
    # BOX
    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
    key = nacl.pwhash.argon2i.kdf(nacl.secret.SecretBox.KEY_SIZE, encryptKey.encode(
        'utf-8'), salt, ops, mem, encoder=nacl.encoding.HexEncoder)
    box = nacl.secret.SecretBox(key, encoder=nacl.encoding.HexEncoder)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    jsonBytes = bytes(json.dumps(userData), 'utf-8')
    encrypted = box.encrypt(jsonBytes, nonce, encoder=nacl.encoding.HexEncoder)
    encrypted_hex_str = base64.b64encode(encrypted).decode("utf-8")

    return encrypted_hex_str


def decryptData(userData, decryptKey):
    # SALT
    salt = bytes(decryptKey, 'utf-8')*16
    salt = salt[0:16]
    # BOX
    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
#	key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,bytes(decryptKey,'utf-8'),salt,ops,mem)
    try:
        key = nacl.pwhash.argon2i.kdf(nacl.secret.SecretBox.KEY_SIZE, decryptKey.encode(
            'utf-8'), salt, ops, mem, encoder=nacl.encoding.HexEncoder)
    except nacl.exceptions.TypeError as error:
        return "error"

    box = nacl.secret.SecretBox(key, encoder=nacl.encoding.HexEncoder)
    try:
        message = box.decrypt(base64.b64decode(userData),encoder=nacl.encoding.HexEncoder)
        message = json.loads(message.decode('utf-8'))
    except nacl.exceptions.CryptoError as error:
        message = "error"
    return message


def generatePubKey(privateKey):
    hex_key = bytes(privateKey, 'utf-8')
    signing_key = nacl.signing.SigningKey(
        hex_key, encoder=nacl.encoding.HexEncoder)
    # PUBLIC KEY
    pubkey_hex = signing_key.verify_key.encode(
        encoder=nacl.encoding.HexEncoder)
    pubkey_hex_str = pubkey_hex.decode('utf-8')
    return pubkey_hex_str

def splitServerRecord(record):
    splitted = record.split(',')
    return splitted

# Returns the request response to caller
def Request(url, data, header):

    if(url == None):
        return "No URL was provided"
    elif(data == None and header == None):  # No data No Header
        req = urllib.request.Request(url)
        #print("No Data / No Header")
    elif(data == None and header != None):  # No data and Header
        req = urllib.request.Request(url, headers=header)
        #print("No Data / Header")
    elif(data != None and header == None):  # data and No header
        req = urllib.request.Request(url, data=data)
        #print("Data / No Header")
    else:
        req = urllib.request.Request(url, data=data, headers=header)
        #print("Data / Header")
    try:
        response = urllib.request.urlopen(req)
        data = response.read()
        response.close()
    except Exception as error:
        print(error)
        return("error")
    else:
        json_response = json.loads(data.decode('utf-8'))
        return json_response
    # except urllib.error.HTTPError as error:
    #     data = error.read()


def pingThread(Hostlist,hostIP,location):
    errorCount = 0
    toCall = 0;
    for host in Hostlist:
        
        hostAddress = host['connection_address']
        hostLocation = host['connection_location']
        if(hostAddress != hostIP and hostLocation == location):
            toCall += 1
            if(hostAddress[:4] != "http"):
                hostAddress = "http://" + hostAddress

            clientResponse = clientAPI.ping_check(hostAddress,hostIP,location)
            if(clientResponse == "error"):
                errorCount += 1
    
    print("=================")
    print("Total errors: "+str(errorCount)+" out of "+str(toCall))
    print("=================")
