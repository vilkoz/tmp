#!/usr/bin/python3

import sys
from math import ceil
from random import randint

VERBOSE = True

def num_to_char(__r):
    __c = []
    while __r > 0:
        __c.insert(0,chr(__r & 0xff))
        __r >>= 8
    return("".join(__c))

def num_to_char_res(__r):
    __c = []
    while __r > 0:
        tmp = __r & 0xff
        if tmp == 0:
            break
        __c.insert(0,chr(tmp))
        __r >>= 8
    return("".join(__c))

def char_to_num(__line):
    __num = []
    for c in __line:
        __num.append(ord(c))
    __msg = int(0)
    for c in __num:
        __msg <<= 8
        __msg += c
    return(__msg)

def my_chr64(__chr):
    if (ord(__chr) < 32):
        return (chr(ord(__chr) + ord('A')));
    elif (ord(__chr) < 60):
        return (chr(ord(__chr) + ord('a') - 32));
    elif (ord(__chr) < 64):
        return (chr(ord(__chr) + 23 - 60));

def my_base64(__num):
    __char = []
    while (__num > 0):
        __char.insert(0, my_chr64(chr(__num & 0x3f)))
        __num >>= 6
    return("".join(__char))

def print_hex(__num):
    __hex_arr = []
    while (__num > 0):
        __hex_arr.append(__num & 0xff)
        __num >>= 8
    j = 32;
    for byte in reversed(__hex_arr):
        print("%02x" % byte, end="")
        j -= 1;
        if (j % 2 == 0):
            print("", end=" ")
        if (j == 0):
            print("")
            j = 32
    print("")

def print_res(__num):
    __hex_arr = []
    while (__num > 0):
        __hex_arr.append(__num & 0xff)
        __num >>= 8
    j = 32;
    is_pad = 1
    for byte in reversed(__hex_arr):
        if not is_pad:
            print("%02x" % byte, end="")
        j -= 1;
        if (j % 2 == 0):
            if not is_pad:
                print("", end=" ")
        if (j == 0):
            if not is_pad:
                print("")
            j = 32
        if byte == 0x00:
            is_pad = 0
    print("")

def parse_nums(fo):
    for line in fo:
        disp_flag = 0
        if (line[0] == "n"):
            if VERBOSE:
                print("n")
            disp_flag = 1
        new = line[line.find("-") + 2:len(line) - 1]
        hexd = new.split();
        hexd = "".join(hexd);
        new_int = int(hexd, 16)
        if (disp_flag == 1 and VERBOSE):
            print_hex(new_int);
        if (line[0] == "n"):
            n = new_int
        if (line[0] == "e"):
            e = new_int
        if (line[0] == "d"):
            d = new_int
    return (n, e, d)

def generate_random_padding(rlen, msg):
    pad = []
    pad.append(chr(0x00))
    pad.append(chr(0x02))
    for i in range(0, rlen):
        rb = randint(1, 255) & 0xFF
        pad.append(chr(rb))
    pad.append(chr(0x00))
    if VERBOSE:
        print("len pad : " + str(len(pad)))
    pad_str = "".join(pad)
    pad_str = pad_str + num_to_char(msg)
    return (char_to_num(pad_str))

def check_len(pub_key, msg):
    NUM_SIZE = len(str(bin(pub_key)[2:])) // 8
    MSG_SIZE = ceil(len(str(bin(msg)[2:])) / 8)
    if VERBOSE:
        print("NUM_SIZE = " + str(NUM_SIZE))
        print("MSG_SIZE = " + str(MSG_SIZE))
    rlen = NUM_SIZE - MSG_SIZE - 3
    if rlen < 8:
        print("Message is too long!")
        exit(2)
    return (rlen)

def encode(msg_text, numbers_path):
    fo = open(numbers_path, "r")
    (n, e, d) = parse_nums(fo)
    msg = char_to_num(msg_text)
    rlen = check_len(n, msg)
    if VERBOSE:
        print("msg")
        print_hex(msg)
        print("random padding")
    msg = (generate_random_padding(rlen, msg))
    if VERBOSE:
        print_hex(msg)
    r = pow(msg, e, n)
    if VERBOSE:
        print("encoded1")
        print_hex(r)
    return (r)

def decode(chiper_text, numbers_path):
    fo = open(numbers_path, "r")
    (n, e, d) = parse_nums(fo)
    r = pow(chiper_text, d, n)
    if VERBOSE:
        print("decoded")
        print_res(r)
        print(num_to_char_res(r))
    return (num_to_char_res(r))

def echo_verbose():
    print(VERBOSE)


# if (len(sys.argv) != 2):
#     print("usage: ./parse.py message")
#     exit(1)
# else:
#     print("message len = " + str(len(sys.argv[1])))
# fo = open("numbers.txt", "r")
# (n, e, d) = parse_nums(fo)

# check_len(n, msg)

# msg = char_to_num(sys.argv[1]);
# print("msg");
# print_hex(msg)

# print("random padding")
# msg = (generate_random_padding(rlen, msg))
# print_hex(msg)

# r = pow(msg, e, n)
# print("encoded1")
# print_hex(r)

# r = encode(sys.argv[1], "numbers.txt")

# r = pow(r, d, n)
# print("decoded")
# print_res(r)
# print(num_to_char_res(r))
