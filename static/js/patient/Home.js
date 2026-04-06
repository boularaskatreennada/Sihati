function search() {
    let query = document.getElementById("searchInput").value;

    if (query.trim() === "") {
        alert("Veuillez entrer un mot clé !");
    } else {
        alert("Recherche pour : " + query);
        // plus tard: redirection vers page résultats
        // window.location.href = "/search?q=" + query;
    }
}