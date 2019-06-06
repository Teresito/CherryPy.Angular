import sqlite3
from sqlite3 import Error

#Consider making a session with RAM
database = "messages.db"


#checkmessages filter later
def updatePublicMessages(user,message,time):
    with sqlite3.connect(database) as db:
        db.execute(
            "INSERT INTO PUBLIC_MESSAGES (USER,MESSAGE,TIME) VALUES (?,?,?)", (user, message, time))
   
def updatePrivateMessages(user,message,cameFrom,time):
    with sqlite3.connect(database) as db:
        db.execute(
            "INSERT INTO PRIVATE_MESSAGES (USER,MESSAGE,FROM,TIME) VALUES (?,?,?)", (user, message, cameFrom, time))

def fetchPublicMessages():
    with sqlite3.connect(database) as db:
        mouse = db.cursor()
        mouse.execute("SELECT * FROM PUBLIC_MESSAGES ORDER BY TIME DESC")

    fetched = mouse.fetchall()
    jsonbody = {}
    messageList = []
    for data in fetched:
        messageList.append(data)

    jsonbody['public_messages'] = messageList
    return(jsonbody)

if __name__ == "__main__":
    print(fetchPublicMessages())

