import base64
import session_handler
import helper
import clientAPI
def broadcast(record,message,private_key,hostIP):
    errorCount = 0
    toCall = 0
    uniCount = 0
    outSide = 0

    unparsed_list = session_handler.fetchList()
    for host in unparsed_list:

        hostAddress = host[1]
        hostLocation = host[2]

        if(hostLocation == '1' or hostLocation == '0'):
            uniCount += 1
        elif(hostLocation == '2'):
            outSide += 1

        if(hostLocation == hostLocation and hostAddress != hostIP):
            toCall += 1
            if(hostAddress[:4] != "http"):
                hostAddress = "http://" + hostAddress

            clientResponse = clientAPI.rx_broadcast(
                hostAddress, message, record, private_key)
            if(clientResponse == "error"):
                errorCount += 1
    print("=================")
    print("Total broadcast errors: "+str(errorCount)+" out of "+str(toCall))
    print("=================")

def updateDBList():
    url = "http://cs302.kiwi.land/api/list_users"
    username = "tmag741"
    password = "Teresito_419588351"
    credentials = ('%s:%s' % (username, password))
    b64_credentials = base64.b64encode(credentials.encode('ascii'))
    header = {
        'Authorization': 'Basic %s' % b64_credentials.decode('ascii'),
        'Content-Type': 'application/json; charset=utf-8',
    }

    json_response = helper.Request(url, None, header)

    if (json_response['response'] == 'ok'):
            user_list = json_response['users']
    else:
        user_list = []
        return None

    for person in user_list:   
        user = person['username']
        address = person['connection_address']
        location = person['connection_location']
        public_key = person['incoming_pubkey']
        time = person['connection_updated_at']
        status = person['status']
        session_handler.updateList(user,address,location,public_key,time,status)


def ping_checkServers(hostIP,location):
    errorCount = 0
    toCall = 0;
    uniCount = 0
    outSide  = 0

    unparsed_list = session_handler.fetchList()
    # print("=================")
    # for user in unparsed_list:
    #     print(user[2] == '2')
    # print("=================")
    for host in unparsed_list:
        
        hostAddress = host[1]
        hostLocation = host[2]

        if(hostLocation == '1' or hostLocation == '0'):
            uniCount += 1
        elif(hostLocation == '2'):
            outSide += 1

        if(hostLocation == location and hostAddress != hostIP):
            toCall += 1
            if(hostAddress[:4] != "http"):
                hostAddress = "http://" + hostAddress

            clientResponse = clientAPI.ping_check(hostAddress,hostIP,location)
            if(clientResponse == "error"):
                errorCount += 1
    
    print("=================")
    print("Total errors: "+str(errorCount)+" out of "+str(toCall))
    print("Total in uni: ", (uniCount))
    print("Total in outside: ", (outSide))
    print("=================")

if __name__ == "__main__":
    ping_checkServers("SOMEWHERE","2")
