# utils.py

import json
import os

DATA_FILE = "data_store.json"

# Ensure file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"admins": [], "channels": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_admins():
    return load_data().get("admins", [])

def add_admin(uid):
    data = load_data()
    if uid not in data["admins"]:
        data["admins"].append(uid)
        save_data(data)

def remove_admin(uid):
    data = load_data()
    if uid in data["admins"]:
        data["admins"].remove(uid)
        save_data(data)

def get_channels():
    return load_data().get("channels", [])

def add_channel(cid):
    data = load_data()
    if cid not in data["channels"]:
        data["channels"].append(cid)
        save_data(data)

def remove_channel(cid):
    data = load_data()
    if cid in data["channels"]:
        data["channels"].remove(cid)
        save_data(data)
