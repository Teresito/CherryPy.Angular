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

    payload = {
        'my_time':server_time,
        'my_active_usernames': 'N/A',
        'connection_address': serverIP,
        'connection_location': location
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, None))

    
def checkmessage(host):
    url = host + "/api/checkmessages"
    payload = {
        'since': str(1559299221)
    }
    payload_b = bytes(json.dumps(payload), 'utf-8')    
    return(helper.Request(url,payload_b,None))

def rx_broadcast(host,message,serverRecord,privKey):
    url = host + "/api/rx_broadcast"

    message = bytes(message,'utf-8')
    timeNOW = str(time.time())

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
    return(helper.Request(url,payload_b,None))


def rx_privatemessage(host, serverRecord, message, privkey, targetKey, target):
    url = host + "/rx_privatemessage"
    timeNOW = str(time.time())

    message = bytes(message, 'utf-8')

    verifykey = nacl.signing.VerifyKey(targetKey, encoder=nacl.encoding.HexEncoder)
    publickey = verifykey.to_curve25519_public_key()
    
    sealed_box = nacl.public.SealedBox(publickey)
    
    encrypted = sealed_box.encrypt(message, encoder=nacl.encoding.HexEncoder)
    message_hex_str = encrypted.decode('utf-8')

    payload = {
        "loginserver_record": serverRecord,
        "target_pubkey": targetKey,
        "target_username": target,
        "encrypted_message": message_hex_str,
        "sender_created_at": timeNOW,
    }
    
    payload_b = bytes(json.dumps(payload), 'utf-8')
    return(helper.Request(url, payload_b, None))
        

if __name__ == "__main__":
    ip = "http://172.23.1.134:8080/api/ping_check"
    #ip = "http://192.168.1.6"
    print(ping_check(ip,ip))
