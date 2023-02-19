from concurrent import futures
import logging, grpc, time, random
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc

ip = "127.0.0.1"
port = 50051

class ChatApp(rpc.ChatAppServicer):  # inheriting here from the protobuf rpc file which is generated

    def __init__(self):

        # A list with all the chat history
        self.serverReplies = []

        # A dictionary with usernames as keys and pending messages queues as values. 
        self.messages = {}

        # A dictionary with UUIDs as keys and account names as values. 
        self.accounts = {}

        # A list to store the users that are currently logged in.
        self.live_users = []

    def createAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        uuid = random.randint(0, 1000)
        while uuid in self.accounts:
            uuid  = random.randint(0,1000)
        self.accounts[uuid] = request.name
        print(f"New account created! User ID: {uuid}")
        return app.Account(id=uuid, name=request.name)

    def logIn(self, request: app.AccountID, context):
        """Missing associated documentation comment in .proto file."""
        if request.id in self.live_users:
            msg = f"User {request.id} already logged in, please try again.\n"
            return app.LoginReply(success=False, message=msg)
        elif not self.accounts.get(request.id):
            msg = f"User {request.id} is not a valid user, please try again.\n"
            return app.LoginReply(success=False, message=msg)
        else: 
            self.live_users.append(request.id)
            msg = f"User {request.id} successfully logged in!\n"
            return app.LoginReply(success=True, message=msg, username=self.accounts[request.id])

    def listAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def filterAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def logOut(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sendMessage(self, request: app.Message, context):
        """Missing associated documentation comment in .proto file."""
        # this is only for the server console
        print(f"[{request.senderID}] {request.message}")
        # Add it to the chat history
        if self.accounts.get(request.recipientID):
            if self.messages.get(request.recipientID):
                self.messages[request.recipientID].append(request)
            else:
                self.messages[request.recipientID] = [request]
            return app.ServerReply(message="Message successfully sent!\n")  
        else:
            return app.ServerReply(message="Message failed to send!\n")

    def listenForMessages(self, request_iterator, context):
        """This is a stream that continuously sends chats."""
        lastMsgIdx = 0
        # each client thread creates
        while context.is_active():
            # check if there are messages to be displayed
            if self.messages.get(request_iterator.id):
                while len(self.messages[request_iterator.id]) > lastMsgIdx:
                    msg = self.messages[request_iterator.id][lastMsgIdx]
                    lastMsgIdx += 1
                    yield msg
        
        self.live_users.remove(request_iterator.id)
        print(f"User {request_iterator.id} disconnected!\n")

    def listenForReplies(self, request_iterator, context):
        """This is a stream that continuously sends chats."""
        lastIdx = 0
        # each client thread creates
        while True:
            # check if there are messages to be displayed
            while len(self.serverReplies) > lastIdx:
                msg = self.serverReplies[lastIdx]
                lastIdx += 1
                yield msg



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatAppServicer_to_server(ChatApp(), server)
    server.add_insecure_port(ip + ':' + str(port))
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()