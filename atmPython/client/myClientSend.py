'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

VERSION = 1

from struct import pack
from sys import maxint, exit
import json

def prepare_send(conn, operation, args):
    json_str = json.dumps({"operation": operation, "arguments": args})
    json_length = len(json_str)

    send_message(pack('!IQ', VERSION,json_length) + json_str, conn)

#create new account
def create_request(conn):
    print "CREATING AN ACCOUNT \n"
    print "enter a starting balance:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    print "enter a an account number 1-100(input 0 for a random number):"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        elif(netBuffer == 0):
            act = -1
            break
    
    args = {"acct_number": act, "balance": bal}
    prepare_send(conn, "createAccount", args)
    return

#delete an existing account
def delete_request(conn):
    print "DELETING AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    
    args = {"acct_number": act}
    prepare_send(conn, "closeAccount", args)
    return

#deposit to an existing account
def deposit_request(conn):
    print "DEPOSITING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    print "enter an amount to deposit:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break

    args = {"acct_number": act, "amount": bal}
    prepare_send(conn, "deposit", args)
    return

#withdraw from an existing account
def withdraw_request(conn):
    print "WITHDRAWING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        
    print "enter an amount to withdraw:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    args = {"acct_number": act, "balance": bal}
    prepare_send(conn, "withdraw", args)
    return

#withdraw from an existing account
def balance_request(conn):
    print "CHECKING THE BALANCE OF AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    args = {"acct_number": act}
    prepare_send(conn, "getBalance", args)
    return

#end a session
def end_session(conn):
    args = {}
    prepare_send(conn, "endSession", args)
    return

def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print "ERROR: connection down"
            exit()
    return
