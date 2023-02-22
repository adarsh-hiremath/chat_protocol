from concurrent import futures
import logging
import grpc
import time
import random
import re
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc
from termcolor import colored

ip = "10.250.129.194"
port = 50051


# inheriting here from the protobuf rpc file which is generated
class ChatApp(rpc.ChatAppServicer):

    def __init__(self):

        # A dictionary with key: username, value: user's pending messages queue.
        self.messages = {}

        # A list with all of account usernames.
        self.accounts = []

        # A list with usernames of accounts that are currently logged in.
        self.live_users = []

    def createAccount(self, request, context):
        """Create an account. (c|<username>)"""

        print(f"user {request.username} requesting account creation")

        # Check if the username is already in use.
        if request.username in self.accounts:
            msg = colored(
                f"\nAccount {request.username} already exists!\n", "red")
            print(f"\nUser {request.username} account creation rejected\n")
            return app.ServerReply(message=msg)

        # Check that the username is a valid alphanumeric.
        if not re.fullmatch("\w{2,20}", request.username):
            msg = colored(
                f"\nUsername must be alphanumeric and 2-20 characters!\n", "red")
            print(f"\nUser {request.username} account creation rejected\n")
            return app.ServerReply(message=msg)

        # Register the user.
        self.accounts.append(request.username)
        msg = colored(f"\nNew account created! User ID: {request.username}. Please log in.\n", "green")
        print(f"\nUser {request.username} account created\n")

        return app.ServerReply(message=msg)

    def logIn(self, request: app.Account, context):
        """Log in as a specific user. (l|<username>)"""

        print(f"login as user {request.username} requested")

        # Check if the user is already logged in.
        if request.username in self.live_users:
            msg = f"\nUser {request.username} already logged in. Please try again.\n"
            msg = colored(msg, "red")
            print(f"\nLogin as user {request.username} denied\n")
            return app.LoginReply(success=False, message=msg)

        # Check if the user has created an account.
        elif request.username not in self.accounts:
            msg = f"\nUser {request.username} is not a valid user, please try again.\n"
            msg = colored(msg, "red")
            print(f"login as user {request.username} denied")
            return app.LoginReply(success=False, message=msg)

        # Log in as the given user.
        else:
            self.live_users.append(request.username)
            msg = f"\nLogin successful - welcome back {request.username}!\n"
            msg = colored(msg, "green")
            print(f"\nLogin as user {request.username} completed.\n")
            return app.LoginReply(success=True, message=msg, username=request.username)

    def listAccounts(self, request, context):
        """List all of the registered users. (u)"""

        print(f"\nListing accounts\n")

        # Output a list of users, and whether they are currently online.
        if len(list(self.accounts)) > 0:
            acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") +
                                         (colored("(live)", "green") if u in self.live_users else ""))
                                        for u in self.accounts]) + "\n"

        # No registered users on the server.
        else:
            acc_str = colored("\nNo existing users!\n", "red")

        return app.ServerReply(message=acc_str)

    def filterAccounts(self, request, context):
        """Filter accounts using a regex. (f|<filter_regex>)"""

        print(f"\nFiltering accounts.\n")

        # Find a list of matching accounts.
        fltr = request.filter
        def fun(x): return re.fullmatch(fltr, x)
        filtered_accounts = list(filter(fun, self.accounts))

        # Output a list of users, and whether they are currently online.
        if len(list(filtered_accounts)) > 0:
            acc_str = "\n" + "\n".join([(colored(f"{u} ", "blue") +
                                         (colored("(live)", "green") if u in self.live_users else ""))
                                        for u in filtered_accounts]) + "\n"

        # No matching accounts on the server.
        else:
            acc_str = colored("\nNo matching users!\n", "red")

        return app.ServerReply(message=acc_str)

    def sendMessage(self, request: app.Message, context):
        """Send a message to a specified other user. (s|<username>|<message>)"""

        print(
            f"user {request.senderName} requesting message to user {request.recipientName}")

        # Check if the recipient is a registered user and send message.
        if request.recipientName in self.accounts:
            if self.messages.get(request.recipientName):
                self.messages[request.recipientName].append(request)
            else:
                self.messages[request.recipientName] = [request]
            msg = colored("\nMessage sent!\n", "green")
            print(f"user {request.senderName} message to user {request.recipientName} sent")

        # Recipient is not a registered user.
        else:
            msg = colored(
                "\nMessage failed to send! Verify recipient username.\n", "red")
            print(
                f"user {request.senderName} message to user {request.recipientName} denied")

        return app.ServerReply(message=msg)

    def deleteAccount(self, request: app.Account, context):
        """Delete the current user's account. (d|<confirm_username>)"""

        print(f"\nUser {request.username} requesting account deletion.\n")

        # User can be deleted. Remove from associated data structures.
        if request.username in self.accounts:
            self.accounts.remove(request.username)
            if self.messages.get(request.username):
                self.messages.pop(request.username)
            msg = colored(
                f"\nAccount {request.username} successfully deleted!\n", "green")
            print(f"\nUser {request.username} account deleted.\n")

        # User has already been deleted.
        else:
            msg = colored(f"\nYour account has already been deleted.\n", "red")
            print(f"\nUser {request.username} account already deleted.\n")

        return app.ServerReply(message=msg)

    def listenForMessages(self, request_iterator, context):
        """Stream run in a thread by client, listens for messages."""

        print(f"user {request_iterator.username} listening stream opened")

        # Polls while user is still online.
        while context.is_active():

            # Stream messages to the client one at a time.
            if self.messages.get(request_iterator.username):
                msg = self.messages[request_iterator.username].pop(0)
                yield msg

        # Disconnect the client.
        self.live_users.remove(request_iterator.username)

        print(f"user {request_iterator.username} disconnected")


# Run the server upon file execution.
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=25))
    rpc.add_ChatAppServicer_to_server(ChatApp(), server)
    server.add_insecure_port(ip + ':' + str(port))
    server.start()
    print(f"Server started, listening on port {port}.\n")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
