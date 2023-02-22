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
conn_refs = {}

# A dictionary with logged in users.
logged_in = []


def create_account(msg_list, connection):
    """Create an account, and associate with the appropriate socket. (c|<username>)"""

    if len(msg_list) != 2:
        msg = (colored("\nInvalid arguments! Usage: c|<username>\n", "red"))
        return msg

    update_live_users()
    init_user = get_account(connection)

    if init_user in logged_in:
        msg = (colored("\nPlease disconnect first!\n", "red"))
        return msg

    username = msg_list[1]

    if username in accounts:
        print(f"\nUser {username} account creation rejected\n")
        msg = colored(f"\nAccount {username} already exists!\n", "red")
        return msg

    if not re.fullmatch("\w{2,20}", username):
        print(f"\nUser {username} account creation rejected\n")
        msg = colored(
            f"\nUsername must be alphanumeric and 2-20 characters!\n", "red")
        return msg

    accounts.append(username)
    print(f"\nUser {username} account created\n")
    msg = colored(
        f"\nNew account created! User ID: {username}. Please log in.\n", "green")
    return msg


def delete_account(msg_list, connection):
    """Delete the current user's account. (d|<confirm_username>)"""

    if len(msg_list) != 2:
        msg = (colored("\nInvalid arguments! Usage: d|<confirm_username>\n", "red"))
        return msg

    username = msg_list[1]
    init_user = get_account(connection)

    if (init_user != username):
        msg = (colored("\nYou can only delete your own account.\n", "red"))
        return msg

    print(f"\nUser {username} requesting account deletion.\n")

    if username in accounts:
        accounts.remove(username)
        logged_in.remove(username)
        if pending_messages.get(username):
            pending_messages.pop(username)
        print(f"\nUser {username} account deleted.\n")
        msg = colored(f"\nAccount {username} has been deleted.\n", "green")
        return msg

    else:
        return (colored("\nIncorrect username for confirmation.\n", "red"))


def update_live_users():
    """Check which socket connections are still live."""

    curr_users = []
    for user in conn_refs:
        try:
            conn_refs[user].send("".encode('UTF-8'))
            curr_users.append(user)
        except:
            pass

    for user in logged_in:
        if user not in curr_users:
            logged_in.remove(user)


def list_accounts():
    """List all of the registered users and display their status. (u)"""

    print(f'\nListing accounts\n')

    update_live_users()

    if accounts:
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") +
                                     (colored("(live)", "green") if u in logged_in else ""))
                                    for u in accounts]) + "\n"

    else:
        acc_str = colored("\nNo existing users!\n", "red")

    return acc_str


def verify_dupes(connection):
    """Verify if a user is already logged in when they try to log in."""

    for username in logged_in:
        if conn_refs[username] == connection:
            return True
    return False


def login(msg_list, connection):
    """Check that the user is not already logged in, log in to a particular user, and deliver unreceived messages if applicable."""

    if len(msg_list) != 2:
        msg = (colored("\nInvalid arguments! Usage: l|<username>\n", "red"))
        return msg

    check_duplicate = verify_dupes(connection)

    if check_duplicate == True:
        msg = (colored("\nPlease log out first!\n", "red"))
        return msg

    username = msg_list[1]

    print(f"\nLogin as user {username} requested\n")

    update_live_users()

    if username in logged_in:
        print(f"\nLogin as {username} denied.\n")
        msg = colored(
            f"\nUser {username} already logged in. Please try again.\n", "red")
        return msg

    elif username not in accounts:
        print(f"\nLogin as {username} denied.\n")
        msg = colored(
            f"\nUser {username} does not exist. Please create an account.\n", "red")
        return msg

    else:
        conn_refs[username] = connection
        print(f"\nLogin as user {username} completed.\n")
        msg = colored(
            f"\nLogin successful - welcome back {username}!\n", "green")
        if username in pending_messages:
            print(f"\nDelivering pending messages to {username}.\n")
            send_msg(connection, username, colored(
                f"\nYou have pending messages! Delivering the  messages now...", "green"))
            deliver_pending_messages(username)
        logged_in.append(username)
        return msg


def get_account(connection):
    """Get account from connection refernce by reverse searching the live_users dictionary."""

    for username in conn_refs:
        if conn_refs[username] == connection:
            return username
    return None


def deliver_pending_messages(recipient_name):
    """Deliver pending messages to a user."""

    while pending_messages[recipient_name]:
        conn_refs[recipient_name].send(
            pending_messages[recipient_name][0].encode('UTF-8'))
        pending_messages[recipient_name].pop(0)


def send_msg(connection, recipient_name, msg):
    """Send a message to the given user."""

    print(f"\nRequest received to send message to {recipient_name}.\n")

    update_live_users()
    init_user = get_account(connection)

    if init_user not in logged_in:
        msg = (colored("\nPlease log in to send a message!\n", "red"))
        return msg

    if recipient_name in accounts:
        sender_name = get_account(connection)
        if recipient_name in logged_in:
            msg = colored(f"\n[{sender_name}] ", "grey") + msg + "\n"
            conn_refs[recipient_name].send(msg.encode('UTF-8'))
            print(f"\nMessage sent to {recipient_name}.\n")
            msg = colored(f"\nMessage sent to {recipient_name}.\n", "green")
        else:
            msg = colored(f"\n[{sender_name}] ", "grey") + msg
            if recipient_name in pending_messages:
                pending_messages[recipient_name].append(msg)
            else:
                pending_messages[recipient_name] = [msg]
            print(
                f"\nMessage will be sent to {recipient_name} after the account is online.\n")
            msg = colored(
                f"\nMessage will be delivered to {recipient_name} after the account is online.\n", "green")
        return msg

    else:
        msg = colored(
            "\nMessage failed to send! Verify recipient username.\n", "red")
        print(f"\nRequest to send message to {recipient_name} denied.\n")
        return msg


def filter_accounts(msg_list):
    """Filter accounts by a given regex."""

    print(f'\nFiltering accounts.\n')

    if len(msg_list) != 2:
        msg = (colored("\nInvalid arguments! Usage: f|<filter_regex>\n", "red"))
        return msg

    update_live_users()

    fltr = msg_list[1]
    def fun(x): return re.fullmatch(fltr, x)
    filtered_accounts = list(filter(fun, accounts))

    if len(list(filtered_accounts)) > 0:
        acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") +
                                     (colored("(live)", "green") if u in logged_in else ""))
                                    for u in filtered_accounts]) + "\n"

    else:
        acc_str = colored("\nNo matching users!\n", "red")

    return acc_str


def wire_protocol(connection):
    """Main server thread that continues running until the connection is closed."""

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
                msg = (colored(
                    "\nInvalid arguments! Usage: s|<recipient_username>|<message>\n", "red"))
            else:
                msg = send_msg(connection, msg_list[1], msg_list[2])

        # Delete an account
        # Usage: d|<confirm_username>
        elif op_code == 'd':
            msg = delete_account(msg_list, connection)

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

    print(f"Server started, listening on port {port}.\n")

    # Main loop for the server to listen to client requests.
    while True:
        connection, address = server.accept()
        print('\nConnected to:', address[0], ':', address[1])
        start_new_thread(wire_protocol, (connection,))


if __name__ == '__main__':
    Main()
