"""
API pour la connexion et l'utilisation d'une base de données mongodb pour le stockage/récuperatino des messages
"""
import os
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

# Variables d'environnement
load_dotenv()
MONGO_SCHEME = os.getenv("MONGO_SCHEME")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_ADDRESS = os.getenv("MONGO_ADDRESS")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_OPTIONS = os.getenv("MONGO_OPTIONS")

# Connexion à la base
try:
    print("Connexion à MongoDB...")
    uri = f"{MONGO_SCHEME}://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_ADDRESS}/{MONGO_DB}?{MONGO_OPTIONS}"
    client = MongoClient(uri)
    db = client[MONGO_DB]
    # Test de la connexion
    client.admin.command('ping')

    print("Connexion à MongoDB réussie")
except ConnectionFailure as e:
    print(f"Erreur de connexion à MongoDB: {e}")
    exit(1)
except OperationFailure as e:
    print(f"Erreur d'opération MongoDB: {e}")
    exit(1)
except Exception as e:
    print(f"Erreur bizarre et inattendue: {e}")
    exit(1)

def insert_message(text: str, sender_name: str, date: str, reciever_name: str):
    """
    Insère un message dans la collection messages

    :param message: Le message à insérer (dictionnaire) 
    
    (ex. {"text": "Bonjour Monde", "sender": "Charlotte", "timestamp": "2025-04-16", "reciever": "Louna"}) 

    (reciever_name = "everyone" pour chat général, sinon id de l'utilisateur)
    """
    message = {
        "text": text,
        "sender": sender_name,
        "timestamp": date,
        "reciever": reciever_name
    }
    
    try:
        result = db.messages.insert_one(message)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Erreur lors de l'insertion du message: {e}")
        return None

def get_messages(reciever_name: str):
    """
    Récupère les messages d'une certaine cible
    """
    try:
        messages = db.messages.find({"reciever": reciever_name})
        res = {}
        for message in messages:
            res[str(message["_id"])] = {
                "text": message["text"],
                "sender": message["sender"],
                "timestamp": message["timestamp"],
                "reciever": message["reciever"]
            }
        return res
    except Exception as e:
        print(f"Erreur lors de la récupération des messages: {e}")
        return None
    
def get_private_messages(sender, reciever):
    try:
        messages = db.messages.find({"$or": [
                {"sender": sender, "reciever": reciever},
                {"sender": reciever, "reciever": sender}
            ]}).sort("timestamp", 1)
        res = {}
        for message in messages:
            res[str(message["_id"])] = {
                "text": message["text"],
                "sender": message["sender"],
                "timestamp": message["timestamp"],
                "reciever": message["reciever"]
            }
        return res
    except Exception as e:
        print(f"Erreur lors de la récupération des messages privés : {e}")
        return []
    
def delete_messages_from_user(sender_name: str):
    """
    Supprime sans vergogne les messages de quelqu'un
    """
    try:
        result = db.messages.delete_many({"sender": sender_name})
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        print(e)
        return None