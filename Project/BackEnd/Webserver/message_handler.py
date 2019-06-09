import sqlite3
from sqlite3 import Error
import pprint
MESSAGE_DB = "messages.db"


def updatePublicMessages(user, message, time, record, signature):
    with sqlite3.connect(MESSAGE_DB) as db:
        db.execute(
            "INSERT INTO PUBLIC_MESSAGES (USER,MESSAGE,TIME,LOGINSERVER_RECORD,SIGNATURE) VALUES (?,?,?,?,?)", (user, message, time, record, signature))
   

def updatePrivateMessages(user, message, cameFrom, time, record, signature,public_key):
    with sqlite3.connect(MESSAGE_DB) as db:
        db.execute(
            "INSERT INTO PRIVATE_MESSAGES (USER,MESSAGE,FROM_USER,TIME,USER_PUBLICKEY,SIGNATURE,LOGINSERVER_RECORD) VALUES (?,?,?,?,?,?,?)", (user, message, cameFrom, time,public_key,signature,record))

def fetchPublicMessages():
    with sqlite3.connect(MESSAGE_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT * FROM PUBLIC_MESSAGES ORDER BY TIME DESC")

    fetched = mouse.fetchall()
    jsonbody = {}
    messageList = []
    for data in fetched:
        messageList.append(data)

    jsonbody['public_messages'] = messageList
    return(jsonbody)

def fetchPrivateMessages():
    with sqlite3.connect(MESSAGE_DB) as db:
        mouse = db.cursor()
        mouse.execute("SELECT * FROM PRIVATE_MESSAGES ORDER BY TIME DESC")

    fetched = mouse.fetchall()
    jsonbody = {}
    messageList = []
    for data in fetched:
        messageList.append(data)

    jsonbody['private_messages'] = messageList
    return(jsonbody)

# if __name__ == "__main__":
#     messageList = fetchPrivateMessages()

#     wat = []
#     for message in messageList['private_messages']:
#         if(message[0] == 'tmag741'):
#             # print(message[1]) # ENCRYPTED
#             # print(message[3]) # TIME
#             # print(message[2]) # FROM
#             wat.append(message)

# pprint.pprint(wat[0][0])