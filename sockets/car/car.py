#!/usr/bin/env python2.7
from __future__ import print_function
import my_rsa
import my_sign
import time
import json
import base64
import socket
import sys
import threading
from server import my_receive
from server import my_send

SERVER_IP = "192.168.0.2"
SRV_KEY_PATH = "../../numbers.txt"
CAR_ID = "192.168.0.247"
PRIVATE_KEY_PATH = "../keys/" + CAR_ID + ".pem"
MODE = 0

HOST = ""
PORT = 50012

class DecodeError(Exception):
    pass
class SignatureError(Exception):
    pass

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def run(self):
        print("Started guard mode")
        while True and not self.stopped():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, 50012))
            data = "STATUS: OK, GPS: Latitude: 41.7696 Longitude: -88.4588"
            my_send(s, msg_wrap_to_send(data))
            print(time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) +
                    "Sending status to server")
            s.close()
            time.sleep(10)
        print("Stopped InfoThread")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


def msg_wrap_to_send(msg):
    encoded_int = (my_rsa.encode(msg, SRV_KEY_PATH));
    encoded_bytes = base64.b64encode(my_rsa.pack(encoded_int))
    json_data_id = json.dumps({
        "data": encoded_bytes,
        "id" : CAR_ID,
        "type" : "car_serial",
        "exp_time" : int(time.time()) + 10
        })
    sign = my_sign.sign_data(json_data_id, PRIVATE_KEY_PATH)
    json_send = json.dumps({
        "sign" : sign,
        "data_id" : json_data_id,
        })
    # print(json_send)
    send_data = json_send
    # send_data += (b'\x00')
    return send_data

def verify_srv_sign(received_data):
    try:
        json_msg = json.loads(received_data)
        signature = json_msg['sign'].encode()
        data_id_json = json_msg['data_id'].encode()
    except Exception as e:
        print("exception: ", (e.message))
        print("[ERROR] wrong message format! from srv")
        raise SignatureError
    if not (my_sign.verify_sign(signature, data_id_json, SRV_KEY_PATH)):
        print("[ERROR] wrong signature from")
        raise SignatureError
    return data_id_json

def decode_srv_message(data_id_json):
    try:
        data_id = json.loads(data_id_json)
        exp_time = int(data_id['exp_time'])
    except Exception as e:
        print("[ERROR] exception: ", (e.message))
        print("[ERROR] wrong data_id format from")
        raise DecodeError
    if (int(time.time()) > exp_time):
        print("[ERROR] expired message from")
        raise DecodeError
    b64_data = bytes(base64.b64decode(data_id['data']))
    data = my_rsa.unpack(b64_data)
    return my_rsa.decode(data, PRIVATE_KEY_PATH)

def msg_unwrap_raw(received_data):
    try:
        data_id_json = verify_srv_sign(received_data)
    except SignatureError:
        raise SignatureError
    try:
        decoded_data = decode_srv_message(data_id_json)
    except DecodeError:
        raise DecodeError
    return decoded_data

def proc_connection(con_socket, info_thread):
    print("receivng....")
    rec_data = my_receive(con_socket).decode()
    print("received data: ", rec_data)
    try:
        data = msg_unwrap_raw(rec_data)
    except SignatureError:
        print(time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + 
                "[SECURITY WARNING] Invalid signature for: " + repr(con_socket))
    except DecodeError:
        print(time.strftime("[%d/%m/%y %H:%M:%S] ",time.gmtime()) + 
                "[SECURITY WARNING] Decription error for: " + repr(con_socket))
    print("unwrapped data: ", data)
    if (data == "guard on"):
        if (info_thread != 0):
            my_send(con_socket, msg_wrap_to_send("guard already runnnig"))
            return info_thread
        info_thread = StoppableThread()
        info_thread.start()
        print("sending response")
        my_send(con_socket, msg_wrap_to_send("guard started"))
        print("sended response")
        con_socket.close()
        return info_thread
    elif (data == "guard off"):
        if (info_thread == 0):
            my_send(con_socket, msg_wrap_to_send("guard not runnnig"))
            return info_thread
        info_thread.stop()
        del info_thread
        my_send(con_socket, msg_wrap_to_send("guard stopped"))
        con_socket.close()
        return 0
    else:
        print("[WARNING] Unrecognized command: " + data)
        return info_thread


if __name__ == "__main__":
    s_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_.bind((HOST, PORT))
    s_.listen(1)
    info_thread_ = 0
    try:
        while 1:
            (con_socket_, addres) = s_.accept()
            print("accepted connection from ", addres)
            info_thread_ = proc_connection(con_socket_, info_thread_)
    except KeyboardInterrupt:
        sys.exit()
