import os
import cherrypy
import server

# The address we listen for connections on
LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 8080

def runMainApp():
    #set up the config
    conf = {

    }


    # Create an instance of MainApp and tell Cherrypy to send all requests under / to it. (ie all of them)
    cherrypy.tree.mount(server.MainApp(), "/api", conf)

    # Tell cherrypy where to listen, and to turn autoreload on
    cherrypy.config.update({'server.socket_host': LISTEN_IP,
                            'server.socket_port': LISTEN_PORT,
                            'engine.autoreload.on': True,
                           })
                  
    
    #Cherry Starting Sequence
    cherrypy.engine.start()
    cherrypy.engine.block()
 
#Run the function to start everything
if __name__ == '__main__':	
    runMainApp()
