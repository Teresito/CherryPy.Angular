import os
import cherrypy
# from Controllers import API
# from Controllers import Serve
# from Controllers import Client
import API
import Serve
import Client

LISTEN_IP = "192.168.1.6"
LISTEN_PORT = 80

def cors():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

def main():

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Bundled',
        },
    }


    cherrypy.config.update({'server.socket_host': LISTEN_IP,
                            'server.socket_port': LISTEN_PORT,
                            'engine.autoreload.on': True,
                           })

    cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
    #cherrypy.tools.auth = cherrypy.Tool('before_handler', auth.check_auth, 99) # <---- CHECK

    print("========================================")
    print("             Teresito Magbag")
    print("         University of Auckland")
    print("   COMPSYS302 - CherryPy / Angular")
    print("========================================")                       
    
    cherrypy.tree.mount(Serve.Web_Page(), "/", conf) # Serves the webpage
    cherrypy.tree.mount(API.Interface(), "/api", conf) # End points for my peers
    cherrypy.tree.mount(Client.Interface(), "/client", conf) # Client communication
#                           #
## FUTURE SESSION WITH RAM ##
#                           #
    cherrypy.engine.start()
    cherrypy.engine.block()
 

if __name__ == '__main__':
    main()
