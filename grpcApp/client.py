import grpc, threading, time, sys
import chatapp_pb2 as app
import chatapp_pb2_grpc as rpc
from termcolor import colored

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

        # print("starting threads")
        self.replyThread.start()
        # messageThread.start()
        self.sendThread.start()
        # self.conn.createAccount(app.AccountName(name=self.username))
        # print("send thread started")

    def __listen_for_messages(self):
        """Thread that listens for messages from other clients"""
        # print("message thread started")
        for msg in self.conn.listenForMessages(app.AccountID(id=self.id)):
            str = colored(f"[{msg.senderName}] ", "grey")
            print(f"\n{str} {msg.message}"),
    
    def __listen_for_replies(self):
        """Thread that listens for server responses/feedback"""
        # print("reply thread started")
        for reply in self.conn.listenForReplies(app.Empty()):
            print(reply.message)

    def send_message(self):
        """Used to gather input from the user"""

        # Loop indefinitely until user quits
        while True:
            
            invalid_args_msg = colored("\nInvalid number of arguments!", "red")

            # Get input from user, then preprocess it
            # time.sleep(1)
            msg1 = colored(f"[{self.username}] ", "grey")
            msg2 = colored("Create an account or log in: \n", "grey", attrs=["bold"])
            msg_str = input(msg1 if self.loggedIn else msg2)
            msg_list = msg_str.split('|')
            msg_list = [elt.strip() for elt in msg_list]
            op_code = msg_list[0].strip()

            # Create an account.
            # Usage: c|<username>
            if op_code == 'c':
                if len(msg_list) != 2:
                    print(invalid_args_msg)
                    print(colored("Usage:   c|<username>\n", "red"))
                    continue
                msg = self.conn.createAccount(app.AccountName(name=msg_list[1]))
                self.username = msg.name
                self.id = msg.id
                print(colored(f"\nAccount created! User ID: {msg.id}\n", "green"))
            
            # Log into an account.
            # Usage: l|<uuid>
            elif op_code == 'l':
                if len(msg_list) != 2:
                    print(invalid_args_msg)
                    print(colored("Usage:   l|<uuid>\n", "red"))
                    continue

                # Check if user is valid and not logged in
                try:
                    id = int(msg_list[1])
                except:
                    print(colored("\nInvalid UUID!\n", "red"))
                    continue
                response = self.conn.logIn(app.AccountID(id=id))
                if response.success:
                    self.username = response.username
                    self.id = id
                    self.loggedIn = True
                    self.messageThread.start()    # Listen for new messages
                print(response.message)

            # List all users and their names. 
            # Usage: u
            elif op_code == 'u':
                if len(msg_list) != 1:
                    print(invalid_args_msg)
                    print(colored("Usage:   u\n", "red"))
                    continue
                response = self.conn.listAccounts(app.Empty())
                print(response.message)

            # Send a message to a user. 
            # Usage: s|<recipient_uuid>|<message>
            elif op_code == 's':
                if len(msg_list) != 3:
                    print(invalid_args_msg)
                    print(colored("Usage:   s|<recipient_uuid>|<message>\n", "red"))
                    continue
                msg = app.Message()
                msg.senderID = self.id
                msg.senderName = self.username
                msg.message = msg_list[2]
                msg.recipientID = int(msg_list[1])
                response = self.conn.sendMessage(msg)
                print(response.message)

            # # Delete an account
            # # Usage: d|<uuid_to_delete>
            # elif op_code == 'd':
            #     msg = delete_account(msg_list[1])
        
            # # Filter accounts using a certain wildcard.
            # # Usage: f|<filter_wildcard>
            elif op_code == 'f':
                if len(msg_list) != 2:
                    print(invalid_args_msg)
                    print(colored("Usage:   f|<filter_wildcard>\n", "red"))
                    continue
                msg = app.FilterString(filter=msg_list[1])
                response = self.conn.filterAccounts(msg)
                print(response.message)
            
            # Log out from your account.
            # Usage: q
            elif op_code == 'q':
                if len(msg_list) != 1:
                    print(invalid_args_msg)
                    print(colored("Usage:   q\n", "red"))
                    continue
                msg = self.conn.logOut(app.AccountID(id=self.id))
                print(msg.message)
                sys.exit()

            # Usage help.
            # Usage: h
            elif op_code == 'h':
                msg = "\nUsage help below:\n"
                msg += "\nCreate an account.        c|<username>"
                msg += "\nLog into an account.      l|<uuid>"
                msg += "\nList users and names.     u"
                msg += "\nSend a message.           s|<recipient_uuid>|<message>"
                msg += "\nDelete an account.        d|<uuid_to_delete>\n"
                msg += "\nLog out of your account.  q"
                msg += "\nUsage help (this page).   h\n"
                msg = colored(msg, 'red')
                print(msg)  

            # Handles an invalid request and lists the correct usage for the user. 
            else:
                msg = "\nInvalid request, use \"h\" for usage help!\n"
                msg = colored(msg, 'red')
                print(msg)  
            

	


if __name__ == '__main__':
    c = Client()  # this starts a client and thus a thread which keeps connection to server open
