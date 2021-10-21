window.addEventListener("load", function(){
    new Glider(document.querySelector(".elementos_lista"), {
         // Mobile-first defaults
        slidesToShow: 4,
        slidesToScroll: 4,
        scrollLock: true,
        dots: '.indicadores',
        arrows: {
        prev: '.carrouselanterior',
        next: '.carrouselsiguiente'
        },
    })
})