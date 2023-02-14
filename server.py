import socket
import random
from _thread import *
import re

# A dictionary with UUIDs as keys and pending messages as values. 
pending_messages = {}

# A dictionary with UUIDs as keys and account names as values. 
accounts = {}

# A dictionary with UUIDs as keys and connection references as values.
live_users = {}

# Create a new account with a given name and associate the account with the appropriate socket. 
def create_account(name, connection): 
    uuid = str(random.randint(0, 1000))
    while uuid in accounts:
        uuid  = str(random.randint(0,1000))
    accounts[uuid] = name
    live_users[uuid] = connection
    return f"\nNew account created! User ID: {uuid} \n"

# Delete the account from the list of accounts. 
def delete_account(uuid): 
    accounts.pop(uuid, None)
    return f"\nAccount with User ID {uuid} has been deleted\n"

# Iterate through the accounts and generate a string with all the UUIDs and account names.
def list_accounts(): 
    acc_str = "\n Active Accounts:\n"
    for acc in accounts: 
        next_acc = "\n" + accounts[acc] + " (UUID: " + acc + ")" + "\n"
        acc_str += next_acc
    return acc_str

# Check that the user is not already logged in, log in to a particular user, and deliver unreceived messages if applicable.
def login(uuid, connection): 
    if uuid in live_users:
        print(f"User {uuid} has already logged in\n")
        return f"\nUser {uuid} already logged in, please try again."
    else: 
        live_users[uuid] = connection
        while pending_messages[uuid]:
            send_msg(uuid, pending_messages[uuid][0])
            pending_messages[uuid].pop(0)
        return f"\nLogged in as user {uuid}!"

# Send a message to the given UUID.
def send_msg(uuid, msg):
    print(f"connection: {live_users[uuid]}")
    live_users[uuid].send(msg.encode('UTF-8'))
    return f"\nMessage sent to {uuid}"

# Iterate through the accounts and generate a string with all the UUIDs and account names.
def filter_accounts(): 
    acc_lst = [accounts[acc] for acc in accounts]
    
    return acc_str

# The main wire protocol specifying how information should be sent and received. 
def wire_protocol(connection):
    # Main server thread that continues running until the connection is closed.
    while True:
        # Preprocess the message by decoding it and splitting it by delimeter. 
        msg = connection.recv(4096)
        msg_str = msg.decode('UTF-8')
        msg_list = msg_str.split('|')
        op_code = msg_list[0]

        # Create an account.
        # Usage: c
        if op_code == 'c':
            msg = create_account(msg_list[1], connection)
        
        # Log into an account.
        # Usage: l|<uuid>
        elif op_code == 'l':
            msg = login(msg_list[1], connection)

        # List all users and their names. 
        # Usage: u
        elif op_code == 'u':
            msg = list_accounts()

        # Send a message to a user. 
        # Usage: s|<recipient_uuid>|<message>
        elif op_code == 's':
            msg = send_msg(msg_list[1], msg_list[2])

        # Delete an account
        # Usage: d|<uuid_to_delete>
        elif op_code == 'd':
            msg = delete_account(msg_list[1])
    
        # Filter accounts using a certain wildcard
        # Usage: f|<filter_wildcard>
        elif op_code == 'f':
            msg = filter_accounts(msg_list[1])

        # Handles an invalid request and lists the correct usage for the user. 
        else:
            msg = "\nInvalid request, see below for usage help:"
            msg += "\nCreate an account, usage: c|<username>"
            msg += "\nLog into an account, usage: l|<uuid>"
            msg += "\nList users and their names, usage: u"
            msg += "\nSend a message, usage: s|<recipient_uuid>|<message>"
            msg += "\nDelete an account, usage: d|<uuid_to_delete>"

        # send encoded acknowledgment to the connected client
        connection.send(msg.encode('UTF-8')) 


def Main():
    # Set IP address and local port.
    ip = "127.0.0.1"
    port = 2048
    
    # Specify the address domain and read properties of the socket. 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Connect to the server at the specified port and IP address. 
    server.bind((ip, port))

    # Listen for a maximum of 100 active connections (can be adjusted).
    server.listen(100)

    # Main loop for the server to listen to client requests.
    while True:
        connection, address = server.accept()
        print('\nConnected to :', address[0], ':', address[1])
        start_new_thread(wire_protocol, (connection,))
        
if __name__ == '__main__':
    Main()
