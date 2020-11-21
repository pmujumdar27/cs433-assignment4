import socket
import sys
import time

PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFERSIZE = 1024
LIBPATH = './serverlib/'
HEADERSIZE = 64
DC_MSG = '-BYE'
FLAGSIZE = 1
ENDFLAG = '\r\ngoodbye\r\n'
FLAGITER = 1

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def sendfile(filename, conn, addr):
    try:
        file = open(LIBPATH + filename, "rb")
        file_contents = file.read()
        flag = str(1).encode(FORMAT)+b' '*(FLAGSIZE-len(str(1)))
        conn.sendto(flag, addr)

        file.close()

        filesize = len(file_contents)
        print(f"Size of requested file is: {filesize}")
        send_filesize = str(filesize).encode(FORMAT)
        send_filesize += b' '*(HEADERSIZE - len(send_filesize))

        conn.sendto(send_filesize, addr)

        len_sent = 0

        print("Sending file...")

        while len_sent < filesize:
            curr_msg = file_contents[len_sent : min(filesize, len_sent+BUFFERSIZE)]
            curr_msg += b' '*(BUFFERSIZE-len(curr_msg))
            conn.sendto(curr_msg, addr)
            # time.sleep(1e-4) #uncomment to add 100microsecond sleep
            len_sent += len(curr_msg)

        for _ in range (FLAGITER):
            endflag = ENDFLAG.encode(FORMAT)+b' '*(BUFFERSIZE-len(ENDFLAG))
            conn.sendto(endflag, addr)

        return "Success!", 1
    except:
        flag = str(0).encode(FORMAT)+b' '*(FLAGSIZE-len(str(0)))
        conn.sendto(flag, addr)
        return str(sys.exc_info()), -1

def handle_connection(conn):

    while True:
        msg_len, addr = conn.recvfrom(HEADERSIZE)
        msg_len = msg_len.decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = ''
            rcv_len = 0
            while rcv_len < msg_len:
                curr_msg, addr = conn.recvfrom(min(BUFFERSIZE, msg_len-rcv_len))
                curr_msg = curr_msg.decode(FORMAT)
                msg += curr_msg
                rcv_len += len(curr_msg)
            
            else:
                print(f"Requested file name: {msg}, length of filename is: {msg_len}")
                ret, val = sendfile(msg, conn, addr)
                print(f"Sendfile exited with value: {val}\n{ret}\n")


    conn.close()


def start_server(server):
    print("Initializing server...")
    print(f"Server is ready and is listening on {ADDR}\n")
    while True:
        handle_connection(server)

start_server(server)