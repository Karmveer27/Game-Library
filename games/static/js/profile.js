document.addEventListener('DOMContentLoaded', function () {
    var slideIndex = 0;

    function showSlides() {
        var i;
        var slides = document.getElementsByClassName("slide");
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1;
        }
        slides[slideIndex - 1].style.display = "block";
        setTimeout(showSlides, 2000);
    }

    showSlides();

    console.log("Getting to here");
    var logStatus = document.getElementById("log-status");
    if (logStatus) {
        logStatus.style.color = "green";
        logStatus.innerText = "Logged In";

        document.getElementById("login-button").style.display = "none";
        document.getElementById("register-button").style.display = "none";
        document.getElementById("logout-button").style.display = "block";
    }
    else{
        document.getElementById("logout-button").style.display = "none";
    }


    const game_list_button = document.getElementById("show_games");
    const allGames = document.querySelectorAll(".game_title_list");
    let isVisable = false;

    game_list_button.addEventListener('click', function () {
        if (isVisable) {
            allGames.forEach((game) => (game.style.display = "none"));
        } else {
            allGames.forEach((game) => (game.style.display = "block"));
        }
        isVisable = !isVisable;
    });




});
//////// List Button maker


