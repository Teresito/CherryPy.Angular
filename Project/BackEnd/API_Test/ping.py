import urllib.request
import json

#url = "http://cs302.kiwi.land/api/ping"
url = "http://302cherrypy.mynetgear.com/api"

#create request and open it into a response object
req = urllib.request.Request(url)
try:
	response = urllib.request.urlopen(req)
except urllib.error.HTTPError as error:
	response = error


#read and process the received bytes
response.close() #be a tidy kiwi
print(response)
print(type(response))
# data = response.read() 
# encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)


# JSON_object = json.loads(data.decode('utf-8'))
# print(JSON_object)
