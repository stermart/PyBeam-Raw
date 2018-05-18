#!/usr/bin/python

import pybeam
import socket
import sys

host = "10.16.188.11"
port = 5007

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('socket created', str(soc))

try:
    soc.bind((host, port))
    print('Socket bind complete', flush=True)
    soc.listen(5)
    print('Server started and listening', flush=True)
except socket.error as err:
    import sys
    print('Bind failed.. Error: {}'.format(str(err)), flush=True)
    sys.exit(1)

while True:
    conn, addr = soc.accept()
    ip, port = str(addr[0]), str(addr[1])
    try:
        print('Accepting connection from {}:{}'.format(ip, port), flush=True)
        while True:
            data = conn.recv(1024).decode()
            print('Data received: {}'.format(data), flush=True)
            if data == "PLAYBACK":
                conn.send('RECORD'.encode())
                print('Playing back!', flush=True)
                pybeam.playback_wav_dir("bform_out6PM")
                sys.exit(0)
    except:
        import traceback
        traceback.print_exc()


