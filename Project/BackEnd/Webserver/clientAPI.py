import json
import urllib.request
import helper
import time
import centralAPI
import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
import nacl.pwhash

def ping_check(host,serverIP,location):
    url = host + "/api/ping_check"

    server_time = str(time.time())
    header = {
        'content-type':'application/json'
    }
    payload = {
        'my_time':server_time,
        'my_active_usernames': 'N/A',
        'connection_address': serverIP,
        'connection_location': location
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')

    return(helper.Request(url, payload_b, header))

    
def checkmessage(host):
    url = host + "/api/checkmessages"
    payload = {
        'since': str(1559299221)
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')    
    return(helper.Request(url,payload_b,None))



def rx_broadcast(host,message,serverRecord,privKey):
    url = host + "/api/rx_broadcast"

    timeNOW = str(time.time())

    header = {
        'content-type': 'application/json'
    }

    signing_key = nacl.signing.SigningKey(privKey, encoder=nacl.encoding.HexEncoder)
    message_bytes = bytes(serverRecord + message + timeNOW, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    payload = {
        'loginserver_record':serverRecord,
        'message': message,
        'sender_created_at': timeNOW,
        'signature':signature_hex_str,
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, header))


def rx_privatemessage(host, server_record, encrypted_message, target_key, target_user, private_key):
    url = host + "/rx_privatemessage"
    timeNOW = str(time.time())

    signing_key = nacl.signing.SigningKey(private_key, encoder=nacl.encoding.HexEncoder)
    message_bytes = bytes(server_record + target_key + target_user +
                          encrypted_message + timeNOW, encoding='utf-8')
    signed = signing_key.sign(message_bytes, encoder=nacl.encoding.HexEncoder)
    signature_hex_str = signed.signature.decode('utf-8')

    header = {
        'content-type': 'application/json'
    }

    payload = {
        "loginserver_record": server_record,
        "target_pubkey": target_key,
        "target_username": target_user,
        "encrypted_message": encrypted_message,
        "sender_created_at": timeNOW,
        'signature': signature_hex_str
    }
    
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, header))
