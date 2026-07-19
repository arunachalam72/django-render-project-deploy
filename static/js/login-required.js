document.addEventListener("DOMContentLoaded", function () {

    const isLoggedIn =
        document.body.dataset.authenticated === "true";

    if (isLoggedIn) return;

    const toast = document.getElementById("loginToast");

    document.querySelectorAll(".login-required").forEach(link => {

        link.addEventListener("click", function(e){

            e.preventDefault();

            toast.classList.add("show");

            clearTimeout(window.toastTimer);

            window.toastTimer = setTimeout(() => {
                toast.classList.remove("show");
            },3000);

        });

    });

});