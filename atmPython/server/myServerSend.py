'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''

from struct import pack
import json

VERSION = 1
"""
Send json data over the network
"""
def json_send(conn, data):
    # encode data as json
    json_str = json.dumps(data)
    json_length = len(json_str)

    # send
    conn.send(pack('!IQ',VERSION,json_length) + json_str)

    return

def general_failure(conn, type, reason):
    #encode and send the data
    data = {"operation": type, "success": False, "message": reason}

    json_send(conn, data)
    return

def json_success(conn, operation, data):
    json_data = {"operation": operation, "success": True, "data": data}
    json_send(conn, json_data)
    return

#create new account
def create_success(conn,act):
    json_success(conn, "createAccount", {"acct_number": act})
    return

#delete an existing account
def delete_success(conn):
    json_success(conn, "closeAccount", {})
    return

#deposit to an existing account
def deposit_success(conn,bal):
    json_success(conn, "deposit", {"balance": bal})
    return

#withdraw from an existing account
def withdraw_success(conn,bal):
    json_success(conn, "withdraw", {"balance": bal})
    return

#withdraw from an existing account
def balance_success(conn,bal):
    json_success(conn, "getBalance", {"balance": bal})
    return

#end a session
def end_session_success(conn):
    json_success(conn, "endSession", {})
    return

#handle invalid opcodes
def unknown_opcode(conn):
    #encode and send the data
    data = {"operation": "unknown", "success": False, "message": "unknown opcode"}

    json_send(conn, data)
    return


