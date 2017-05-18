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



for line in fo:
    new = line[line.find("-") + 2:len(line) - 1]
    # print(new)
    hexd = new.split();
    # print(hexd)
    hexd = "".join(hexd);
    # print(hexd)
    new_int = int(hexd, 16)
    # print(new_int)
    if (line[0] == "n"):
        n = new_int
    if (line[0] == "e"):
        e = new_int
    if (line[0] == "d"):
        d = new_int


print(sys.argv[1])
msg = char_to_num(sys.argv[1]);
r = pow(msg, e, n)
print("encoded")
print((r))
r = pow(r, d, n)
print("decoded")
print((r))
print(num_to_char(r))
