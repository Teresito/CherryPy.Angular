import sqlite3
from sqlite3 import Error
import time


SESSION_DB = "session.db"

def loginUser(user, apikey, time):
    epoch = time.time()
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("INSERT INTO USER_SESSION (USER,APIKEY,TIME) VALUES (?,?,?)", (user, apikey, epoch))


def logoutUser(user):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("DELETE FROM USER_SESSION WHERE USER=?", [user])


def userCheck(user):
    check = False
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT * FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    if(len(fetched) >= 1):
        check = True

    return(check)

def userHeader(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT APIKEY FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    return(fetched)

def userKeys(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT PRIVATE_KEY PUBLIC_KEY FROM USER_SESSION WHERE USER=?", [user])
    
    fetched = mouse.fetchall()
    return(fetched)
