import { serverIP } from './config.js';

function inscription(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const passwordConfirm = document.getElementById("password_conf").value;

    const forbidden = /[:\/*]/;


    if (username === "" || password === "" || passwordConfirm === "") {
        alert("Veuillez remplir tous les champs !");
        return;
    }

    if (password !== passwordConfirm) {
        alert("Les mots de passe ne correspondent pas !");
        return;
    }

    if (forbidden.test(username) || forbidden.test(password)) {
        alert("Le nom d'utilisateur ou le mot de passe ne doit pas contenir ':', '*' ou '/' !");
        return;
    }

    fetch(`http://${serverIP}:5000/register/${username}/${password}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Réponse de l'API :", data);

        if (data.status === "error") {
            alert(data.message);
        } else if (data.status === "registered") {
            sessionStorage.setItem('username', username);
            sessionStorage.setItem('password', password);
            alert(`Inscription réussie pour ${username}`);
            window.location.href = "accueil.html";
        }
    })
    .catch(error => {
        console.error("Erreur :", error);
        alert("Erreur lors de la connexion à l'API");
    });
}

function goToConnexion(){
    window.location.href = 'connexion.html';
}
window.goToConnexion = goToConnexion;

document.querySelector('form').addEventListener('submit', function(event) {
    inscription(event);
});
