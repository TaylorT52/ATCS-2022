const interval = 200; 
const minPos = -500; 
var lastScroll = 0; 
var triggered = false;
var elementsToShow = document.querySelectorAll('.show-on-scroll');
elementsToShow = Array.from(elementsToShow); 
var scroll = window.requestAnimationFrame || function(callback){ window.setTimeout(callback, 1000/60)};

window.addEventListener('scroll', () => {
    var test = document.documentElement.getBoundingClientRect().top; 
    if(test < minPos){
        if(!triggered){
            show(elementsToShow); 
        }
    }
    lastScroll = test; 
})

function show(arr) {
    if (arr.length === 0) {
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