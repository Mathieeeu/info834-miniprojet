"""
Connexion à Redis pour gérer les utilisateurs en ligne et les statistiques de connexion
"""

import redis

r = redis.Redis(host='localhost', port=6379)

def ping() -> dict:
    return {"ping": "pong"}

def connect(username: str) -> dict:
    r.sadd("online_users", username)
    return {"status": "success", "username": username}

def disconnect(username: str) -> dict:
    r.srem("online_users", username)
    return {"status": "disconnected", "username": username}

def register(username: str, password: str) -> dict:
    if r.exists(username):
            return {"status": "error", "message": "User already exists"}
    r.set(username, password)
    return {"status": "success", "username": username}

def login(username: str, password: str) -> dict:
    if r.exists(username):
        stored_password = r.get(username).decode('utf-8')
        if stored_password == password:
            r.sadd("online_users", username)
            return {"status": "success", "username": username}
        else:
            return {"status": "error", "message": "Invalid password"}
    else:
        return {"status": "error", "message": "User does not exist"}

def get_user_count() -> dict:
    user_count = r.scard("online_users")
    return {"user_count": user_count}

def get_user_list() -> dict:
    online_users = r.smembers("online_users")
    return {"online_users": [user.decode('utf-8') for user in online_users]}

