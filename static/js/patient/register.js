const nextBtn = document.getElementById("nextBtn");
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");

nextBtn.addEventListener("click", function () {

    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm_password").value;

    if (password.length < 8) {
        alert("Mot de passe trop court");
        return;
    }

    if (password !== confirm) {
        alert("Les mots de passe ne correspondent pas");
        return;
    }

    step1.style.display = "none";
    step2.style.display = "block";
});