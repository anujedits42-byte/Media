import json
from pathlib import Path

DB = Path("users.json")

def load():
    if not DB.exists():
        return []
    return json.loads(DB.read_text())

def save(data):
    DB.write_text(json.dumps(data))

def add_user(uid):
    users = load()
    if uid not in users:
        users.append(uid)
        save(users)

def get_users():
    return load()
