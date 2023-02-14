import socket
import sys
import select


def Main():
    # Set IP address and local port.
    ip = "127.0.0.1"
    port = 2048

    # Create a TCP socket connection.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Connect to the socket at the specified port and IP address. 
    server.connect((ip, port))

    # Main loop for clients to receive and send messages to the server.
    while True:
        # List of input streams. 
        sockets_list = [sys.stdin, server]
        
        # Initialize read sockets to process inputs from the server.
        read_sockets, _, _ = select.select(
            sockets_list, [], [])

        for socks in read_sockets:
            # Display messages received from the server. 
            if socks == server:
                message = socks.recv(4096)
                print(message.decode('UTF-8'))
            
            # Read and send messages from the client. 
            else:
                message = sys.stdin.readline().strip()
                server.send(message.encode('UTF-8'))
                data = server.recv(4096)
                print(str(data.decode('UTF-8')))
if __name__ == '__main__':
    Main()
