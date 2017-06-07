#!/usr/bin/env python2.7
from __future__ import print_function
import os
import sys
import json

DB_PATH = "database/"

def insert(phone_number, car_serial):
    if (os.path.isfile("database.json")):
        of = open("database.json", "r")
        data = json.loads(of.read())
        of.close()
    else:
        data = []
    data.append({"phone_number" : phone_number, "car_serial" : car_serial})
    json_data = json.dumps(data)
    with open("database.json", "w+") as f:
        f.write(json_data)
    os.system("./keys/new_key.sh " + phone_number)
    os.system("./keys/new_key.sh " + car_serial)
    print("Insered")

def get_match_key(value, field):
    if (os.path.isfile("database.json")):
        of = open("database.json", "r")
        data = json.loads(of.read())
        of.close()
        for node in data:
            if node[field] == value:
                trash = node.pop(field)
                return list(node.values())[0]
        return False
    else:
        print("[ERROR] NO DATABASE")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("script for inserting values in database")
        print("usage: ./databse.py phone_number car_serial")
        sys.exit(0)
    insert(sys.argv[1], sys.argv[2])
    # print("find by phone 1234: " + get_match_key("1234", 'phone_number'))
    # print("find by car_serial: " + get_match_key("192.168.0.247", 'car_serial'))

