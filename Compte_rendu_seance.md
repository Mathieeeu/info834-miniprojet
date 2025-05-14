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
    - Récupération des messages envoyées (problème avec le format retourné des messages qui comportaient des ObjetcId et non des id simple)

**A faire :**
- Chat privé
- Mise en forme du site


## Séance 4 - 06/05/25

**Membres présents :** Charlotte, Mathieu & Louna

**Travail effectué :**
- Restructuration des fichiers et création d'un fichier de script général 
    - beaucoup d'erreur du à ça, notamment à cause des modules -> mettre sous la fonction _window.nomfonction = nomfonction;_
    - on avait un listener pour deconnecter l'utilisateur correctement s'il fermait la page sans se deco et il pose des problème avec le sessionStorage lors du changement de page (il est appellé lors de l'import)
- Page de chat personnel
    - envoyer un message à un utilisateur
    - voir les messages enchangés avec un utilisateur choisi dans la liste des utilisateur
- CSS des pages
    - connexion
    - inscription
    - accueil

**Amélioration possible :**
- barre de recherche des gens
- trouver une façon de déconnecter si l'onglet est fermé sans réinitialiser la sessionStorage


## Séance 5 - 14/05/25

**Membres présents :** Charlotte, Mathieu & Louna

**Travail effectué :**
- Fin du CSS
- Rapport
- Ajout de statistiques
    - utilisateur le + bavard
    - utilisateur le + solicité ("everyone" ne pouvant pas être retourné)

- Présentation