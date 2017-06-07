#!/usr/bin/env python2.7
from __future__ import print_function
import os
import json

DB_PATH = "database/"

def db_insert(phone_number, car_serial):
    if (os.path.isfile("database.json")):
        of = open("database.json", "r")
        data = json.loads(of.read())
        of.close()
    else:
        data = []
    data.append({"phone" : phone_number, "car_serial" : car_serial})
    json_data = json.dumps(data)
    with open("database.json", "r+") as f:
        f.write(json_data)
        f.truncate()
    os.system("./keys/new_key.sh " + phone_number)
    os.system("./keys/new_key.sh " + car_serial)
    print("Insered")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("script for inserting values in database")
        print("usage: ./databse.py phone_number car_serial")
        sys.exit(0)
    db_insert(sys.argv[1], sys.argv[2])

