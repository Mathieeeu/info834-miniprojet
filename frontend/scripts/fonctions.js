import { serverIP } from './config.js';

export function goToConversation(){
    window.location.href = "conversation.html";
}
window.goToConversation = goToConversation;

export function goToAccueil(){
    window.location.href = "accueil.html";
}
window.goToAccueil = goToAccueil;

function handleUserLeaving(event) {
    const username = sessionStorage.getItem('username');
    if (username) {
        // Envoyer la requête de déconnexion
        navigator.sendBeacon(`http://${serverIP}:5000/disconnect/${username}`, JSON.stringify({}));
    }
}

export function deconnexion() {
    const username = sessionStorage.getItem('username');

    // Envoyer la requête de déconnexion
    navigator.sendBeacon(`http://${serverIP}:5000/disconnect/${username}`, JSON.stringify({}));

    // Effacer le sessionStorage
    sessionStorage.clear();

    window.location.href = "connexion.html";
}
window.deconnexion = deconnexion;

export function updateOnlineUserList() {
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

export function updateUserList() {
    const UserList = document.getElementById('user_list');

    fetch(`http://${serverIP}:5000/user_list`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        UserList.innerHTML = '';
        data["user_list"].forEach(user => {
            const li = document.createElement('li');
            li.textContent = user;
            li.addEventListener("click", () => {
                sessionStorage.setItem("destinataire", user);
                document.getElementById('contact-name').textContent = user; 
                updateMessageList("conversation"); 
            });
            UserList.appendChild(li);
        });
    });
}

export function envoyer(event, page){
    event.preventDefault(); // Empêche le rechargement de la page

    const username = sessionStorage.getItem('username');
    const message = document.getElementById('message').value;

    if (page === "accueil") {
        var destinataire = "everyone";
    } else if (page === "conversation") {
        if (sessionStorage.getItem("destinataire") != null){
            var destinataire = sessionStorage.getItem("destinataire");
        }
         else{
            var destinataire = "everyone";
         }
    } else {
        console.error("Page non reconnue :", page);
        return;
    }

    var request = `http://${serverIP}:5000/send_message/${message}/${username}/${destinataire}`;
    fetch(request, {
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
    updateMessageList(page);
}
window.envoyer = envoyer;

export function updateMessageList(page){
    const username = sessionStorage.getItem('username');
    if (page === "accueil") {
        var request = `http://${serverIP}:5000/get_messages/everyone`
    } else if (page === "conversation") {
        const destinataire = sessionStorage.getItem('destinataire');
        if (!destinataire) {
            var request = `http://${serverIP}:5000/get_messages/${username}`
        }
        else{
            var request = `http://${serverIP}:5000/get_private_messages/${username}/${destinataire}`;
        }
        
    } else {
        console.error("Page non reconnue :", page);
        return;
    }

    fetch(request, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        const messageList = document.getElementById('message_list');
        messageList.innerHTML = ''; 
        let previousDate = null;

        Object.values(data).forEach(msg => {
            const messageItem = document.createElement('li');
            const fullTimestamp = msg.timestamp;
            const currentDate = fullTimestamp.slice(0, 10); // Format: YYYY-MM-DD

            // séparateur de date quand la date change
            if (currentDate !== previousDate) {
                const dateSeparator = document.createElement('li');
                dateSeparator.classList.add('date-separator');
                dateSeparator.textContent = new Date(currentDate).toLocaleDateString();
                messageList.appendChild(dateSeparator);
                previousDate = currentDate;
            }

            if (msg.sender === username) {
                messageItem.classList.add('message-sent');
            } else {
                messageItem.classList.add('message-received');
            }

            const timestampSansSecondes = fullTimestamp.slice(11, 16);
            messageItem.innerHTML = `<span class="author">${msg.sender}<br></span><span class="msgTxt">${msg.text}</span><span class="timestamp"><br>${timestampSansSecondes}</span>`;
            messageList.appendChild(messageItem);
        });
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des messages :", error);
        document.getElementById('message_list').textContent = "Erreur de connexion à l'API.";
    });
}

export function addEventListeners(page) {
    // Events lorsque le DOM (la page en gros) est chargé
    document.addEventListener("DOMContentLoaded", function () {
        const username = sessionStorage.getItem('username');
        const password = sessionStorage.getItem('password');

        var connexionRequest = `http://${serverIP}:5000/login/${username}/${password}`;
        fetch(connexionRequest, {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "error") {
                // Erreur de connexion
                alert(data.message);
                window.location.href = "connexion.html";
            }
        })

        if (!username) {
            alert("Vous n'êtes pas connecté !");
            window.location.href = "connexion.html";
        }
        document.getElementById('username').textContent = username;

        var userListUpdateInterval = 5000;
        var messageListUpdateInterval = 20000;

        // Liste des utilisateurs en ligne
        if (page === "accueil") {
            updateOnlineUserList();
            setInterval(() => {
                updateOnlineUserList();
            }, userListUpdateInterval);
        }

        // Liste des messages
        updateMessageList(page);
        setInterval(() => {
            updateMessageList(page);
        }, messageListUpdateInterval);

        //Liste de tous les utilisateurs
        if (page === "conversation") {
            updateUserList();
            setInterval(() => {
                updateUserList();
            }, userListUpdateInterval);
        }
    });

    // Event lorsque l'utilisateur ferme la page
    window.addEventListener('beforeunload', handleUserLeaving);
    window.addEventListener('unload', handleUserLeaving);
}