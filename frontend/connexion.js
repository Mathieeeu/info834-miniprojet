
function connexion(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const forbidden = /[:\/*]/;

    if (username === "" || password === "") {
        alert("Veuillez remplir tous les champs !");
        return;
    }

    if (forbidden.test(username) || forbidden.test(password)) {
        alert("Le nom d'utilisateur ou le mot de passe ne doit pas contenir ':', '*' ou '/' !");
        return;
    }

    fetch(`http://localhost:5000/login/${username}/${password}`, {// c l'api faut hardcodé l'adresse IP
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Réponse de l'API :", data);
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('password', password);
        // Redirection
        window.location.href = "accueil.html"; 
    })
    .catch(error => {
        console.error("Erreur :", error);
        alert("Erreur lors de la connexion à l'API");
    });
}