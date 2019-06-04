import random
import nacl.encoding
import nacl.signing
import time
import nacl.secret
import nacl.utils
import nacl.pwhash
import base64
import json


password = b"magbag"*16
cut = password[0:16]
print(cut)
ops = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE
mem = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
key = nacl.pwhash.argon2id.kdf(nacl.secret.SecretBox.KEY_SIZE,password,cut,ops,mem)
box = nacl.secret.SecretBox(key)

nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
privateData = {
    "prikeys": ["...", "..."],
    "blocked_pubkeys": ["...", "..."],
    "blocked_usernames": ["...", "..."],
    "blocked_words": ["...", "..."],
    "blocked_message_signatures": ["...", "..."],
    "favourite_message_signatures": ["...", "..."],
    "friends_usernames": ["...", "..."]
}

jsonBytes = bytes(json.dumps(privateData),'utf-8')
encrypted = box.encrypt(jsonBytes,encoder=nacl.encoding.HexEncoder) # Encrypting
encrypted_hex_str = base64.b64encode(encrypted).decode("ascii") # send to payload
myData = box.decrypt(encrypted,encoder=nacl.encoding.HexEncoder)
print(encrypted)
print(myData)

