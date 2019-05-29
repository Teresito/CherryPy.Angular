import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing

url = "http://cs302.kiwi.land/api/check_pubkey?pubkey="
# b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6' <--
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

# b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
# b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'

# PRIVATE KEY
hex_key = b'3c22f109c37683b833ca5d24fc2d23c41e1bc2a8b26c8064776ef13d8eb57b3c'
signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
verify_key = signing_key.verify_key
pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
pubkey_hex_str = pubkey_hex.decode('utf-8')

payload = {
    "pubkey" : "c64bcf1bb8662433fb178b5de5be2e61903e4ca1821a1db537d8757a00cfa765"
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
