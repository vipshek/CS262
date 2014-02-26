'''
CS 262: Distributed Systems

Created on Feb 18, 2010

Restructured and re-factored by Jim Waldo, 2/17/2014
'''

import socket
import struct
import myServerReceive
import myServerSend
from myServerSend import unknown_opcode
import thread
import json

version = 1
#opcode associations
opcodes = {'createAccount': myServerReceive.create_request, 
           'getBalance': myServerReceive.balance_request,
           'deposit': myServerReceive.deposit_request,
           'withdraw': myServerReceive.withdraw_request,
           'closeAccount': myServerReceive.delete_request,
           'endSession': myServerReceive.end_session
           }
HEADER_LENGTH = 12

def recordConnect(log, addr):
    print 'Opened connection with ' + addr
    log.write('Opened connection with ' + addr + '\n')
    log.flush()
    
#thread for handling clients
def handler(conn,lock, myData):
    #keep track of erroneous opcodes
    second_attempt = 0
    while True:   
        #retrieve header
        try:
            netbuffer = conn.recv( 4096 )
        except:
            #close the thread if the connection is down
            thread.exit()
        #if we receive a message...
        if len(netbuffer) >= HEADER_LENGTH:
            #unpack it...
            header = struct.unpack('!IQ',netbuffer[0:HEADER_LENGTH])
            #only allow correct version numbers and buffers that are of the appropriate length
            if header[0] == version and len(netbuffer) == header[1] + HEADER_LENGTH:
                json_data = json.loads(netbuffer[HEADER_LENGTH:])
                #try to send packet to correct handler
                try:
                    opcodes[json_data['operation']](conn,json_data,myData,lock)
                #catch unhandled opcodes
                except KeyError:
                    if(second_attempt):
                        #disconnect the client
                        myServerSend.end_session_success(conn)
                        conn.close()
                        return
                    else:
                        #send incorrect opcode message
                        second_attempt = 1
                        unknown_opcode(conn)


if __name__ == '__main__':
    #set up log
    log = open('log.txt', 'a')
    #data structure for storing account information
    myData = dict()

    #setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',8080))
    mySocket.listen(5)  #param represents the number of queued connections

    #listening for connections
    while True:
        #This is the simple way to start this; we could also do a SELECT
        conn, address = mySocket.accept()
        #log connection
        recordConnect(log, str(address)) 
        #start a new thread
        lock = thread.allocate_lock()
        thread.start_new_thread(handler, (conn, lock, myData))

    log.close()