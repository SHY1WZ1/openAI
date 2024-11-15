// Detect scroll and add a class to change navbar background color
window.addEventListener('scroll', function() {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {  // Change the number to adjust the scroll threshold
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});