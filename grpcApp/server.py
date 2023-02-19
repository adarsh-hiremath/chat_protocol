from concurrent import futures
import logging, grpc, time, random, re
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc
from termcolor import colored

ip = "127.0.0.1"
port = 50051

class ChatApp(rpc.ChatAppServicer):  # inheriting here from the protobuf rpc file which is generated

    def __init__(self):

        # A list with all the server reply history
        self.serverReplies = []

        # A dictionary with usernames as keys and pending messages queues as values. 
        self.messages = {}

        # A list with all of the account usernames 
        self.accounts = []

        # A list to store the users that are currently logged in.
        self.live_users = []

    def createAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""

        # check if the account already exists
        if request.username in self.accounts:
            msg = colored(f"\nAccount {request.username} already exists!\n", "red")
            return app.ServerReply(message=msg)

        # check for a valid username
        if not re.fullmatch("\w{2,20}", request.username):
            msg = colored(f"\nUsername must be alphanumeric and 2-20 characters!\n", "red")
            return app.ServerReply(message=msg)

        # successful registration
        self.accounts.append(request.username)
        msg = colored(f"\nWelcome, {request.username}! Please log in. \n", "green")
        return app.ServerReply(message=msg)

    def logIn(self, request: app.Account, context):
        """Missing associated documentation comment in .proto file."""
        if request.username in self.live_users:
            msg = f"\nUser {request.username} already logged in, please try again.\n"
            msg = colored(msg, "red")
            return app.LoginReply(success=False, message=msg)
        elif request.username not in self.accounts:
            msg = f"\nUser {request.username} is not a valid user, please try again.\n"
            msg = colored(msg, "red")
            return app.LoginReply(success=False, message=msg)
        else: 
            self.live_users.append(request.username)
            msg = f"\nLogin successful - welcome back {request.username}!\n"
            msg = colored(msg, "green")
            return app.LoginReply(success=True, message=msg, username=request.username)

    def listAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        if len(list(self.accounts)) > 0:
            str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                        (colored("(live)", "green") if u in self.live_users else ""))
                        for u in self.accounts]) + "\n"
        else:
            str = colored("\nNo existing accounts!\n", "red")
        return app.ServerReply(message=str)

    def filterAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        fltr = request.filter
        fun = lambda x: re.fullmatch(fltr, x)
        filteredAccounts = list(filter(fun, self.accounts))
        if len(list(filteredAccounts)) > 0:
            str = "\n" + "\n".join([(colored(f"{u} ", "blue") + 
                        (colored("(live)", "green") if u in self.live_users else ""))
                        for u in filteredAccounts]) + "\n"
        else:
            str = colored("\nNo accounts found!\n", "red")

        return app.ServerReply(message=str)

    # def logOut(self, request, context):
    #     """Missing associated documentation comment in .proto file."""
    #     if request.username in self.live_users: 
    #         self.live_users.remove(request.username)
    #         msg = colored(f"\nUser {request.username} logged out!\n", "green")
    #     else:
    #         msg = colored(f"\nUser {request.username} not found? Contact the\n", "red")
    #     return app.ServerReply(message=msg)

    def sendMessage(self, request: app.Message, context):
        """Missing associated documentation comment in .proto file."""
        # this is only for the server console
        print(f"[{request.senderName}] {request.message}")
        # Add it to the chat history
        if request.recipientName in self.accounts:
            if self.messages.get(request.recipientName):
                self.messages[request.recipientName].append(request)
            else:
                self.messages[request.recipientName] = [request]
            msg = colored("\nMessage sent!\n", "green")
        else:
            msg = colored("\nMessage failed to send! Verify recipient username.\n", "red")
        
        return app.ServerReply(message=msg)
    
    def deleteAccount(self, request: app.Account, context):
        """Delete a specified account by username."""
        # this is only for the server console
        # print(f"[{request.senderName}] {request.message}")
        # Add it to the chat history
        response = app.ServerReply()
        if request.username in self.accounts:
            self.accounts.remove(request.username)
            if self.messages.get(request.username): 
                self.messages.pop(request.username)
            response.message = colored(f"\nAccount {request.username} successfully deleted!\n", "green")
        else:
            response.message = colored(f"\nYour account has already been deleted.\n", "red")

        return response

    def listenForMessages(self, request_iterator, context):
        """This is a stream that continuously sends chats."""
        # each client thread creates
        while context.is_active():
            # check if there are messages to be displayed
            if self.messages.get(request_iterator.username):
                msg = self.messages[request_iterator.username].pop(0)
                yield msg
        
        self.live_users.remove(request_iterator.username)
        print(f"User {request_iterator.username} disconnected!\n")

    def listenForReplies(self, request_iterator, context):
        """This is a stream that continuously sends chats."""
        # each client thread creates
        while context.is_active():
            # check if there are messages to be displayed
            if len(self.serverReplies) > 0:
                msg = self.serverReplies.pop(0)
                yield msg

        self.serverReplies = []



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=25))
    rpc.add_ChatAppServicer_to_server(ChatApp(), server)
    server.add_insecure_port(ip + ':' + str(port))
    server.start()
    print(f"Server started, listening on port {port}.")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()