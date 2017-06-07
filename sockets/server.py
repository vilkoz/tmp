#!/usr/bin/env python2.7
from __future__ import print_function

import socket
import threading
import my_rsa
import my_sign
import json
import base64
import time

class DecodeError(Exception):
    pass
class SignatureError(Exception):
    pass

MSGLEN = 4096
HOST = ""
PORT = 50012

my_rsa.VERBOSE = False
VERBOSE = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def my_send(server, msg):
    totalsend = 0
    b_msg = msg.encode()
    b_msg += b'\x00'
    while totalsend < len(b_msg):
        sent = server.send(b_msg[totalsend:])
        if sent == '':
            raise RuntimeError("socket connection broken")
        totalsend += sent

def my_receive(server):
    chunks = []
    bytes_recv = 0
    while bytes_recv < MSGLEN:
        chunk = server.recv(2048)
        if (chunk == 0):
            # raise RuntimeError("socket connection broken")
            print("socket connection broken")
        chunks.append(chunk)
        bytes_recv += len(chunk)
        if VERBOSE:
            print ("my_recerive: received: ", chunks)
            print ("my_recerive: received size: ", bytes_recv)
        if len(chunk) != 0:
            if VERBOSE:
                print ("my_recerive: chunk [len(chunk - 1)] = ",
                        chunk[len(chunk) - 1])
        if (len(chunk) == 0 or chunk[len(chunk) - 1] == 0):
            break
    ret = b""
    for chunk in chunks:
        ret += chunk
    return ret[:-1]

def verify_client_sign(received_data, client):
    try:
        json_msg = json.loads(received_data)
        signature = json_msg['sign'].encode()
        data_id_json = json_msg['data_id'].encode()
        client_id = json.loads(data_id_json)['id']
    except Exception as e:
        print("exception: ", (e.message))
        print("[ERROR] wrong message format! from" + repr(client[1]))
        raise SignatureError
    # TODO: get numbers_path by user id
    if not (my_sign.verify_sign(signature, data_id_json, "../numbers.txt")):
        print("[ERROR] wrong signature from" + repr(client[1]))
        raise SignatureError
    return data_id_json

def decode_message(data_id_json, client):
    try:
        data_id = json.loads(data_id_json)
        exp_time = int(data_id['exp_time'])
    except Exception as e:
        print("[ERROR] exception: ", (e.message))
        print("[ERROR] wrong data_id format from" + repr(client[1]))
        raise DecodeError
    if (int(time.time()) > exp_time):
        print("[ERROR] expired message from" + repr(client[1]))
        raise DecodeError
    b64_data = bytes(base64.b64decode(data_id['data']))
    data = my_rsa.unpack(b64_data)
    return my_rsa.decode(data, "../numbers.txt")


def proc_client(client):
    string = "processing: " + repr(client[0]) + " " + repr(client[1])
    print (time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + string)
    received_data = my_receive(client[0]).decode()
    try:
        data_id_json = verify_client_sign(received_data, client)
    except SignatureError:
        return
    if (VERBOSE):
        print("received data: \n")
        my_rsa.print_hex(received_data)
    try:
        decoded_data = decode_message(data_id_json, client)
    except DecodeError:
        return
    print("received and decoded data:", decoded_data)

def proc_sockets(socket_list):
    for client in socket_list:
        proc_client(client)
        client[0].close()
        socket_list.remove(client)
        print("Number of clients: ", len(socket_list))

class ProcThread(threading.Thread):
    clients_list = []
    def __init_(self):
        threading.Thread.__init__(self)
    def run(self):
        print("Number of clients: ", len(self.clients_list))
        while True:
            if len(self.clients_list) > 0:
                proc_sockets(self.clients_list)
    def add_client(self, client):
        print("Number of clients: ", len(self.clients_list))
        self.clients_list.append(client)


pc = ProcThread()
pc.start()
while 1:
    (client_socket, addres) = s.accept()
    print("accepted connection from ", addres)
    pc.add_client((client_socket, addres))
