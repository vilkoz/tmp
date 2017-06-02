#!/usr/bin/env python2.7

import my_rsa
import hashlib
import json

def sign_data(data, keys_path):
    sha256_sum = hashlib.sha256(data).hexdigest()
    sign = my_rsa.encode_withot_pad(sha256_sum, keys_path)
    return (json.dumps((sign, data)))

print(sign_data(b"asdfasdf", "../numbers.txt"))
