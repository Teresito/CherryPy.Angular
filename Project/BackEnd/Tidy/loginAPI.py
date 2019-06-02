import cherrypy
import urllib.request
import json
import base64
import nacl.encoding
import nacl.signing
import time
import nacl.secret
import nacl.utils
import nacl.pwhash

HOST = "http://cs302.kiwi.land/api"

# Returns the request response to caller


def Request(url, data, header):
	success = False
	failed = False
	if(url == None): 
		return "No URL was provided"
	elif(data == None and header == None):  # No data No Header
		req = urllib.request.Request(url)
		print("No Data / No Header")
	elif(data == None and header != None):  # No data and Header
		req = urllib.request.Request(url, headers=header)
		print("No Data / Header")
	elif(data != None and header == None):  # data and No header
		req = urllib.request.Request(url, data=data)
		print("Data / No Header")
	else:
		req = urllib.request.Request(url, data=data, headers=header)
		print("Data / Header")
	try:		
		response = urllib.request.urlopen(req)
		data = response.read()
		encoding = response.info().get_content_charset('utf-8')        
		response.close()
		success = True
	except urllib.error.HTTPError as error:
		data = error.read()
		failed = True

	
	if(success == True):
		json_response = json.loads(data.decode(encoding))
		return json_response
	elif(failed == True):
		json_response = json.loads(data.decode('utf-8'))
		return json_response  

def ping():
	url = HOST+'/ping'
	return(Request(url, None, None))

# Returns private, public key back to server
def add_pubkey(api_key, username):
	url = HOST+"/add_pubkey"
	# PRIVATE KEY
	hex_key = nacl.signing.SigningKey.generate().encode(encoder=nacl.encoding.HexEncoder)
	signing_key = nacl.signing.SigningKey(hex_key, encoder=nacl.encoding.HexEncoder)
	# PUBLIC KEY
	pubkey_hex = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder)
	pubkey_hex_str = pubkey_hex.decode('utf-8')
	# SIGNATURE
	message_bytes = bytes(pubkey_hex_str + username, encoding='utf-8')
	signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
	signature_hex_str = signed.signature.decode('utf-8')
	# HEADER
	header = {
		'X-username': username,
		'X-apikey': api_key
	}
	# PAYLOAD
	payload = {
		"pubkey": pubkey_hex_str,
		"username": username,
		"signature": signature_hex_str,
	}


# Returns API key to server
def load_new_apikey(username, password):
	url = HOST + "/load_new_apikey"
	# CREDENTIALS
	credentials = ('%s:%s' % (username, password))
	b64_credentials = base64.b64encode(credentials.encode('ascii'))
	headers = {
		'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
		'Content-Type': 'application/json; charset=utf-8',
	}
	return(Request(url,None,headers))

if __name__ == '__main__':
	name = 'tmag741'
	password = 'Teresito_419588351'
	print(load_new_apikey('123','asd'))
	#print(load_new_apikey(name,password))
