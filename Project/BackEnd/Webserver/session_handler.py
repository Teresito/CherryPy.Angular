import sqlite3
from sqlite3 import Error
import time


SESSION_DB = "session.db"

def addUser(user, apikey, time):
    epoch = time.time()
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("INSERT INTO USER_SESSION (USER,APIKEY,TIME) VALUES (?,?,?)", (user, apikey, epoch))


def deleteUser(user):
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

def userAPIKey(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT APIKEY FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    return(fetched)


def updateEDKey(user,EDKey):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute(
            "UPDATE USER_SESSION (EDKEY) VALUES (?) WHERE USER=? ", [EDKey],[user])

def updateReport(user):
    epoch = time.time()
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("UPDATE USER_SESSION (TIME) VALUES (?) WHERE USER=? ", [epoch],[user])

def userKeys(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT PRIVATE_KEY PUBLIC_KEY FROM USER_SESSION WHERE USER=?", [user])
    
    fetched = mouse.fetchall()
    return(fetched)
