import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing

url = "http://cs302.kiwi.land/api/add_pubkey"
# 
username = "tmag741"
password = "Teresito_419588351"

# BASIC
credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type': 'application/json; charset=utf-8',
}

# header = {
#   'X-username': username,
#   'X-apikey': api_key
# }
# PRIVATE KEY ( NEW )
#hex_key = nacl.signing.SigningKey.generate().encode(encoder=nacl.encoding.HexEncoder)
hex_key = b'fbb230618365d64547c54a7bf8d22a60abf908958de3f00d28d9ba3301a5abc6'
signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
# PUBLIC KEY
pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
pubkey_hex_str = pubkey_hex.decode('utf-8')
# SIGNATURE
message_bytes = bytes(pubkey_hex_str + username, encoding='utf-8')
signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
signature_hex_str = signed.signature.decode('utf-8')
print(signature_hex_str)
payload = {
    "pubkey":pubkey_hex_str, 
    "username": "tmag741",
    "signature": signature_hex_str,
}

try:
    req = urllib.request.Request(url, data=bytes(json.dumps(payload), 'utf-8'), headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    response.close()
except urllib.error.HTTPError as error:
    print(error.read())
    exit()

JSON_object = json.loads(data.decode(encoding))
print(JSON_object)
