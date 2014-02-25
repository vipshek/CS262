'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''
from myServerSend import general_failure, end_session_success,create_success, delete_success,deposit_success,withdraw_success,balance_success
from struct import unpack
import sys

#create new account
def create_request(conn,json_data,myData,lock):
    balance, acct_number = json_data.arguments.balance, json_data.arguments.acct_number
    lock.acquire()
    try:
        if balance < 0:
            general_failure(conn, 'createAccount', "invalid balance")
        elif acct_number < 0 or acct_number > 100:
            general_failure(conn, 'createAccount', "invalid account number")
        elif acct_number in myData:
            general_failure(conn, 'createAccount', "account already in use")
        else:
            myData[acct_number] = balance
            create_success(conn,acct_number)

        """
        #generate a value if it was -1
        elif values[1] == -1:
            i = 1
            while i in myData:
                i+=1
                if i == 101:
                    general_failure(conn, 'create',"no remaining accounts")
                    return
            act = i
        """
    finally:
        lock.release()
        print myData
    
    return

#delete an existing account
def delete_request(conn,json_data,myData,lock):
    acct_number = json_data.arguments.acct_number
    lock.acquire()
    try:
        if acct_number < 0 or acct_number > 100:
            general_failure(conn, 'closeAccount',"invalid account number")
        elif acct_number not in myData:
            general_failure(conn, 'closeAccount',"nonexistent account number")
        elif myData[acct_number] != 0:
            general_failure(conn, 'closeAccount',"nonzero money in that account")
        else:
            del myData[acct_number]
            delete_success(conn)
    finally:
        lock.release()
        print myData
    return

#deposit to an existing account
def deposit_request(conn,json_data,myData,lock):
    amount, acct_number = json_data.arguments.amount, json_data.arguments.acct_number
    lock.acquire()
    try:
        if amount < 0:
            general_failure(conn, 'deposit', "invalid deposit amount")
        elif acct_number < 0 or acct_number > 100:
            general_failure(conn, 'deposit', "invalid account number")
        elif acct_number not in myData:
            general_failure(conn, 'deposit', "nonexistent account number")
        else:
            if amount < sys.maxint - myData[acct_number] - 1:
                myData[acct_number] += amount
                deposit_success(conn, myData[acct_number])
            else:
                general_failure(conn,'deposit',"account overflow... damn you are rich")
    finally:
        lock.release()
        print myData
    
    
    return

#withdraw from an existing account
def withdraw_request(conn,json_data,myData,lock):
    amount, acct_number = json_data.arguments.amount, json_data.arguments.acct_number

    lock.acquire()
    try:
        if amount < 0:
            general_failure(conn, 'withdraw', "invalid withdrawal amount")
        elif acct_number < 0 or acct_number > 100:
            general_failure(conn, 'withdraw', "invalid account number")
        elif acct_number not in myData:
            general_failure(conn, 'withdraw', "nonexistent account number")
        else:
            if myData[acct_number] - amount >= 0:
                myData[acct_number] -= amount
                withdraw_success(conn, myData[acct_number])
            else:
                general_failure(conn,'withdraw',"not enough money in account")
    finally:
        lock.release()
        print myData 
    return

#withdraw from an existing account
def balance_request(conn,json_data,myData,lock):
    acct_number = json_data.arguments.acct_number

    if acct_number < 0 or acct_number > 100:
        general_failure(conn,'getBalance',"invalid account number")

    #no need to lock: we are just reading a value from a dict, which is thread-safe
    #get the current balance
    try:
        balance = myData[acct_number]
    except KeyError:
        general_failure(conn,'getBalance',"nonexistent account")
        return

    balance_success(conn,balance)
    return

#end a session
def end_session(conn,json_data,myData,lock):
    end_session_success(conn)
    conn.close()
    return