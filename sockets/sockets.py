#!/usr/bin/env python3

import socket
import sys
import my_rsa

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 50012))
encoded_int = (my_rsa.encode(sys.argv[1], "../numbers.txt"));
encoded_bytes = encoded_int.to_bytes((encoded_int.bit_length() + 7) // 8, "big")
print("enc bytes = ", encoded_bytes)

send_data = encoded_bytes 
send_data += (b'\x00')
print(send_data)
s.sendall(send_data)
# data = s.recv(1024)
s.close()
# print ('Received ', (data.decode())) 
