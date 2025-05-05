"""
Connexion à Redis pour gérer les utilisateurs en ligne et les statistiques de connexion
"""

import redis

r = redis.Redis(host='localhost', port=6379)

def ping() -> dict:
    return {"ping": "pong"}

def clear_user_data() -> dict:
    """
    Attention : Supprime toutes les données utilisateur de Redis
    """
    r.flushdb()
    return {"status": "cleared all user data"}

def disconnect(username: str) -> dict:
    r.srem("online_users", username)
    return {"status": "disconnected", "username": username}

def register(username: str, password: str) -> dict:
    if username == "everyone":
        return {"status": "error", "message": "Tu ne peux pas t'appeler 'everyone' voyons!"}
    
    user_key = f"user:{username}"
    if r.exists(user_key):
        return {"status": "error", "message": "Username already exists"}
    
    r.hset(user_key, mapping={"password": password})
    r.sadd("online_users", username)
    return {"status": "registered", "username": username}

def login(username: str, password: str) -> dict:
    user_key = f"user:{username}"
    if not r.exists(user_key):
        return {"status": "error", "message": "Invalid username or password"}
    
    stored_password = r.hget(user_key, "password")
    if stored_password is None or stored_password.decode() != password:
        return {"status": "error", "message": "Invalid username or password"}
    
    r.sadd("online_users", username)
    return {"status": "logged_in", "username": username}

def get_online_user_count() -> dict:
    user_count = r.scard("online_users")
    return {"user_count": user_count}

def get_online_user_list() -> dict:
    online_users = r.smembers("online_users")
    return {"online_users": [user.decode('utf-8') for user in online_users]}

def get_user_count() -> dict:
    user_keys = r.keys("user:*")
    return {"user_count": len(user_keys)}


def get_user_list() -> dict:
    user_keys = r.keys("user:*")
    user_list = [key.decode('utf-8').split("user:")[1] for key in user_keys]
    return {"user_list": user_list}
