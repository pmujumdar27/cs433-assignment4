import socket
import sys
import time
import os

PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFERSIZE = 1024
LIBPATH = './serverlib/'
HEADERSIZE = 64
DC_MSG = '-BYE'
FLAGSIZE = 1

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def get_msg(conn):
    msg_len = conn.recv(HEADERSIZE).decode(FORMAT)
    msg = ''
    if msg_len:
        msg_len = int(msg_len)
        rcv_len = 0
        while rcv_len < msg_len:
            curr_msg = conn.recv(min(BUFFERSIZE, msg_len-rcv_len)).decode(FORMAT)
            msg += curr_msg
            rcv_len += len(curr_msg)
    return msg

def sendfile(filename, conn):
    file = open(LIBPATH + filename, "rb")
    file_contents = file.read()

    file.close()

    filesize = len(file_contents)
    print(f"Size of requested file is: {filesize}")
    send_filesize = str(filesize).encode(FORMAT)
    send_filesize += b' '*(HEADERSIZE - len(send_filesize))

    conn.send(send_filesize)

    len_sent = 0

    print("Sending file...")

    while len_sent < filesize:
        curr_msg = file_contents[len_sent : min(filesize, len_sent+BUFFERSIZE)]
        conn.send(curr_msg)
        len_sent += len(curr_msg)

    print(f"File {filename} sent successfully!")
    return "Success!", 1

def handle_connection(conn, addr):
    print(f"\n[+] Client Connected: {addr}")

    while True:
        msg = ''
        while True:
            msg = get_msg(conn)
            if len(msg)!=0:
                break
        if msg==DC_MSG:
            break
        filename = msg
        sendfile(filename, conn)

def run_server():
    print("Initializing server...")
    server.listen()
    while True:
        print(f"\n\nServer is ready and is listening on {ADDR} ")
        conn, addr = server.accept()
        rc = os.fork()
        if rc==0:
            handle_connection(conn, addr)
        print(f"Client {addr} disconnected!")

run_server()