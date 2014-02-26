'''
Team 3
'''

import socket
from myClientSend import *
from myClientReceive import *
import sys
from struct import unpack
import json

success_handlers = {
    "createAccount": create_success,
    "getBalance": balance_success,
    "deposit": deposit_success,
    "withdraw": withdraw_success,
    "closeAccount": delete_success,
    "endSession": end_session_success
}

def getInput():
    print '''
CONNECTED TO ATM SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Deposit Money to an Account
    (4) Withdraw Money from an Account
    (5) Check the Balance of an Account
    (6) End Session
    '''
    netBuffer = raw_input('>> ')
    return netBuffer

def processInput(netBuffer, mySocket):
    #create
    if netBuffer == str(1):
        create_request(mySocket)

    #delete
    elif netBuffer == str(2):
        delete_request(mySocket)

    #deposit
    elif netBuffer == str(3):
        deposit_request(mySocket)
        
    #withdraw
    elif netBuffer == str(4):
        withdraw_request(mySocket)
        
    #balance
    elif netBuffer == str(5):
        balance_request(mySocket)
        
    #quit
    elif netBuffer == str(6):
        end_session(mySocket)
        
    return
        
def getResponse(mySocket):
    #wait for server responses...
    while True:
        try:
            retBuffer = mySocket.recv( 4096 )
        except:
            #close the client if the connection is down
            print "ERROR: connection down"
            sys.exit()
            
        if len(retBuffer) > 12:
            header = unpack('!IQ',retBuffer[0:12])
            #only allow correct version numbers
            if header[0] == VERSION:
                length = header[1]
                msg = retBuffer[12:]

                #check that we have the entire message
                if (len(msg) != length):
                    print "ERROR: did not receive entire message"
                    continue

                try:
                    msg_obj = json.loads(msg)
                except:
                    print "ERROR: unable to read message"
                    continue    

                if not msg_obj['success']:
                    print "ERROR: " + msg_obj['message']
                else:
                    try:
                        success_handlers[msg_obj['operation']](mySocket, msg_obj['data'])
                    except KeyError:
                        print "ERROR: operation not recognized."
                        continue
            else:
                print "ERROR: wrong protocol version."
                continue
        return
    
if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print "ERROR: Usage 'python myClient.py <host> <port>'"
        sys.exit()
        
    #get the address of the server
    myHost = sys.argv[1]
    myPort = sys.argv[2]
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect ( ( myHost, int(myPort)) )
    except:
        print "ERROR: could not connect to " + myHost + ":" + myPort
        sys.exit()

    while True:
        netBuffer = getInput()
        #menu selection and function priming
        processInput(netBuffer, mySocket)
        getResponse(mySocket)

    mySocket.close()