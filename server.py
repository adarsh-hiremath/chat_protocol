import socket
import random


# import thread module
from _thread import *
import threading


# map from UUIDs to a queue of unreceived messages sent to that UUID
pending_messages = {}

# map from UUIDs to information about that account (name)
accounts = {}

# map from UUIDs to connections of all currently connected clients
live_users = {}

# create a new account with given name, connect it to the current socket
def create_account(name, connection):

    # generate a unique uuid
    uuid = str(random.randint(0, 1000))
    while uuid in accounts:
        uuid  = str(random.randint(0,1000))

    # add the new user to accounts and live users
    accounts[uuid] = name
    live_users[uuid] = connection

    # send acknowledgment of new account creation
    return f"\nNew account created! User ID: {uuid} \n"

def delete_account(uuid): 
    accounts.pop(uuid, None)
    return f"\nAccount with User ID {uuid} has been deleted\n"

def list_accounts(): 
    acc_str = "\n Active Accounts:\n"
    for acc in accounts: 
        next_acc = "\n" + accounts[acc] + " (UUID: " + acc + ")" + "\n"
        acc_str += next_acc
    return acc_str

def login(uuid, connection): 
    if uuid in live_users:
        return f"\nUser {uuid} already logged in, please try again."
    else: 
        live_users[uuid] = connection

        # deliver unreceived messages 
        while pending_messages[uuid]:
            send_msg(uuid, pending_messages[uuid][0])
            pending_messages[uuid].pop(0)

        return f"\nLogged in as user {uuid}!"

# send a message to the given uuid
def send_msg(uuid, msg):
    print(f"connection: {live_users[uuid]}")
    live_users[uuid].send(msg.encode('UTF-8'))
    return f"\nMessage sent to {uuid}\n"

def wire_protocol(connection):
    while True:
        # preprocess the message
        msg = connection.recv(2048)
        msg_str = msg.decode('UTF-8')
        msg_list = msg_str.split('|')
        op_code = msg_list[0]
        # create an account
        # usage: c|<username>
        if op_code == 'c':
            msg = create_account(msg_list[1], connection)
        
        # log into an account
        # usage: l|<uuid>
        elif op_code == 'l':
            msg = login(msg_list[1], connection)

        # list users and their names
        # usage: u
        elif op_code == 'u':
            msg = list_accounts()

        # send a message
        # usage: s|<recipient_uuid>|<message>
        elif op_code == 's':
            msg = send_msg(msg_list[1], msg_list[2])

        # delete account
        # usage: d|<uuid_to_delete>
        elif op_code == 'd':
            msg = delete_account(msg_list[1])

        # invalid request
        else:
            # TODO: give a more descriptive error message
            msg = "\nInvalid Request\n"

        # send encoded acknowledgment to the connected client
        connection.send(msg.encode('UTF-8')) 


def Main():
    host = "127.0.0.1"
    port = 2048

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(100)

    while True:
        connection, address = server.accept()
        print('\nConnected to :', address[0], ':', address[1])
        start_new_thread(wire_protocol, (connection,))
    server.close()


if __name__ == '__main__':
    Main()
