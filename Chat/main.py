import os
import cherrypy
import sqlite3
import API
import Serve
import Client
import thread_tasks
import socket

# LISTEN_IP = "192.168.1.6"  # IPv4 connection router to this device
hostname = socket.gethostname()
LISTEN_IP = socket.gethostbyname(hostname)
LISTEN_PORT = 10204  # Port to be communicated with
##                                                         ##
# Note if you are in uni, you use IPv4 for LOCATION_ADDRESS #
##                                                         ##
# LOCATION_ADRESS = "122.60.172.73:80" # External IP for connection externallly
LOCATION_ADRESS = LISTEN_IP # External IP for connection externallly
WORLD_CONNECTION = '0' # 0 Uni computer / 1 Uni WiFi / 2 External Connection

SESSION_DB = 'session.db' # Database for multiple user session

# Cross Origin Scripting Function
# This used to enable frameworks like Angular make backend calls to CherryPy

def cors():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

# Main function to start CherryPy
def main():
	# CherryPy configuration
    conf = {
    	# Route all / sessions to current directory folder
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        # Route all /static to /Bundled folder
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Bundled',
        },
    }

    # CherryPy socket configuration
    cherrypy.config.update({'server.socket_host': LISTEN_IP,
                            'server.socket_port': LISTEN_PORT,
                            'engine.autoreload.on': True,
                           })

    # CORS function per request
    cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
    

    print("========================================")
    print("             Teresito Magbag")
    print("         University of Auckland")
    print("   COMPSYS302 - CherryPy / Angular")
    print("========================================")                       
    
    cherrypy.tree.mount(Serve.Web_Page(), "/", conf) # Serves the webpage
    cherrypy.tree.mount(API.Interface(), "/api", conf) # End points for my peers
    cherrypy.tree.mount(Client.Interface(), "/client", conf) # Client communication


    cherrypy.engine.subscribe('start', start_session) # Starting the threading and database ssessions
    cherrypy.engine.subscribe('stop', stop_session) # Dropping all database sessions

    cherrypy.engine.start() # Start CherryPy
    cherrypy.engine.block()
 
# Start function before CherryPy continues
def start_session():
	# Background thread task to ping_check my peers every 2 minutes 
    interval_ping = cherrypy.process.plugins.BackgroundTask(
        120, thread_tasks.ping_checkServers, [LOCATION_ADRESS, WORLD_CONNECTION])

    # Background thread task to update user_list used for ping_check everyone 30 seconds
    interval_list = cherrypy.process.plugins.BackgroundTask(
        30, thread_tasks.updateDBList)

    # Start Threads
    interval_ping.start()
    interval_list.start()

    # Create table for sessions
    createSESSION = """ CREATE TABLE IF NOT EXISTS "USER_SESSION" (
	"USER" TEXT NOT NULL UNIQUE,
	"APIKEY" TEXT NOT NULL UNIQUE,
	"PRIVATE_DATA" TEXT UNIQUE,
	"PRIVATE_KEY" TEXT UNIQUE,
	"PUBLIC_KEY" TEXT UNIQUE,
	"TIME" INTEGER NOT NULL,
	"STATUS" TEXT,
    "EDKEY"	TEXT
    ); """

    # Create table for user_list to ping
    createLIST = """ CREATE TABLE IF NOT EXISTS "USER_LIST" (
	"USER"	TEXT NOT NULL UNIQUE,
	"ADDRESS"	TEXT NOT NULL,
	"LOCATION"	TEXT NOT NULL,
	"PUBLIC_KEY"	TEXT NOT NULL UNIQUE,
	"TIME"	INTEGER NOT NULL,
	"STATUS"	TEXT NOT NULL
    );"""

    # Execute creation of table. Drop them first if server was abruptly killed
    with sqlite3.connect(SESSION_DB) as con:
        con.execute("DROP TABLE IF EXISTS USER_SESSION")
        con.execute("DROP TABLE IF EXISTS USER_LIST")
        con.execute(createSESSION)
        con.execute(createLIST)

# Stop function before CherryPy ends
def stop_session():
	# Drop all table for the ssesions
    with sqlite3.connect(SESSION_DB) as con:
        con.execute("DROP TABLE IF EXISTS USER_SESSION")
        con.execute("DROP TABLE IF EXISTS USER_LIST")

if __name__ == '__main__':
    main() # Function to call on running this script
