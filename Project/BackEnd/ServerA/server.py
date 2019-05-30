import cherrypy

class MainApp(object):

	#CherryPy Configuration
    _cp_config = {'tools.encode.on': True, 
                  'tools.encode.encoding': 'utf-8',
                  'tools.sessions.on' : 'True',
                 }       

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def ping(self):
        url = "http://cs302.kiwi.land/api/ping"

        #create request and open it into a response object
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)

        #read and process the received bytes
        data = response.read() 
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close() #be a tidy kiwi


        JSON_object = json.loads(data.decode(encoding))
        print(JSON_object)

##                         ##
# Functions only after here #
##                         ##