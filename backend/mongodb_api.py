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
    client = MongoClient(f"{MONGO_SCHEME}://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_ADDRESS}/{MONGO_DB}?{MONGO_OPTIONS}")
    db = client[MONGO_DB]
    # Test de la connexion
    client.admin.command('ping')

    print("Connexion à MongoDB réussie")
except ConnectionFailure as e:
    print(f"Erreur de connexion à MongoDB: {e}")
except OperationFailure as e:
    print(f"Erreur d'opération MongoDB: {e}")
except Exception as e:
    print(f"Erreur bizarre et inattendue: {e}")

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
    Récupère les messages d'une certainecible
    """
    try:
        messages = db.messages.find({"reciever": reciever_name})
        return list(messages)
    except Exception as e:
        print(f"Erreur lors de la récupération des messages: {e}")
        return None
    