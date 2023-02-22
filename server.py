import socket
import random
from _thread import *
import re
from termcolor import colored

# A dictionary with username as key and pending messages as values. 
pending_messages = {}

# A list of account names. 
accounts = []

# A dictionary with usernames as keys and connection references as values.
live_users = {}

# Create a new account with a given name and associate the account with the appropriate socket. 
def create_account(msg_list, connection): 
    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage: c|<username>\n", "red"))
        connection.send(msg.encode('UTF-8'))
        return 

    username = msg_list[1]

    if username in accounts: 
        print(f"\nUser {username} account creation rejected\n")
        msg = colored(f"\nAccount {username} already exists!\n", "red")
        return msg
    
    if not re.fullmatch("\w{2,20}", username):
        print(f"\nUser {username} account creation rejected\n")
        msg = colored(f"\nUsername must be alphanumeric and 2-20 characters!\n", "red")
        return msg
    
    accounts.append(username)
    print(f"\nUser {username} account created")
    msg = colored (f"\nNew account created! User ID: {username}. Please log in.\n", "green")
    return msg

# Delete the account from the list of accounts. 
def delete_account(msg_list): 
    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage: d|<confirm_account>\n", "red"))
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

# Check which socket connections are still live. 
def check_live_users():
    curr_users = []
    for user in live_users:
        try:
            live_users[user].send("".encode('UTF-8'))
            curr_users.append(user)
        except:
            pass
    return curr_users

# Displays all account names and their status (live or not). 
def list_accounts(): 
    print(f'\nListing accounts\n')

    curr_users = check_live_users()

    if accounts: 
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                    (colored("(live)", "green") if u in curr_users else ""))
                    for u in accounts]) + "\n"
    
    else: 
        acc_str = colored("\nNo existing users!\n", "red")

    return acc_str

# Check that the user is not already logged in, log in to a particular user, and deliver unreceived messages if applicable.
def login(msg_list, connection): 
    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage: l|<username>\n", "red"))
        return msg
    
    username = msg_list[1]

    print(f"\nLogin as user {username} requested\n")
    
    curr_users = check_live_users()

    if username in curr_users: 
        print(f"\nLogin as {username} denied.\n")
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
        if username in pending_messages:
            print(f"\nDelivering pending messages to {username}.\n")
            send_msg(connection, username, colored(f"\nYou have pending messages! Delivering the  messages now...", "green"))
            deliver_pending_messages(username)
        return msg

# Get account from connection refernce by reverse searching the live_users dictionary.
def get_account(connection):
    for username in live_users:
        if live_users[username] == connection:
            return username

# Deliver pending messages to a user.     
def deliver_pending_messages(recipient_name):
    while pending_messages.get(recipient_name):
        live_users[recipient_name].send(pending_messages[recipient_name][0].encode('UTF-8')) 
        pending_messages[recipient_name].pop(0)

# Send a message to the given user.
def send_msg(connection, recipient_name, msg):
    print(f"\nRequest received to send message to {recipient_name}.\n")

    curr_users = check_live_users()

    if recipient_name in accounts: 
        sender_name = get_account(connection)
        if recipient_name in curr_users:
            msg = colored(f"\n[{sender_name}] ", "grey") + msg + "\n"
            live_users[recipient_name].send(msg.encode('UTF-8'))
            print(f"\nMessage sent to {recipient_name}.\n")
            msg = colored(f"\nMessage sent to {recipient_name}.\n", "green")
        else:
            msg = colored(f"\n[{sender_name}] ", "grey") + msg
            if recipient_name in pending_messages:
                pending_messages[recipient_name] = pending_messages[recipient_name].append(msg)
            else: 
                pending_messages[recipient_name] = [msg]
            print(pending_messages)
            print(f"\nMessage will be sent to {recipient_name} after the account is online.\n")
            msg = colored(f"\nMessage will be delivered to {recipient_name} after the account is online.\n", "green")
        return msg

    else: 
        msg = colored("\nMessage failed to send! Verify recipient username.\n", "red")
        print(f"\nRequest to send message to {recipient_name} denied.\n")
        return msg

# Filter accounts by a given regex.
def filter_accounts(msg_list): 
    print(f'\nFiltering accounts.\n')

    if len(msg_list) != 2: 
        msg = (colored("\nInvalid arguments! Usage: f|<filter_regex>\n", "red"))
        return msg
    
    request = msg_list[1]

    fltr = request.filter
    fun = lambda x: re.fullmatch(fltr, x)
    filtered_accounts = list(filter(fun, accounts))

    curr_users = check_live_users()

    if len(list(filtered_accounts)) > 0:
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                (colored("(live)", "green") if u in curr_users else ""))
                for u in filtered_accounts]) + "\n"
        
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

        # List all users and their status. 
        # Usage: u
        elif op_code == 'u':
            msg = list_accounts()

        # Send a message to a user. 
        # Usage: s|<recipient_username>|<message>
        elif op_code == 's':
            if len(msg_list) != 3: 
                msg = (colored("\nInvalid arguments! Usage: s|<recipient_username>|<message>\n", "red"))
            else: 
                msg = send_msg(connection, msg_list[1], msg_list[2])

        # Delete an account
        # Usage: d|<confirm_username>
        elif op_code == 'd':
            msg = delete_account(msg_list)
    
        # Filter accounts using a certain wildcard.
        # Usage: f|<filter_regex>
        elif op_code == 'f':
            msg = filter_accounts(msg_list)
        
        # Print a list of all the commands.
        # Usage: h
        elif op_code == 'h':
            msg = "\nUsage help below:\n"
            msg += "\nCreate an account.        c|<username>"
            msg += "\nLog into an account.      l|<username>"
            msg += "\nSend a message.           s|<recipient_username>|<message>"
            msg += "\nFilter accounts.          f|<filter_regex>"
            msg += "\nDelete your account.      d|<confirm_username>"
            msg += "\nList users and names.     u"
            msg += "\nUsage help (this page).   h\n"
            msg = colored(msg, 'yellow')

        # Handles an invalid request and lists the correct usage for the user. 
        else:
            msg = "\nInvalid request, use \"h\" for usage help!\n"
            msg = colored(msg, 'red')

        # Send encoded acknowledgment to the connected client
        connection.send(msg.encode('UTF-8')) 

def Main():
    # Set IP address and local port.
    ip = "10.250.129.194"
    port = 50051
    
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
