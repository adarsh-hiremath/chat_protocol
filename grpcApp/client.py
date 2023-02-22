import grpc
import threading
import time
import sys
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc
from termcolor import colored

ip = "10.250.129.194"
port = 50051


class Client:
    def __init__(self):

        # Set initial client variables
        self.username = None
        self.loggedIn = False
        channel = grpc.insecure_channel(ip + ':' + str(port))
        self.conn = rpc.ChatAppStub(channel)

        # Initialize and start a thread to communicate with server.
        self.sendThread = threading.Thread(target=self.send_message)
        self.sendThread.start()

        # Initialize a thread for messages, but wait until login to start.
        self.messageThread = threading.Thread(
            target=self.__listen_for_messages)

    def __listen_for_messages(self):
        """Thread that listens for messages from other clients."""

        for msg in self.conn.listenForMessages(app.Account(username=self.username)):
            str = colored(f"[{msg.senderName}] ", "grey")
            print(f"{str} {msg.message}\n")

    def send_message(self):
        """Gather input and communicate with the client."""

        # Welcome message.
        msg = "\nWelcome to the chat application! Begin by logging in or creating an account. Below, you will find a list of supported commands :\n"
        msg += "\nCreate an account.        c|<username>"
        msg += "\nLog into an account.      l|<username>"
        msg += "\nSend a message.           s|<recipient_username>|<message>"
        msg += "\nFilter accounts.          f|<filter_regex>"
        msg += "\nDelete your account.      d|<confirm_username>"
        msg += "\nList users and names.     u"
        msg += "\nUsage help (this page).   h\n"
        msg = colored(msg, 'yellow')
        print(msg)

        # Loop indefinitely until client quits.
        while True:

            # General message for invalid argument count.
            invalid_args_msg = colored("\nInvalid number of arguments!", "red")

            # Get input from user, then preprocess it.
            msg_str = input("")
            msg_list = msg_str.split('|')
            msg_list = [elt.strip() for elt in msg_list]
            op_code = msg_list[0].strip()

            # Create an account.
            # Usage: c|<username>
            if op_code == 'c':
                if len(msg_list) != 2:
                    print(colored("\nInvalid arguments! Usage: c|<username>\n", "red"))
                    continue

                # Check if user is already logged in.
                if self.loggedIn:
                    print(colored("\nPlease disconnect first!\n", "red"))
                    continue

                msg = self.conn.createAccount(
                    app.Account(username=msg_list[1]))
                print(msg.message)

            # Log into an account.
            # Usage: l|<username>
            elif op_code == 'l':
                if len(msg_list) != 2:
                    print(colored("\nInvalid arguments! Usage: l|<username>\n", "red"))
                    continue

                # Check if user is already logged in
                if self.loggedIn:
                    print(colored("\nPlease log out first!\n", "red"))
                    continue

                # Begin listening for messages (& dequeue all queued messages).
                response = self.conn.logIn(app.Account(username=msg_list[1]))
                if response.success:
                    self.username = response.username
                    self.loggedIn = True
                    self.messageThread.start()
                print(response.message)

            # Send a message to a user.
            # Usage: s|<recipient_username>|<message>
            elif op_code == 's':
                if len(msg_list) != 3:
                    print(colored("\nInvalid arguments! Usage: s|<recipient_username>|<message>\n", "red"))
                    continue

                # Initialize and send the message.
                if not self.loggedIn:
                    print(colored("\nPlease log in to send a message!\n", "red"))
                    continue

                msg = app.Message()
                msg.senderName = self.username
                msg.recipientName = msg_list[1]
                msg.message = msg_list[2]
                response = self.conn.sendMessage(msg)
                if response.message:
                    print(response.message)

            # Filter accounts using a regex.
            # Usage: f|<filter_regex>
            elif op_code == 'f':
                if len(msg_list) != 2:
                    print(invalid_args_msg)
                    print(colored("Usage:   f|<filter_regex>\n", "red"))
                    continue
                msg = app.FilterString(filter=msg_list[1])
                response = self.conn.filterAccounts(msg)
                print(response.message)

            # Delete the current client's account.
            # Usage: d|<confirm_username>
            elif op_code == 'd':
                if len(msg_list) != 2:
                    print(
                        colored("\nInvalid arguments! Usage: d|<confirm_username>\n", "red"))
                    continue

                # Ensure user is logged in and uses correct confirmation.
                if not self.loggedIn:
                    print(colored("\nPlease log in first!\n", "red"))
                    continue
                if self.username != msg_list[1]:
                    print(colored("\nIncorrect username for confirmation.\n", "red"))
                    continue

                msg = self.conn.deleteAccount(
                    app.Account(username=self.username))

                print(msg.message)

                # Exit the process so that a user must reconnect.
                sys.exit(0)

            # List all users and their status.
            # Usage: u
            elif op_code == 'u':
                if len(msg_list) != 1:
                    print(invalid_args_msg)
                    print(colored("Usage: u\n", "red"))
                    continue
                response = self.conn.listAccounts(app.Empty())
                print(response.message)

            # Usage help.
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
                msg = colored(msg, 'red')
                print(msg)

            # Handles an invalid request and lists the correct usage for the user.
            else:
                msg = "\nInvalid request, use \"h\" for usage help!\n"
                msg = colored(msg, 'red')
                print(msg)


# Start a Client process to handle user actions.
if __name__ == '__main__':
    c = Client()
