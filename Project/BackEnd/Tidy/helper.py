import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
import nacl.pwhash
import urllib.request
import json
import base64
import time

def encryptData(userData,encryptKey):
    #SALT
    salt = bytes(encryptKey,'utf-8')*16
    salt = salt[0:16]
    #BOX
    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
    key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,encryptKey,cut,ops,mem)
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    jsonBytes = bytes(json.dumps(userData),'utf-8')
    encrypted = box.encrypt(jsonBytes,encoder=nacl.encoding.HexEncoder)
    encrypted_hex_str = base64.b64encode(encrypted).decode("utf-8") # send to payload
    return encrypted_hex_str

def decryptData(decryptKey):
	#SALT
	salt = bytes(decryptKey,'utf-8')*16
	salt = salt[0:16]
	#BOX
	ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
	mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
	key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,decryptKey,cut,ops,mem)
	box = nacl.secret.SecretBox(key)
	try:
	    message = box.decrypt(encrypted,encoder=nacl.encoding.HexEncoder)
	except nacl.exceptions.CryptoError as error:
	    message = "error"
	return message