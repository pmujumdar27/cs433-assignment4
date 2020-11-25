import socket
import os
import sys
import time
import csv

PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFERSIZE = 1024
HEADERSIZE = 64
WELCOMEPATH = "./supportFiles/clientWelcome.txt"
DC_MSG = "-BYE"
LIBPATH = "./clientlib/"

aggThroughputDict = {}
aggTPFieldNames = ['one_conn_time', 'agg_throughput']
fileDownloadTimes = []
fieldNames = []
fileDownloadTimeDict = {}
fileThroughputs = []
fileThroughputDict = {}
SINGLEFILE = sys.argv[1] #uncomment for single file
# SINGLEFILE = 2

def get_conn_mode():
    mode = int(input())
    return mode

def get_file_requests():
    print("Enter the number of files you want")
    n = int(input())
    filenames = []
    print("Enter the filenames one by one")
    for _ in range(n):
        fname = input()
        filenames.append(fname)
    return filenames

def send_msg(msg, client):
    msg_len = len(msg)
    message = msg.encode(FORMAT)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' '*(HEADERSIZE-len(send_len))
    client.send(send_len)
    len_sent = 0
    while len_sent < msg_len:
        curr_msg = message[len_sent : min(len_sent+BUFFERSIZE, msg_len)]
        client.send(curr_msg)
        len_sent += len(curr_msg)

def getfile(conn, filename):
    send_msg(filename, conn)
    filesize = int(conn.recv(HEADERSIZE).decode(FORMAT))

    print(f"Size of requested file {filename} is: {filesize}")
    fname = "protocol_tcp_" + str(os.getpid()) + "_"+ filename 
    file = open(LIBPATH+fname, "wb")
    len_recv = 0
    print(f"Writing to {fname}")
    start_time = time.time()
    while len_recv < filesize:
        curr_msg = conn.recv(min(BUFFERSIZE, filesize-len_recv))
        file.write(curr_msg)
        len_recv += len(curr_msg)
    
    download_time = time.time()-start_time
    print(f"Time taken for download {download_time} seconds")
    print(f"Throughput: {filesize/(download_time*1e6)} MB/sec")
    fileThroughputDict[filename] = filesize/(download_time*1e6)
    print("Success!\n")
    file.close()
    return filesize, download_time


def get_files_persistent(filerequests):
    start_time = time.time()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    conn_time = time.time()-start_time
    aggThroughputDict["one_conn_time"] = conn_time
    totsize = 0
    for filename in filerequests:
        filesize, indiv_download_time = getfile(client, filename)
        totsize += filesize
        fileDownloadTimeDict[filename] = indiv_download_time
        fieldNames.append(filename)
    send_msg(DC_MSG, client)
    total_time = time.time()-start_time
    tot_throughput = totsize/(total_time*1e6)
    fileDownloadTimes.append(fileDownloadTimeDict)
    fileThroughputs.append(fileThroughputDict)
    aggThroughputDict['agg_throughput'] = tot_throughput
    return tot_throughput

def get_files_non_persistent(filerequests):
    start_time = time.time()
    totsize = 0
    avg_conn_time = 0
    for filename in filerequests:
        conn_start = time.time()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        avg_conn_time += time.time()-conn_start
        filesize, indiv_download_time = getfile(client, filename)
        totsize += filesize
        fileDownloadTimeDict[filename] = indiv_download_time
        fieldNames.append(filename)
        send_msg(DC_MSG, client)
        client.close()
    total_time = time.time()-start_time
    fileDownloadTimes.append(fileDownloadTimeDict)
    fileThroughputs.append(fileThroughputDict)
    avg_conn_time/=len(filerequests)
    aggThroughputDict["one_conn_time"] = avg_conn_time
    tot_throughput = totsize/(total_time*1e6)
    aggThroughputDict["agg_throughput"] = tot_throughput
    return tot_throughput


def run_client():
    client_welcome = open(WELCOMEPATH, "r")
    welcome_text = client_welcome.read()
    print(welcome_text)

    mode = get_conn_mode()

    if SINGLEFILE == '1':
        mode = 2
        filerequests = [sys.argv[2]]
    else:
        mode = get_conn_mode()    
        filerequests = get_file_requests()

    throughput = 0

    if mode==1:
        throughput = get_files_non_persistent(filerequests)

    else:
        throughput = get_files_persistent(filerequests)

    if SINGLEFILE=="1":
        print(fileDownloadTimeDict)
        print(aggThroughputDict)
        print(fileThroughputDict)
        return
    else:
        indiv_time_log = f'tcp_fork_indiv_time_mode_{mode}.csv'
        indiv_throughput_log = f'tcp_fork_indiv_throughput_mode_{mode}.csv'
        agg_log = f'tcp_fork_agg_log_mode_{mode}.csv'

    print(fileDownloadTimeDict)
    print(aggThroughputDict)
    print(fileThroughputDict)

    writeHeaderAgain = False

    try:
        with open (indiv_time_log, "r") as csvfile:
            mycsv = csv.reader(csvfile)
            for row in mycsv:
                print(row[0])
                if(row[0]==""):
                    writeHeaderAgain = True
                    break
                break
    except:
        writeHeaderAgain = True


    with open (indiv_time_log, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        if writeHeaderAgain:
            writer.writeheader()
        writer.writerows(fileDownloadTimes)

    with open (indiv_throughput_log, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        if writeHeaderAgain:
            writer.writeheader()
        writer.writerows(fileThroughputs)

    with open (agg_log, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=aggTPFieldNames)
        if writeHeaderAgain:
            writer.writeheader()
        writer.writerows([aggThroughputDict])
    
    print(f"Cumulative throughput in mode {mode} was: {throughput}")

run_client()