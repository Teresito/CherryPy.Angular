import random
import nacl.encoding
import nacl.signing
import time
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64
import json

def encryptData(userData,encryptKey):
    #SALT
    salt = bytes(encryptKey,'utf-8')*16
    salt = salt[0:16]
    #BOX
    ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
    mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
    key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,bytes(encryptKey,'utf-8'),salt,ops,mem)
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    jsonBytes = bytes(json.dumps(userData),'utf-8')
    encrypted = box.encrypt(jsonBytes,nonce,encoder=nacl.encoding.HexEncoder)
    encrypted_hex_str = encrypted.decode('utf-8')

    return encrypted_hex_str

def decryptData(userData,decryptKey):
	#SALT
	salt = bytes(decryptKey,'utf-8')*16
	salt = salt[0:16]
	#BOX
	ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
	mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
#	key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,bytes(decryptKey,'utf-8'),salt,ops,mem)
	try:
		key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,bytes(decryptKey,'utf-8'),salt,ops,mem)
	except nacl.exceptions.TypeError as error:
		return "error"	
	
	box = nacl.secret.SecretBox(key)
	
	try:
	    message = box.decrypt(userData,encoder=nacl.encoding.HexEncoder)
	except nacl.exceptions.CryptoError as error:
	    message = "error"
	return message