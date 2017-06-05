#!/usr/bin/env python2.7

import my_rsa
import hashlib
import json
import base64

def sign_data(data, keys_path):
    sha256_sum = hashlib.sha256(data).hexdigest()
    sign = base64.b64encode(str(my_rsa.encode_sign(sha256_sum, keys_path)),
            'ascii')
    return sign

def verify_sign(signature, data, keys_path):
    sha256_sum = hashlib.sha256(data).hexdigest()
    decr_sign = my_rsa.decode_sign(int(base64.b64decode(signature, 'asscii')),
            keys_path)
    print("sum =\n", sha256_sum)
    print("decr_sign =\n", decr_sign)
    return (sha256_sum == decr_sign)

if __name__ == "__main__":
    data_ = "my data"
    sign_ = sign_data(data_, "../numbers.txt")
    print(verify_sign(sign_, data_, "../numbers.txt"))
