// Accueil.js
//============================================================================
const serverIP = "192.168.43.110"; // ben c'est l'adresse IP du serveur     ||
//============================================================================

const username = sessionStorage.getItem('username');
const messageList = document.getElementById('message_list');

function deconnexion() {
    console.log(username);

    // Envoyer la requête de déconnexion
    navigator.sendBeacon(`http://${serverIP}:5000/disconnect/${username}`, JSON.stringify({}));

    // Effacer le sessionStorage
    sessionStorage.clear();

    window.location.href = "connexion.html";
}

function updateOnlineUserList() {
    const onlineUserList = document.getElementById('online_user_list');

    fetch(`http://${serverIP}:5000/online_user_list`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        onlineUserList.innerHTML = '';
        data["online_users"].forEach(user => {
            const li = document.createElement('li');
            li.textContent = user;
            onlineUserList.appendChild(li);
        });
    });
}

function envoyer(event){
    event.preventDefault(); // Empêche le rechargement de la page

    const message = document.getElementById('message').value;
    const destinataire = "everyone";

    fetch(`http://${serverIP}:5000/send_message/${message}/${username}/${destinataire}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        if (data !== null) {
            console.log("Message envoyé avec succès ! ID du message :", data);
            document.getElementById("Form").reset();
        } else {
            console.log("L'insertion a échoué.");
        }
    })
    .catch(error => {
        console.error("Erreur :", error);
        alert("Erreur lors de la connexion à l'API");
    });

}

function updateMessageList(){
    fetch(`http://${serverIP}:5000/get_messages/everyone`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        const messageList = document.getElementById('message_list');
        messageList.innerHTML = ''; 
        Object.values(data).forEach(msg => {
            const messageItem = document.createElement('li');
            const fullTimestamp = msg.timestamp;
            const timestampSansSecondes = fullTimestamp.slice(11, 16);
            messageItem.textContent = `${msg.sender} : ${msg.text} (${timestampSansSecondes})`;
            messageList.appendChild(messageItem);
        });
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des messages :", error);
        document.getElementById('message_list').textContent = "Erreur de connexion à l'API.";
    });
}

// Events lorsque le DOM (la page en gros) est chargé
document.addEventListener("DOMContentLoaded", function () {
    if (!username) {
        // alert("Vous n'êtes pas connecté !");
        window.location.href = "connexion.html";
    }
    console.log(`Utilisateur connecté : ${username}`);
    document.getElementById('username').textContent = username;

    // Liste des utilisateurs en ligne
    updateOnlineUserList();
    setInterval(() => {
        updateOnlineUserList();
    }, 5000); 

    // Liste des messages
    updateMessageList();
    setInterval(() => {
        updateMessageList();
    }, 2000);
});

// Event lorsque l'utilisateur ferme la page
window.addEventListener('beforeunload', deconnexion);


