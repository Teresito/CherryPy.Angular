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
import pprint

def encryptData(userData, encryptKey):
    box = create_secretBox(encryptKey)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    jsonBytes = bytes(json.dumps(userData), 'utf-8')
    encrypted = box.encrypt(jsonBytes, nonce)
    encrypted_hex_str = base64.b64encode(encrypted).decode("utf-8")

    return encrypted_hex_str


def create_secretBox(encryption_key):

    kdf = nacl.pwhash.argon2i.kdf

    password = encryption_key.encode('utf-8')
    salt = nacl.pwhash.argon2i.SALTBYTES * password

    cut_salt = salt[0:nacl.pwhash.argon2i.SALTBYTES]
    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE

    symmetric_key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt=cut_salt,
                        opslimit=ops, memlimit=mem, encoder=nacl.encoding.HexEncoder)

    secret_box = nacl.secret.SecretBox(symmetric_key,encoder=nacl.encoding.HexEncoder)
    return secret_box    


def decryptData(userData, decryptKey):
    box = create_secretBox(decryptKey)

    try:
        userData_UTF = userData.encode('utf-8')
        message_object = base64.b64decode(userData_UTF)
        message = box.decrypt(message_object)
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

    elif(data == None and header != None):  # No data and Header
        req = urllib.request.Request(url, headers=header)

    elif(data != None and header == None):  # data and No header
        req = urllib.request.Request(url, data=data)

    else:
        req = urllib.request.Request(url, data=data, headers=header)

    try:
        response = urllib.request.urlopen(req, timeout=5)
        data = response.read()
        response.close()
    except urllib.error.HTTPError as error:
        print(url)
        print(error.read())
        return("error")
    except Exception as error:
        return("error")
    else:
        json_response = json.loads(data.decode('utf-8'))
        # print("===================")
        # pprint.pprint(json_response)
        # print("===================")
        return json_response
