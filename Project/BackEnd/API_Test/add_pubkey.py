import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing

url = "http://cs302.kiwi.land/api/add_pubkey"

#STUDENT TO UPDATE THESE...
username = "tmag741"
password = "Teresito_419588351"

#create HTTP BASIC authorization header
credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type': 'application/json; charset=utf-8',
}

# PRIVATE KEY
# b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
# b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'
#hex_key = nacl.signing.SigningKey.generate().encode(encoder=nacl.encoding.HexEncoder)
hex_key = b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
print(hex_key)
signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
# PUBLIC KEY



pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)

pubkey_hex_str = pubkey_hex.decode('utf-8')

message_bytes = bytes(pubkey_hex_str + username, encoding='utf-8')

signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)

signature_hex_str = signed.signature.decode('utf-8')

payload = {
    "pubkey":pubkey_hex_str, 
    "username": "tmag741",
    "signature": signature_hex_str,
}

try:
    req = urllib.request.Request(url, data=bytes(json.dumps(payload), 'utf-8'), headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read()  # read the received bytes
    # load encoding if possible (default to utf-8)
    encoding = response.info().get_content_charset('utf-8')
    response.close()
except urllib.error.HTTPError as error:
    print(error.read())
    exit()

JSON_object = json.loads(data.decode(encoding))
print(JSON_object)
