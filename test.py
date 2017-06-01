#!/usr/bin/python3
import sys
import my_rsa

chiper_text = my_rsa.encode(sys.argv[1], "numbers.txt")
clear_text = my_rsa.decode(chiper_text, "numbers.txt")
