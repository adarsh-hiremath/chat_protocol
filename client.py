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

    # connect to server on local computer
    server.connect((ip, port))

    # message you send to server
    # message = "V for vendetta"
    while True:
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(
            sockets_list, [], [])

        for socks in read_sockets:

            # if we're getting a message
            if socks == server:
                message = socks.recv(2048)
                print(message.decode('UTF-8'))
            else:

                message = sys.stdin.readline().strip()
                server.send(message.encode('UTF-8'))
                data = server.recv(2048)
                print(str(data.decode('UTF-8')))


if __name__ == '__main__':
    Main()
