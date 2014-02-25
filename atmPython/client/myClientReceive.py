'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from struct import unpack
from sys import exit

#create new account
def create_success(conn, data):
    print "Account creation successful " + str(data['acct_number'])
    return

#delete an existing account
def delete_success(conn, data):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn, data):
    print "Deposit success. The updated balance: " + str(data['balance'])
    return

#withdraw from an existing account
def withdraw_success(conn, data):
    print "Withdrawal success. The updated balance: " + str(data['balance'])
    return

#withdraw from an existing account
def balance_success(conn, data):
    print "The balance of that account is: " + str(data['balance'])
    return

#end a session
def end_session_success(conn, data):
    print "SHUTTING DOWN"
    conn.close()
    exit()
    return

#handle invalid opcodes
def unknown_opcode(conn):
    print "ERROR: INCORRECT OPCODE"
    return