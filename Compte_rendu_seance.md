# Compte rendu avancement séance

## Séance 1 - 16/04/25

**Membres présents :** Charlotte, Mathieu & Louna

**Travail effectué :**
- discussion sur l'architecture
- début de la programmation des API
- début début du front (lecture doc)

**A faire**
- Changement de user_id à user_name dans l'API (logique différente)
- Interface de base pour visualiser et tester

## Séance 2 - 17/04/25

**Membres présents :** Charlotte, Mathieu & Louna

**Travail effectué :**
- Structure des données dans Redis :
    - online_users : set des utilisateurs connectés
    - user:<nom> <password> : hashtable avec les informations de l'utilisateur
- Strcture des données dans MongoDB :
    - messages : collection avec les messages envoyés
        - id : identifiant du message
        - text : texte du message
        - sender : nom de l'utilisateur qui a envoyé le message
        - receiver : nom de l'utilisateur qui a reçu le message ("everyone" réservé pour le chat public)
        - timestamp : date d'envoi du message (généré automatiquement par le serveur)
- Définition des différentes requêtes possibles pour utiliser l'API (voir `backend/api.py`, il y a des exemples)
- Pages de connexion/incription fonctionnelles
- Début des variables de session

**A faire :**
- Finir les variables de session
- Developper le chat :)

**Améliorations possibles :**
- Hashage du mot de passe
- Statistiques sur les utilisateurs via l'API (nb de messages envoyés, nb de messages reçus, nb de communications entre deux personnes, etc.)


## Séance 3 - 05/05/25

**Membres présents :** Charlotte, Mathieu & Louna

**Travail effectué :**
- Session fonctionnelle 
- Deconnexion
- Affichage des utilisateurs en lignes

- Chat global !!!!
    - Formulaire pour envoie de message (ils sont bien enregistrés dans mongodb)
    - Récupération des messages envoyées
