#!/usr/bin/env python2.7

import aes128

def encrypt(input_text, key):
    crypted_data = []
    temp = []
    for byte in input_text:
        temp.append(byte)
        if len(temp) == 16:
            crypted_part = aes128.encrypt(temp, key)
            crypted_data.extend(crypted_part)
            del temp[:]
    else:
        #padding v1
        # crypted_data.extend(temp)

        # padding v2
        if 0 < len(temp) < 16:
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(1)
            crypted_part = aes128.encrypt(temp, key)
            crypted_data.extend(crypted_part)
    return crypted_data

def decrypt(chiper_text, key):
    decrypted_data = []
    temp = []
    for byte in chiper_text:
        temp.append(byte)
        if len(temp) == 16:
            decrypted_part = aes128.decrypt(temp, key)
            decrypted_data.extend(decrypted_part)
            del temp[:] 
    else:
        #padding v1
        # decrypted_data.extend(temp)
        
        # padding v2
        if 0 < len(temp) < 16:
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(1)
            decrypted_part = aes128.encrypt(temp, key)
            decrypted_data.extend(crypted_part) 
    return decrypted_data
