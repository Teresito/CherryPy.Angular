import nacl.secret
import nacl.utils
import nacl.pwhash
import nacl.encoding
# Do not do "import nacl", it won't work
import base64
import json
password = b"I like Python"
secret_msg = b"Actually, I prefer Javascript..."

someJSON = {
	"key": "value"
}

JSON_Bytes = bytes(json.dumps(someJSON),'utf-8')

# Generate the key:
kdf = nacl.pwhash.argon2i.kdf # our key derivation function
salt_size = nacl.pwhash.argon2i.SALTBYTES # The salt musts have a size of 16 bytes

#salt = nacl.utils.random(salt_size) # can be sth like: b'3\xba\x8f\r]\x1c\xcbOsU\x12\xb6\x9c(\xcb\x94'
salt = b'\x9b\xcb\xb6E\x1d\xc1\x06\xa2\xebg\x8e\xea>Q\x01^'

print(salt)

key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)

# Encrypt the data:
box = nacl.secret.SecretBox(key)
#encrypted = box.encrypt(secret_msg) # Encrypting
encrypted = box.encrypt(JSON_Bytes,encoder=nacl.encoding.HexEncoder) # Encrypting
encrypted_hex_str = encrypted.decode('utf-8')
print(encrypted_hex_str)
#content = base64.b64encode(encrypted).decode("ascii") # Into ASCII Base64
#content_hex = content.encode(encoder=nacl.encoding.HexEncoder)
#content_hex_str = content_hex.decode('utf-8')

#print(content)

# DECRYPTING PART
box = nacl.secret.SecretBox(key)
secret_msg = box.decrypt(encrypted,encoder=nacl.encoding.HexEncoder)
print(secret_msg.decode("utf-8"))

