'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''

version = '\x01'

import socket
from myClientSend import *
from myClientReceive import *
import sys
from struct import unpack

#opcode associations; note that these opcodes will be returned by the serverzl;khjapoiwpe
opcodes = {'\x11': create_success,
           '\x12': general_failure,  
           '\x21': delete_success,
           '\x22': general_failure,
           '\x31': deposit_success,
           '\x32': general_failure,
           '\x41': withdraw_success,
           '\x42': general_failure,
           '\x51': balance_success,
           '\x52': general_failure,
           '\x61': end_session_success,
           '\x62': unknown_opcode
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
            retBuffer = mySocket.recv( 1024 )
        except:
            #close the client if the connection is down
            print "ERROR: connection down"
            sys.exit()
            
        if len(retBuffer) != 0:
            
            header = unpack('!cIc',retBuffer[0:6])
            #only allow correct version numbers
            if header[0] == version:
                opcode = header[2]
                #send packet to correct handler
                try:
                    opcodes[opcode](mySocket,retBuffer)
                except KeyError:
                    break
            #mySocket.send ('\x01\x01\x02\x03\x53\x10\x12\x34')
            break
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