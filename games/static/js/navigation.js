let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

//menu.addEventListener('click', () => {

  //  navbar.classList.toggle('open');
//});


window.addEventListener('scroll', function() {
    var navbar = document.getElementById('navbar');
    if (window.scrollY != 0) {
        navbar.classList.add('hidden');
    } else {
        navbar.classList.remove('hidden');
    }
});



