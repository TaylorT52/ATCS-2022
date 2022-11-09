const interval = 200; 
const intervalSlide = 100;
const minPosEx = -3500; 
var lastScroll = 0; 
var triggeredEx = false;
var triggeredLs = false;
var minPosLs = -500; 

var slideElements = document.querySelectorAll('.fade-left')
var elementsToShow = document.querySelectorAll('.show-on-scroll');
elementsToSlide = Array.from(slideElements); 
elementsToShow = Array.from(elementsToShow); 
var scroll = window.requestAnimationFrame || function(callback){ window.setTimeout(callback, 1000/60)};

window.addEventListener('scroll', () => {
    var test = document.documentElement.getBoundingClientRect().top; 
    if(test < minPosEx){
        if(!triggeredEx){
            show(elementsToShow); 
        }
    }else if(test < minPosLs){
        if(!triggeredLs){
            console.log(elementsToSlide.length);
            slideIn(elementsToSlide); 
        }
    }
    lastScroll = test; 
})

function slideIn(arr) {
    if (arr.length == 0) {
        triggeredLs = true;
        return;
    }
    arr[0].classList.add("active");
    arr[0].classList.remove("not-visible")

    setTimeout(() => {
        slideIn(arr.slice(1))
    }, intervalSlide);
}

function show(arr) {
    if (arr.length == 0) {
        return;
    }
    arr[0].style.opacity = 1; 

    setTimeout(() => {
        show(arr.slice(1));
    }, interval);  
}

function goTo(id){
    var loc; 
    switch(id){
        case 1:
            loc = "loc-1"; 
            break;
    }
    document.getElementById(loc).scrollIntoView({behavior: 'smooth'});
}