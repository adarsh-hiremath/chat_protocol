import grpc, threading
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc

ip = "127.0.0.1"
port = 50051

class Client:

    def __init__(self):
        self.username = None
        self.id = -1
        self.loggedIn = False
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(ip + ':' + str(port))
        self.conn = rpc.ChatAppStub(channel)
        # create new listening thread for when new message streams come in
        self.replyThread = threading.Thread(target=self.__listen_for_replies)
        self.messageThread = threading.Thread(target=self.__listen_for_messages)
        self.sendThread = threading.Thread(target=self.send_message)
        # messageThread = threading.Thread(target=self.__listen_for_messages)
        # sendThread = threading.Thread(target=self.send_message)

        print("starting threads")
        self.replyThread.start()
        # messageThread.start()
        self.sendThread.start()
        # self.conn.createAccount(app.AccountName(name=self.username))
        # print("send thread started")

    def __listen_for_messages(self):
        """Thread that listens for messages from other clients"""
        print("message thread started")
        for msg in self.conn.listenForMessages(app.AccountID(id=self.id)):  # this line will wait for new messages from the server!
            print(f"[{msg.senderName}] {msg.message}")  # debugging statement
    
    def __listen_for_replies(self):
        """Thread that listens for replies from the server -- not messages from other clients"""
        print("reply thread started")
        for reply in self.conn.listenForReplies(app.Empty()):  # this line will wait for new messages from the server!
            print(reply.message)  # debugging statement

    def send_message(self):
        """
        This method is called when user enters something into the textbox
        """
        print("send thread started")
        while True:
            msg_str = input("Enter a request:\n")
            msg_list = msg_str.split('|')
            msg_list = [elt.strip() for elt in msg_list]
            op_code = msg_list[0].strip()

            # Create an account.
            # Usage: c|username
            if op_code == 'c':
                if len(msg_list) != 2:
                    print("Invalid number of arguments!")
                    continue
                msg = self.conn.createAccount(app.AccountName(name=msg_list[1]))
                self.username = msg.name
                self.id = msg.id
                print(f"Account created! User ID: {msg.id}")
            
            # Log into an account.
            # Usage: l|<uuid>
            elif op_code == 'l':
                if len(msg_list) != 2:
                    print("Invalid number of arguments!")
                    continue
                id = int(msg_list[1])
                response = self.conn.logIn(app.AccountID(id=id))
                if response.success:
                    self.username = response.username
                    self.id = id
                    self.loggedIn = True
                    self.messageThread.start()
                print(response.message)

            # List all users and their names. 
            # Usage: u
            # elif op_code == 'u':
            #     msg = list_accounts()

            # Send a message to a user. 
            # Usage: s|<recipient_uuid>|<message>
            elif op_code == 's':
                if len(msg_list) != 3:
                    print("Invalid number of arguments!")
                    continue
                msg = app.Message()  # create protobug message (called Note)
                msg.senderID = self.id  # set the username
                msg.senderName = self.username
                msg.message = msg_list[2]  # set the actual message of the note
                msg.recipientID = int(msg_list[1])
                response = self.conn.sendMessage(msg)  # send the Note to the server
                print(response.message)

            # # Delete an account
            # # Usage: d|<uuid_to_delete>
            # elif op_code == 'd':
            #     msg = delete_account(msg_list[1])
        
            # # Filter accounts using a certain wildcard.
            # # Usage: f|<filter_wildcard>
            # elif op_code == 'f':
            #     msg = filter_accounts(msg_list[1])
            
            # # Disconnect a user.
            # # Usage: q|<uuid_to_disconnect>
            # elif op_code == 'q':
            #     msg = disconnect_user(msg_list[1])
            #     connection.send(msg.encode('UTF-8')) 
            #     live_users[msg_list[1]].close()

            # Handles an invalid request and lists the correct usage for the user. 
            else:
                msg = "Invalid request, see below for usage help:"
                msg += "\nCreate an account, usage: c|<username>"
                msg += "\nLog into an account, usage: l|<uuid>"
                msg += "\nList users and their names, usage: u"
                msg += "\nSend a message, usage: s|<recipient_uuid>|<message>"
                msg += "\nDelete an account, usage: d|<uuid_to_delete>\n"
                print(msg)  
            

	


if __name__ == '__main__':
    c = Client()  # this starts a client and thus a thread which keeps connection to server open
