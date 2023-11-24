document.addEventListener('DOMContentLoaded', function () {
    const gameCards = document.querySelectorAll('.game-card');



    gameCards.forEach(function (card) {
        const cardId = card.id;
        const heartIcon = document.getElementById('heart' + cardId);
        let isRed = false;

        card.addEventListener('mouseenter', function () {
            heartIcon.style.display = 'inline';
        });

        card.addEventListener('mouseleave', function () {
            heartIcon.style.display = 'none';
        });


        if(heartIcon.classList.contains('logged_in')) {
            heartIcon.addEventListener("click", function () {
                if (isRed) {
                    heartIcon.style.color = 'lightgray'
                } else {
                    heartIcon.style.color = 'red'
                }
                isRed = !isRed;

            })
        }
    });

    const redHearts = document.querySelectorAll(".red");
    redHearts.forEach(heart => {
        heart.style.color = 'red';
    })


});
