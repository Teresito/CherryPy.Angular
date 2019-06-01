import os, os.path
import urllib.request
import json
import cherrypy
import base64

global api_key



def cors():
  if cherrypy.request.method == 'OPTIONS':
    # preflign request 
    # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
    cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
    cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
    cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
    # tell CherryPy no avoid normal handler
    return True
  else:
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)


class Main(object):
    @cherrypy.expose
    def default(self):
        return open('./bundled/index.html')

@cherrypy.config(**{'tools.cors.on': True}) 
class Api:

  @cherrypy.expose 
  def endpoint(self):
    data = cherrypy.request.body.read()
    data_json = json.loads(data.decode('utf-8'))
    print("-----")
    print(data_json['a'])
    print("-----")
    return "Helo"

  @cherrypy.expose 
  def ping(self):
    url = "http://cs302.kiwi.land/api/ping" 

    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
   
    data = response.read() 
    response.close() 
    return(data)

  @cherrypy.expose
  def logout(self):
    api_key = 0;
    return "1"

  @cherrypy.expose 
  def login(self):
    data = cherrypy.request.body.read()
    data_json = json.loads(data.decode('utf-8'))
    print(data_json)


    url = "http://cs302.kiwi.land/api/load_new_apikey"

    credentials = ('%s:%s' % (data_json['user'], data_json['pass']))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type' : 'application/json; charset=utf-8',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read() # read the received bytes
        encoding = response.info().get_content_charset('utf-8') #load encoding if possible (default to utf-8)
        response.close()
    except urllib.error.HTTPError as error:
        error = error.read()
        error_json = json.loads(error.decode('utf-8'))
        return "0"

    JSON_object = json.loads(data.decode(encoding))
    api_key = JSON_object['api_key']
    return "1"

config = {
  'global' : {
    #'server.socket_host' : '192.168.1.13',
    #'server.socket_port' : 80,
    'server.socket_host' : '192.168.1.13',
    'server.socket_port' : 80,
    'server.thread_pool' : 8
  },
  '/':{
    'tools.sessions.on': True,
    'tools.staticdir.root': os.path.abspath(os.getcwd())
  },

  '/static': { 
      'tools.staticdir.on': True,
      'tools.staticdir.dir': './bundled',
  },
}

if __name__ == '__main__':
  #cherrypy.quickstart(Api(), '/api', config)
  cherrypy.tree.mount(Main(), '/', config)
  cherrypy.quickstart(Api(), '/api', config)
      # Start the web server
  cherrypy.engine.start()

  # And stop doing anything else. Let the web server take over.
  cherrypy.engine.block()