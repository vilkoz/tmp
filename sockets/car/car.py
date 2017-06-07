#!/usr/bin/env python2.7
from __future__ import print_function
import my_rsa
import my_sign
import time
import json
import base64
import socket
from server import my_receive
from server import my_send

MODE = 0

HOST = ""
PORT = 50012

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def proc_connection(con_socket, addres):
    rec_data = my_receive(con_socket).decode()
    print("received data: ", rec_data)

while 1:
    (con_socket, addres) = s.accept()
    proc_connection(con_socket, addres)
    print("accepted connection from ", addres)
