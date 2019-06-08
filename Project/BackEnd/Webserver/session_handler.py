import sqlite3
from sqlite3 import Error
import time


SESSION_DB = "session.db"


def addUser(user, apikey):
    epoch = time.time()
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("DELETE FROM USER_SESSION WHERE USER=?", [user])
        db.execute("INSERT INTO USER_SESSION (USER,APIKEY,TIME,STATUS) VALUES (?,?,?,?)", (user, apikey, epoch,"online"))

def hasData():
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT 1 FROM USER_SESSION ")

    fetched = mouse.fetchall()
    return(len(fetched) == 0)

def deleteUser(user):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("DELETE FROM USER_SESSION WHERE USER=?", [user])


def userKeys(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute(
            "SELECT PRIVATE_KEY, PUBLIC_KEY FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    return(fetched)

def userPrivateData(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute(
            "SELECT PRIVATE_DATA FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    return(fetched[0][0])

def userCheck(user):
    check = False
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT USER FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    if(len(fetched) >= 1):
        check = True

    return(check)

def userAPIKey(user):
    with sqlite3.connect(SESSION_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT APIKEY FROM USER_SESSION WHERE USER=?", [user])

    fetched = mouse.fetchall()
    return(fetched[0][0])


def updatePrivateData(user, private_data):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("UPDATE USER_SESSION SET PRIVATE_DATA = ? WHERE USER = ?", (private_data, user))


def updateKeys(user, private, public):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("UPDATE USER_SESSION SET PRIVATE_KEY = ?, PUBLIC_KEY = ? WHERE USER = ?", (private, public, user))


def updateEDKey(user, EDKey):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("UPDATE USER_SESSION SET EDKEY = ? WHERE USER = ? ", (EDKey, user))


def updateReport(user):
    epoch = time.time()
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("UPDATE USER_SESSION SET TIME = ? WHERE USER=? ",(epoch, user))

def updateList(user,address,location,public_key,time,status):
    with sqlite3.connect(SESSION_DB) as db:
        db.execute("DELETE FROM USER_LIST WHERE USER=?", [user])
        db.execute("INSERT INTO USER_LIST (USER,ADDRESS,LOCATION,PUBLIC_KEY,TIME,STATUS) VALUES (?,?,?,?,?,?)",
                   (user, address, location, public_key, time, status))

def fetchList():
    with sqlite3.connect(SESSION_DB) as db:
        mouse=db.cursor()
        mouse.execute("SELECT * FROM USER_LIST")
    
    fetched=mouse.fetchall()
    return fetched
