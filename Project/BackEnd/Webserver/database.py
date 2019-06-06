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


# if __name__ == "__main__":
#     updatePublicMessages('tmag741','HELLO WORLD',123)

