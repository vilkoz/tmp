#!/usr/bin/env python2.7
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
