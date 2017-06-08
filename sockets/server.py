#!/usr/bin/env python2.7
from __future__ import print_function

import socket
import threading
import my_rsa
import my_sign
import json
import base64
import time
import database

KEY_PATH = "../numbers.txt"

MSGLEN = 4096
my_rsa.VERBOSE = False
VERBOSE = False

class DecodeError(Exception):
    pass
class SignatureError(Exception):
    pass

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
        if (len(chunk) == 0 or chunk[-1] == '\x00'):
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
        data_json_arr = json.loads(data_id_json)
        client_id = data_json_arr['id']
        client_type = data_json_arr['type']
    except Exception as e:
        print("received_data: ", received_data)
        print("exception: ", (e.message))
        print("[ERROR] wrong message format! from" + repr(client[1]))
        raise SignatureError
    if not database.get_match_key(client_id, client_type):
        print("[ERROR] invalid id from" + repr(client[1]))
        raise SignatureError
    if not (my_sign.verify_sign(signature, data_id_json,
    "keys/" + client_id + ".pem")):
        print("[ERROR] wrong signature from" + repr(client[1]))
        raise SignatureError
    return (data_id_json, client_id, client_type)

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
    return my_rsa.decode(data, KEY_PATH)

def srv_msg_wrap(msg, client_id):
    encoded_int = (my_rsa.encode(msg, "keys/" + client_id + ".pem"));
    encoded_bytes = base64.b64encode(my_rsa.pack(encoded_int))

    json_data_id = json.dumps({
        "data": encoded_bytes,
        "exp_time" : int(time.time()) + 10
        })
    sign = my_sign.sign_data(json_data_id, KEY_PATH)
    json_send = json.dumps({
        "sign" : sign,
        "data_id" : json_data_id,
        })
    send_data = json_send
    return send_data

def verify_decode_raw(client, received_data):
    try:
        (data_id_json,
        client_id,
        client_type) = verify_client_sign(received_data, client)
    except SignatureError:
        raise SignatureError
    if (VERBOSE):
        print("received data: \n")
        my_rsa.print_hex(received_data)
    try:
        decoded_data = decode_message(data_id_json, client)
    except DecodeError:
        raise DecodeError
    return (decoded_data, client_id, client_type)

def send_message_to_car(msg, client_id, client_type):
    print("sending message to car")
    car_ip = database.get_match_key(client_id, client_type)
    s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_new.connect((car_ip, 50012))
    my_send(s_new, srv_msg_wrap(msg, car_ip))
    # my_receive(s_new)
    print("receiving message from car")
    (decoded_data,
    client_id,
    client_type) = verify_decode_raw((s_new, 'tmp'), my_receive(s_new))
    print("received message from car")
    return decoded_data

def proc_client(client):
    string = "processing: " + repr(client[0]) + " " + repr(client[1])
    print (time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + string)
    received_data = my_receive(client[0]).decode()
    try:
        (decoded_data,
        client_id,
        client_type) = verify_decode_raw(client, received_data)
    except (SignatureError, DecodeError):
        return 0
    print("received and decoded data:", decoded_data)
    if (decoded_data == "guard on"):
        try:
            response = send_message_to_car("guard on", client_id, client_type)
        except (SignatureError, DecodeError):
            print("[ERROR] send message fail")
            return 0
        if (response == "guard started"):
            info_str = time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + "STARTED GUARDD FOR CLIENT " + client_id
            print (info_str)
            my_send(client[0], srv_msg_wrap(info_str, client_id))
        elif (response == "guard already running"):
            info_str = time.strftime("[%d/%m/%y %H:%M:%S][ERROR] ",time.gmtime()) + "GUARD ALREADY RUNNING for" + client_id
            print (info_str)
            my_send(client[0], srv_msg_wrap(info_str, client_id))
    elif (decoded_data == "guard off"):
        try:
            response = send_message_to_car("guard off", client_id, client_type)
        except (SignatureError, DecodeError):
            print("[ERROR] send message fail")
            return 0
        if (response == "guard stopped"):
            info_str = time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + "STOPPED GUARDD FOR CLIENT " + client_id
            print (info_str)
            my_send(client[0], srv_msg_wrap(info_str, client_id))
        elif (response == "guard not running"):
            info_str = time.strftime("[%d/%m/%y %H:%M:%S][ERROR] ",time.gmtime()) + "GUARD ALREADY NOT for" + client_id
            print (info_str)
            my_send(client[0], srv_msg_wrap(info_str, client_id))
    elif (decoded_data == "SOS"):
        info_str = time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + "SOS SIGNAL from: " + client_id
        print (info_str)
        my_send(client[0], srv_msg_wrap("OPERATIONAL TEAM IS ON THE WAY", client_id))
    else:
        info_str = time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + "unrecognized command" + decoded_data + " from: " + client_id
        print (info_str)
        my_send(client[0], srv_msg_wrap(info_str, client_id))

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

if __name__ == "__main__":
    HOST = ""
    PORT = 50012

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    pc = ProcThread()
    pc.start()
    while 1:
        (client_socket, addres) = s.accept()
        print("accepted connection from ", addres)
        pc.add_client((client_socket, addres))
