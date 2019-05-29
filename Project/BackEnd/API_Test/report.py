import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing

url = "http://cs302.kiwi.land/api/report"

# PRIVATE KEY
# b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
# b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'
# b'9a72eeb920ce03a812deda0f49206a89398e09aac546476e6dee4c717ebba638'
username = "tmag741"
password = "Teresito_419588351"


hex_key = b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
verify_key = signing_key.verify_key
pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
pubkey_hex_str = pubkey_hex.decode('utf-8')


credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type' : 'application/json; charset=utf-8',
}

payload = {
    "connection_address": "192.168.1.9:1234",
    "connection_location": "2",
    "incoming_pubkey" : pubkey_hex_str,
    "status" : "online"
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

