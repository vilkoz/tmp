#!/usr/bin/python3

import sys

fo = open("numbers.txt", "r")

def num_to_char(__r):
    __c = []
    while __r > 0:
        __c.insert(0,chr(__r & 0xff))
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



for line in fo:
    disp_flag = 0
    if (line[0] == "n"):
        print("n")
        disp_flag = 1
    # if (line[0] == "d"):
    #     print("d" + "\n")
    #     disp_flag = 1
    new = line[line.find("-") + 2:len(line) - 1]
    # print(new)
    hexd = new.split();
    # print(hexd)
    hexd = "".join(hexd);
    new_int = int(hexd, 16)
    if (disp_flag == 1):
        # print(hexd + "\n")
        print_hex(new_int);
        # print(bin(new_int) + "\n")
    # # print(new_int)
    if (line[0] == "n"):
        n = new_int
    if (line[0] == "e"):
        e = new_int
    if (line[0] == "d"):
        d = new_int


# print(sys.argv[1])
msg = char_to_num(sys.argv[1]);
# msg = 0x506834cd47;
r = pow(msg, e, n)
print("msg");
# print(bin(msg));
print_hex(msg)
print("encoded1")
# print(hex(r));
print_hex(r)
# print("encoded")
# print(my_base64(r))
r = pow(r, d, n)
print("decoded")
print_hex(r)
# print((r))
print(num_to_char(r))
