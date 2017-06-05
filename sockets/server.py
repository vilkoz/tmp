#!/usr/bin/env python2.7
from __future__ import print_function

import socket
import threading
import my_rsa
import my_sign
import json
import base64
import time

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

def proc_sockets(socket_list):
    for client in socket_list:
        string = "processing: \n" + repr(client[0]) + " \n" + repr(client[1])
        print (string)
        # received_data = my_rsa.unpack(my_receive(client[0]))
        received_data = my_receive(client[0]).decode()
        try:
            json_msg = json.loads(received_data)
            signature = json_msg['sign'].encode()
            data_id_json = json_msg['data_id'].encode()
        except Exception as e:
            print("exception: ", (e.message))
            print("wrong message format! from" + repr(client[1]))
            client[0].close()
            socket_list.remove(client)
            return
        if not (my_sign.verify_sign(signature, data_id_json, "../numbers.txt")):
            print("wrong signature from" + repr(client[1]))
            client[0].close()
            socket_list.remove(client)
            return
        if (VERBOSE):
            print("received data: \n")
            my_rsa.print_hex(received_data)
        try:
            data_id = json.loads(data_id_json)
            exp_time = int(data_id['exp_time'])
            if (int(time.time()) > exp_time):
                print("expired message from" + repr(client[1]))
                client[0].close()
                socket_list.remove(client)
                return
            b64_data = bytes(base64.b64decode(data_id['data']))
            data = my_rsa.unpack(b64_data)
        except Exception as e:
            print("exception: ", (e.message))
            print("wrong data_id format from" + repr(client[1]))
            client[0].close()
            socket_list.remove(client)
            return
        # TODO: get numbers_path by user id
        decoded_data = my_rsa.decode(data, "../numbers.txt")
        print("received and decoded data:", decoded_data)
        # my_send(client[0], string + "received: " + received_data)
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
