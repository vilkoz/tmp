#!/usr/bin/env python2

import socket
import sys
import my_rsa
import my_sign
import json
import base64
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 50012))
encoded_int = (my_rsa.encode(sys.argv[1], "../numbers.txt"));
encoded_bytes = base64.b64encode(my_rsa.pack(encoded_int))

json_data_id = json.dumps({
    "data": encoded_bytes,
    "id" : "1234",
    "type" : "phone_number",
    "exp_time" : int(time.time()) + 10
    })
sign = my_sign.sign_data(json_data_id, "keys/1234.pem")
json_send = json.dumps({
    "sign" : sign,
    "data_id" : json_data_id,
    })
print(json_send)
send_data = json_send
send_data += (b'\x00')
    # print(send_data)
    # data = s.recv(1024)
    # print ('Received ', (data.decode())) 
s.sendall(send_data)
s.close()
