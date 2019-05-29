import nacl.secret
import nacl.utils
import nacl.pwhash
import base64

password = b"I like Python"
salt = b'3\xba\x8f\r]\x1c\xcbOsU\x12\xb6\x9c(\xcb\x94' # our previous salt from encryption.py:
# https://gist.github.com/authmane512/7f0c1d6797ea9ff83015c3ddce704b3a

# Generate the key:
kdf = nacl.pwhash.argon2i.kdf # our key derivation function
key = kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt)

# Read the data with binary mode:
with open('file.bin', 'rb') as f:
  encrypted = f.read()

# Read the data with text mode:
with open('file.txt', 'r') as f:
  content = f.read()
  encrypted = base64.b64decode(content)

# Decrypt the data:
box = nacl.secret.SecretBox(key)
secret_msg = box.decrypt(encrypted)
print(secret_msg.decode("utf-8"))