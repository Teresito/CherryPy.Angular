import urllib.request
import json
import base64

url = "http://cs302.kiwi.land/api/load_new_apikey"


username = "tmag741"
password = "Teresito_419588351"


credentials = ('%s:%s' % (username, password))
b64_credentials = base64.b64encode(credentials.encode('ascii'))
headers = {
    'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
    'Content-Type' : 'application/json; charset=utf-8',
}

# headers = {
#     'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
#     'Content-Type' : 'application/json; charset=utf-8',
# }
try:
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read() # read the received bytes
    encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
    response.close()
except urllib.error.HTTPError as error:
    print(error.read())
    exit()

JSON_object = json.loads(data.decode(encoding))
print(JSON_object['api_key'])

