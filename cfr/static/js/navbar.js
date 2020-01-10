window.onload = function() {
  const burger = document.querySelector('.navbar-burger');
  const menu = document.querySelector('#navMenu');

  burger.onclick = function() {
    burger.classList.toggle('is-active');
    menu.classList.toggle('is-active');
  }
}
