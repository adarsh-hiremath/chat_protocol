import socket
import random
from _thread import *
import re
from termcolor import colored

# A dictionary with username as key and pending messages as values. 
pending_messages = {}

# A dictionary with usernames as keys and account names as values. 
accounts = []

# A dictionary with usernames as keys and connection references as values.
live_users = {}

# Create a new account with a given name and associate the account with the appropriate socket. 
def create_account(msg_list, connection): 
    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage:   c|<username>\n", "red"))
        connection.send(msg.encode('UTF-8'))
        return 

    username = msg_list[1]

    if username in accounts: 
        print(f"\nUser {username} account creation rejected\n")
        msg = colored(f"\nAccount {username} already exists!\n", "red")
        return msg
    
    if not re.fullmatch("\w{2,20}", username):
        print(f"User {username} account creation rejected")
        msg = colored(f"\nUsername must be alphanumeric and 2-20 characters!\n", "red")
        return msg
    
    accounts.append(username)
    print(f"\nUser {username} account created")
    msg = f"\nNew account created! User ID: {username}. Please log in.\n"
    return msg

# Delete the account from the list of accounts. 
def delete_account(msg_list): 
    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage:   d|<confirm_account>\n", "red"))
        return msg

    username = msg_list[1]

    username = msg_list[1]
    print(f"\nUser {username} requesting account deletion.\n")

    if username in accounts: 
        accounts.remove(username)
        if pending_messages.get(username):
            pending_messages.pop(username)
        print(f"\nUser {username} account deleted.\n")
        msg = colored(f"\nAccount {username} has been deleted.\n", "green")
        return msg

# Displays all account names and their status (live or not). 
def list_accounts(): 
    print(f'\nListing accounts\n')

    if len(list(accounts)) < 0: 
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                    (colored("(live)", "green") if u in live_users else ""))
                    for u in accounts]) + "\n"
    
    else: 
        acc_str = colored("\nNo existing users!\n", "red")

    return acc_str

# Check that the user is not already logged in, log in to a particular user, and deliver unreceived messages if applicable.
def login(msg_list, connection): 
    print(f"\nLogin as user {username} requested\n")

    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage:   l|<username>\n", "red"))
        return msg
    
    username = msg_list[1]

    if username in live_users: 
        print(f"\Login as {username} denied.\n")
        msg = colored(f"\nUser {username} already logged in. Please try again.\n", "red")
        return msg
    
    elif username not in accounts: 
        print(f"\nLogin as {username} denied.\n")
        msg = colored(f"\nUser {username} does not exist. Please create an account.\n", "red") 
        return msg
    
    else: 
        live_users[username] = connection
        print (f"\nLogin as user {username} completed.\n")
        msg = colored(f"\nLogin successful - welcome back {username}!\n", "green")
        if len(pending_messages.get(username)) > 0: 
            print(f"\nDelivering pending messages to {username}.\n")
            send_msg(username, f"\nYou have pending messages! Delivering the  messages now.\n")
            while pending_messages.get(username):
                send_msg(username, pending_messages[username][0])
                pending_messages[username].pop(0)
        return msg

# Send a message to the given user.
def send_msg(recipientName, msg):
    print(f"\nRequest received to send message to {recipientName}.\n")

    if recipientName in accounts: 
        if recipientName in live_users:
            live_users[recipientName].send(msg.encode('UTF-8'))
            print(f"\nMessage sent to {recipientName}.\n")
            msg = colored(f"\nMessage sent to {recipientName}.\n", "green")
        else: 
            if pending_messages.get(recipientName):
                pending_messages[recipientName].append(msg)
            else: 
                pending_messages[recipientName] = [msg]
            print(f"\nMessage will be sent to {recipientName} after the account is online.\n")
            msg = colored(f"\nMessage will be delivered to {recipientName} after the account is online.\n", "green")
        return msg

    else: 
        msg = colored("\nMessage failed to send! Verify recipient username.\n", "red")
        print(f"\nRequest to send message to {recipientName} denied.\n")
        return msg

# Filter accounts by a given regex.
def filter_accounts(msg_list): 
    print(f'\nFiltering accounts.\n')

    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage:   f|<filter_regex>\n", "red"))
        return msg
    
    request = msg_list[1]

    # Find a list of matching accounts.
    fltr = request.filter
    fun = lambda x: re.fullmatch(fltr, x)
    filtered_accounts = list(filter(fun, accounts))

    # Output a list of users, and whether they are currently online.
    if len(list(filtered_accounts)) > 0:
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                (colored("(live)", "green") if u in live_users else ""))
                for u in filtered_accounts]) + "\n"

    # No matching accounts on the server.
    else:
        acc_str = colored("\nNo matching users!\n", "red")

    return acc_str

# The main wire protocol specifying how information should be sent and received. 
def wire_protocol(connection):
    # Main server thread that continues running until the connection is closed.
    while True:
        # Preprocess the message by decoding it and splitting it by delimeter.
        msg = connection.recv(4096)
        msg_str = msg.decode('UTF-8')
        msg_list = msg_str.split('|')
        msg_list = [elt.strip() for elt in msg_list]
        op_code = msg_list[0].strip()

        # Create an account.
        # Usage: c|<username>
        if op_code == 'c':
            msg = create_account(msg_list, connection)
        
        # Log into an account.
        # Usage: l|<username>
        elif op_code == 'l':
            msg = login(msg_list, connection)

        # List all users and their names. 
        # Usage: u
        elif op_code == 'u':
            msg = list_accounts()

        # Send a message to a user. 
        # Usage: s|<recipient_username>|<message>
        elif op_code == 's':
            if len(msg_list) != 2: 
                msg = (colored("\nInvalid arguments! Usage:   s|<recipient_username>|<message>\n", "red"))
            else: 
                msg = send_msg(msg_list[1], msg_list[2])

        # Delete an account
        # Usage: d|<confirm_username>
        elif op_code == 'd':
            msg = delete_account(msg_list)
    
        # Filter accounts using a certain wildcard.
        # Usage: f|<filter_regex>
        elif op_code == 'f':
            msg = filter_accounts(msg_list)
        
        elif op_code == 'h':
            msg = "\nUsage help below:\n"
            msg += "\nCreate an account.        c|<username>"
            msg += "\nLog into an account.      l|<username>"
            msg += "\nSend a message.           s|<recipient_username>|<message>"
            msg += "\nFilter accounts.          f|<filter_regex>"
            msg += "\nDelete your account.      d|<confirm_username>"
            msg += "\nList users and names.     u"
            msg += "\nUsage help (this page).   h\n"
            msg = colored(msg, 'red')

        # Handles an invalid request and lists the correct usage for the user. 
        else:
            msg = "\nInvalid request, use \"h\" for usage help!\n"
            msg = colored(msg, 'red')

        # Send encoded acknowledgment to the connected client
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
