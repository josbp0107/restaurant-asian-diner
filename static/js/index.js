window.addEventListener("load", function(){
    new Glider(document.querySelector(".elementos_lista"), {
         // Mobile-first defaults
        slidesToShow: 3,
        slidesToScroll: 3,
        scrollLock: true,
        dots: '.indicadores',
        arrows: {
        prev: '.carrouselanterior',
        next: '.carrouselsiguiente'
        },
    })
})